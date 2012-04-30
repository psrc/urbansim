# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.misc import unique, DebugPrinter, write_to_text_file, quantile, write_table_to_text_file
from opus_core.logger import logger
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.sampling_toolbox import sample_noreplace
from numpy import arange, where, resize, zeros, array, logical_and, logical_or, logical_not, concatenate, ones, log, concatenate, newaxis, exp
from scipy.ndimage import histogram
import os


def match_parcels_to_constraints_and_templates(parcel_dataset,
                                                development_template_dataset,
                                                output_dir, log_scale=True, strict=True,
                                                output_points=False,
                                                parcel_index=None,
                                                template_index=None,
                                                consider_constraints_as_rules=True,
                                                template_opus_path="urbansim_parcel.development_template",
                                                dataset_pool=None,
                                                resources=None):
    """
    This function matches parcels to their constraints and templates and gives a summary about how many parcels have no match.
    It also creates a plot for each GLU and unit type of template ranges and densities.
    parcel_index - 1D array, indices of parcel_dataset (default is all parcels).
    template_index - index to templates that are available (default is all templates).
    If strict is True, parcels without templates are considered across GLU, otherwise only within each GLU. 
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    resources = Resources(resources)
    debug = resources.get("debug",  0)
    if not isinstance(debug, DebugPrinter):
        debug = DebugPrinter(debug)

    if parcel_index is not None and parcel_index.size <= 0:
        return None
        
    if parcel_index is not None:
        index1 = parcel_index
    else:
        index1 = arange(parcel_dataset.size())

    if template_index is not None:
        index2 = template_index
    else:
        index2 = arange(development_template_dataset.size())

    has_constraint_dataset = True
    try:
        constraints = dataset_pool.get_dataset("development_constraint") 
        constraints.load_dataset_if_not_loaded()
    except:
        has_constraint_dataset = False

    parcels_glu = parcel_dataset.compute_variables(['parcel.disaggregate(land_use_type.generic_land_use_type_id)'], dataset_pool=dataset_pool)
    if has_constraint_dataset:
        constraint_types = unique(constraints.get_attribute("constraint_type"))  #unit_per_acre, far etc
        development_template_dataset.compute_variables(map(lambda x: "%s.%s" % (template_opus_path, x), constraint_types), dataset_pool)
            
        parcel_dataset.get_development_constraints(constraints, dataset_pool, 
                                                   index=index1, 
                                                   consider_constraints_as_rules=consider_constraints_as_rules)
        generic_land_use_type_ids = development_template_dataset.compute_variables("urbansim_parcel.development_template.generic_land_use_type_id",
                                                       dataset_pool=dataset_pool)

    parcel_ids = parcel_dataset.get_id_attribute()
    template_ids = development_template_dataset.get_id_attribute()
    
    
    has_template = zeros(index1.size, dtype="int32")
    vacant_land = parcel_dataset.compute_variables(['urbansim_parcel.parcel.vacant_land_area'],
                                                                dataset_pool=dataset_pool)[index1]
    is_vacant = vacant_land>0
    #vacant_land = vacant_land*logical_or(parcels_glu==1, parcels_glu==2)                                                            
    is_developable_parcel = zeros(index1.size, dtype="int32")
    accepted_by_constraints = zeros(index1.size, dtype="int32")
    
    #parcels_to_template = {} 
    parcels_to_template_acc_by_constr = {}
    density_types = development_template_dataset['density_type']
    parcels_acc_by_constr_wo_templ = {}
    parcels_acc_by_constr = {}
    #pidx = parcel_dataset.get_id_index(804461)
    logger.start_block("Combine parcels, templates and constraints")
    for i_template in index2:
        this_template_id = template_ids[i_template]
        
        fit_indicator = ones(index1.size, dtype="bool8")
        parcels_to_template_acc_by_constr[this_template_id] = []
        this_templ_accepted_by_constraints = zeros(index1.size, dtype="int32")
        has_this_template = zeros(index1.size, dtype="int32")
        if has_constraint_dataset:
            generic_land_use_type_id = generic_land_use_type_ids[i_template]
            if generic_land_use_type_id not in parcels_acc_by_constr_wo_templ.keys():
                parcels_acc_by_constr_wo_templ[generic_land_use_type_id] = zeros(index1.size, dtype="int32")
            if generic_land_use_type_id not in parcels_acc_by_constr.keys():
                parcels_acc_by_constr[generic_land_use_type_id] = zeros(index1.size, dtype="int32")
            #if generic_land_use_type_id not in [1,2]:
            #    continue
            units_proposed = parcel_dataset.compute_variables(['psrc_parcel.parcel.units_proposed_for_template_%s' % this_template_id],
                                                                dataset_pool=dataset_pool)[index1]
            is_size_fit = parcel_dataset.compute_variables(['psrc_parcel.parcel.is_size_fit_for_template_%s' % this_template_id],
                                                                dataset_pool=dataset_pool)[index1]
            for constraint_type, constraint in parcel_dataset.development_constraints[generic_land_use_type_id].iteritems():
                if density_types[i_template] <> constraint_type:
                    continue
                template_attribute = development_template_dataset.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
                if template_attribute == 0:
                    continue
                min_constraint = constraint[:, 0].copy()
                max_constraint = constraint[:, 1].copy()
                ## treat -1 as unconstrained
                w_unconstr = min_constraint == -1
                if w_unconstr.any():
                    min_constraint[w_unconstr] = template_attribute
                
                w_unconstr = max_constraint == -1
                if w_unconstr.any():
                    max_constraint[w_unconstr] = template_attribute

                this_accepted_by_constraints = logical_and(template_attribute >= min_constraint,
                                                        template_attribute <= max_constraint)
                fit_indicator = logical_and(fit_indicator, 
                                            logical_and(logical_and(this_accepted_by_constraints, units_proposed > 0), is_size_fit))
                
                is_developable_parcel = logical_or(is_developable_parcel, max_constraint > 0)
                this_templ_accepted_by_constraints = logical_or(this_templ_accepted_by_constraints, 
                                                                logical_and(is_developable_parcel, 
                                                                            logical_and(this_accepted_by_constraints, units_proposed > 0)))
                has_this_template = logical_or(has_this_template, fit_indicator)
            accepted_by_constraints = logical_or(accepted_by_constraints, this_templ_accepted_by_constraints)
            has_template = logical_or(has_template, has_this_template)
            #parcels_to_template[this_template_id] = where(logical_and(vacant_land>0, 
            #                    logical_and(logical_and(is_developable_parcel, this_accepted_by_constraints),
            #                                logical_not(fit_indicator))))[0]
            #parcels_to_template_acc_by_constr[this_template_id].append(where(accepted_by_constraints)[0].tolist())
            not_accepted = logical_and(this_templ_accepted_by_constraints, logical_and(logical_not(has_this_template), is_vacant))
            parcels_to_template_acc_by_constr[this_template_id].append(where(not_accepted)[0].tolist())
            parcels_acc_by_constr_wo_templ[generic_land_use_type_id] = logical_or(parcels_acc_by_constr_wo_templ[generic_land_use_type_id], 
                                            not_accepted)
            parcels_acc_by_constr[generic_land_use_type_id] = logical_or(parcels_acc_by_constr[generic_land_use_type_id], 
                                                            logical_and(this_templ_accepted_by_constraints, is_vacant))
            #if fit_indicator[pidx]:
            #    print 'Parcel 804461: template %s accepted.' %  this_template_id
            
    logger.end_block()
    ### Print summary
    ##################
    unique_glu = parcels_acc_by_constr_wo_templ.keys()
    #parcels_wo_templ = zeros(index1.size, dtype="int32")
    
    #parcels_wo_templ = where(logical_and(vacant_land>0, logical_and(is_developable_parcel, logical_not(has_template))))[0]
    #nr_parcels_wo_templ = parcels_wo_templ.size
    #is_vacant = vacant_land>0
    #logger.log_status("\nGLU\tvacant land\tconstraint out\tno template")
    logger.log_status("\nGLU\tconsidered\tno template")
    no_glu_templ = []
    parcels_wo_temp_by_glu = {}
    sum1 = 0
    sum2 = 0
    parcels_wo_templ = logical_not(has_template)
    for glu in unique_glu:
        if strict:
            parcels_acc_by_constr_wo_templ[glu] = logical_and(parcels_acc_by_constr_wo_templ[glu], parcels_wo_templ)
        #if glu == 3:
        #parcels_wo_templ = logical_or(parcels_wo_templ, parcels_acc_by_constr_wo_templ[glu])
#        if glu not in generic_land_use_type_ids:
#            no_glu_templ.append(glu)
        #idx = parcels_glu==glu
#        if idx.sum() > 0:
#            logger.log_status("%s\t%7i\t\t%7i\t\t%7i" % (glu, is_vacant[idx].sum(), 
#                        is_vacant[idx].sum() - logical_and(is_vacant[idx], is_developable_parcel[idx]).sum(),
#                        logical_and(is_vacant[idx], logical_and(is_developable_parcel[idx], logical_not(has_template[idx]))).sum()))
#            parcels_wo_temp_by_glu[glu] = where(logical_and(idx, logical_and(is_vacant, 
#                                    logical_and(is_developable_parcel, logical_not(has_template)))))[0]
        logger.log_status("%s\t%7i\t\t%7i" % (glu, parcels_acc_by_constr[glu].sum(), parcels_acc_by_constr_wo_templ[glu].sum()))
        sum1 = sum1 + parcels_acc_by_constr[glu].sum()
        sum2 = sum2 + parcels_acc_by_constr_wo_templ[glu].sum()      
    logger.log_status("\nall\t%7i\t\t%7i" % (sum1, sum2))
    #if len(no_glu_templ) > 0:
    #    logger.log_status("\nNo templates for GLUs: %s" % no_glu_templ)
        
    ### Create plots
    #################
    
    templ_min_max = {}
    for glu in unique_glu:
        gidx = where(parcels_acc_by_constr_wo_templ[glu])[0]
        logger.start_block("Creating figures for GLU %s using %s parcels" % (glu,gidx.size))
        templ_min_max[glu] = []
        max_land_sqft = {'far': 0, 'units_per_acre': 0}
        min_land_sqft = {'far': 9999999, 'units_per_acre': 9999999}
        max_templ_attr = {'far': 0, 'units_per_acre': 0}
        min_templ_attr = {'far': 999999, 'units_per_acre': 9999999}
        xy = {'far':[], 'units_per_acre':[]}
        points = {'far':zeros((0,3)), 'units_per_acre':zeros((0,3))}
        npoints = {'far': 0, 'units_per_acre': 0}
        for i_template in index2:
            if glu <> generic_land_use_type_ids[i_template]:
                continue
            this_template_id = template_ids[i_template]
            #units_proposed = parcel_dataset['units_proposed_for_template_%s' % this_template_id]
            #is_size_fit = parcel_dataset['is_size_fit_for_template_%s' % this_template_id]
            #is_constraint = zeros(parcel_dataset.size(), dtype='bool8')
            #is_constraint[array(parcels_to_template_acc_by_constr[this_template_id])]=True
            #is_size_fit = logical_and(logical_and(logical_not(is_size_fit), 
            #                                      logical_and(is_vacant, units_proposed>0)), 
            #                          logical_and(is_constraint,
            #                                      is_developable_parcel))
            missed_to_match = zeros(parcel_dataset.size(), dtype='bool8')
            missed_to_match[(unique(array(parcels_to_template_acc_by_constr[this_template_id]).flatten())).astype('int32')] = True
            missed_to_match = where(logical_and(missed_to_match, parcels_acc_by_constr_wo_templ[glu]))[0]
            #missed_to_match = unique(array(parcels_to_template_acc_by_constr[this_template_id]).flatten())
            for constraint_type, constraint in parcel_dataset.development_constraints[glu].iteritems():
                if density_types[i_template] <> constraint_type:
                    continue
                template_attribute = development_template_dataset.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
                if template_attribute == 0:
                    continue
                templ_min_max[glu].append([development_template_dataset["land_sqft_min"][i_template], 
                                           development_template_dataset["land_sqft_max"][i_template]])
                xy[constraint_type] = xy[constraint_type] + [[development_template_dataset["land_sqft_min"][i_template], 
                            development_template_dataset["land_sqft_max"][i_template]], 
                            [template_attribute, template_attribute]]
                #if is_size_fit[gidx].sum() > 0:
                if missed_to_match.size > 0:
                    npoints[constraint_type] = npoints[constraint_type] + missed_to_match.size #is_size_fit[gidx].sum()
                    #if is_size_fit[gidx].sum() > 100:
                    if missed_to_match.size > 100:
                        draw = sample_noreplace(missed_to_match, 100)
                        thisidx = draw
                    else:
                        thisidx = missed_to_match
                    points[constraint_type] = concatenate((points[constraint_type], 
                                      concatenate((parcel_dataset['vacant_land_area'][thisidx][:,newaxis], 
                                                   template_attribute*ones((thisidx.size,1)), 
                                                   parcel_ids[thisidx][:,newaxis]), axis=1)), axis=0)
                    max_land_sqft[constraint_type] = max(max_land_sqft[constraint_type], parcel_dataset['vacant_land_area'][thisidx].max())
                    min_land_sqft[constraint_type] = min(min_land_sqft[constraint_type], parcel_dataset['vacant_land_area'][thisidx].max())
                    max_templ_attr[constraint_type] = max(max_templ_attr[constraint_type], template_attribute)
                    min_templ_attr[constraint_type] = min(min_templ_attr[constraint_type], template_attribute)

        import matplotlib.ticker as ticker
        import matplotlib.pyplot as plt
        def myexp(x, pos):
            return '%i' % (round(exp(x)))
        def myexp2(x, pos):
            return '%.2f' % (round(exp(x), 2))

        for type in ['far', 'units_per_acre']:
            if points[type].size == 0:
                continue
            #print xy[type]
            lxy = array(xy[type])
            dots = points[type][:,0:2]
            minx = min_land_sqft[type]-100
            maxx = max_land_sqft[type]+100
            miny = min_templ_attr[type]-0.05
            maxy = max_templ_attr[type]+0.05
            if log_scale:
                lxy = log(lxy)
                dots = log(dots)
                minx = log(minx)
                maxx = log(maxx)
                miny = log(miny)
                maxy = log(maxy)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            lines = ax.plot(*lxy) # template lines
            po = ax.plot(dots[:,0], dots[:,1]) # parcel points
            if log_scale:
                xformatter = ticker.FuncFormatter(myexp)
                yformatter = ticker.FuncFormatter(myexp2)
                ax.xaxis.set_major_formatter(xformatter)
                ax.yaxis.set_major_formatter(yformatter)
                # The following would be better but throws an error
                #locator = ticker.LogLocator(base=2.718282, subs=0.1)
                #ax.xaxis.set_major_locator(locator)
            plt.setp(lines, color='b', linewidth=1)
            plt.setp(po, marker='o', linestyle='None', linewidth=0)

            ax.axis([min(dots[:,0].min(), minx), 
                     max(dots[:,0].max(), maxx), 
                     min(dots[:,1].min(), miny), 
                     max(dots[:,1].max(), maxy)])
            plt.title('GLU: %s, units: %s, missing: %s' % (glu, type, npoints[type]))
            #ax.grid(True)
            plt.xlabel('land sqft range')
            plt.ylabel('density')
            log_suffix = ''
            if log_scale:
                log_suffix = '_log'
            plt.savefig(os.path.join(output_dir, 'match_templates%s_%s_%s.pdf' % (log_suffix, glu, type)))
            plt.close()
            #plt.show()
            if output_points:
            #if glu == 3:
                write_table_to_text_file(os.path.join(output_dir, 'points_%s_%s.txt' % (glu, type)), points[type], delimiter=', ')
        logger.end_block()

    logger.log_status('Resulting figures stored into %s' % output_dir)               
    return parcel_ids[index1][parcels_wo_templ]
    
class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage

    
if __name__ == '__main__':
    ### User's settings:
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_with_income_growth_NHoust/2000"
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_data/2000"
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/runs/run_bm_2.tmod1/2040"
    output_dir =  "/Users/hana/match_templ2" # where the resulting figures are going to be stored
    output_dir =  "/Users/hana/workspace/data/psrc_parcel/constraints"
    log_scale = True
    ### End of user's settings
    instorage = FltStorage().get(input_cache)
    dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=instorage)
    parcel_dataset = dataset_pool.get_dataset('parcel')
    development_templates = dataset_pool.get_dataset('development_template')
    res = match_parcels_to_constraints_and_templates(parcel_dataset, development_templates, output_dir=output_dir, 
                                                     log_scale=log_scale, strict=True, output_points=True, dataset_pool=dataset_pool)
    #write_to_text_file(os.path.join(output_dir, 'dev_parcels_wo_templ.txt'), res[0:100], delimiter='\n')
    