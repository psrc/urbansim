# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.misc import unique, DebugPrinter, write_to_text_file, quantile, write_table_to_text_file
from opus_core.logger import logger
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.sampling_toolbox import sample_noreplace
from numpy import arange, where, resize, zeros, array, logical_and, logical_or, logical_not, concatenate, ones, log, concatenate, newaxis, exp, maximum, minimum, floor, round_, float64
from scipy.ndimage import histogram
import os

def units_proposed_as_in_model(template_dataset, i_template, vacant_land, lc, parcel_sqft, is_inside_ugb, mol=0.1):
    """Units proposed by template i_template on the given parcels, computed as in the development proposals:
    land area taken as in urbansim_parcel.development_project_proposal.land_area_taken,
    usable ratio as the minimum of the constraint lot coverage lc (in %) and 100 - percent_land_overhead of the template,
    units rounded as in urbansim_parcel.development_project_proposal.units_proposed,
    plus one unit per legal lot for non-FAR templates as in
    psrc_parcel.development_project_proposal.units_proposed_plus_minimum_1DU_per_legal_lot_yield.
    """
    land_min = template_dataset['land_sqft_min'][i_template]
    land_max = template_dataset['land_sqft_max'][i_template]
    density = template_dataset['density'][i_template]
    density_type = template_dataset['density_type'][i_template]
    land_area_taken = floor(vacant_land.astype(float64))
    land_area_taken[land_area_taken < land_min] = 0
    land_area_taken[land_area_taken >= land_max * (1 + mol)] = int(land_max)
    usable_ratio = minimum(lc, 100 - template_dataset['percent_land_overhead'][i_template]) / 100.0
    if density_type == 'units_per_lot':
        fraction = density * ones(vacant_land.size)
    else:
        density_convertor = 1 / 43560.0 if density_type == 'units_per_acre' else 1.0
        fraction = land_area_taken * usable_ratio * density * density_convertor
    units = round_(fraction)
    if density_type != 'far':
        is_legal_lot = logical_or(logical_and(parcel_sqft > 9999, logical_not(is_inside_ugb)),
                                  logical_and(parcel_sqft > 3499, is_inside_ugb))
        units = units + logical_and(logical_and(fraction > 0, fraction <= 0.5), is_legal_lot)
    return units


def match_parcels_to_constraints_and_templates(parcel_dataset,
                                                development_template_dataset,
                                                output_dir, log_scale=True, strict=False, strict_res_nonres=True, 
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
    If strict_res_nonres is True, split the "strictness" only between residential and non-residential.
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
        development_template_dataset.compute_variables(["%s.%s" % (template_opus_path, x) for x in constraint_types], dataset_pool)
            
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
    parcel_sqft = parcel_dataset['parcel_sqft'][index1]
    is_inside_ugb = parcel_dataset['is_inside_urban_growth_boundary'][index1].astype("bool8")
    #vacant_land = vacant_land*logical_or(parcels_glu==1, parcels_glu==2)                                                            
    is_developable_parcel = zeros(index1.size, dtype="int32")
    accepted_by_constraints = zeros(index1.size, dtype="int32")
    
    #parcels_to_template = {} 
    parcels_to_template_acc_by_constr = {}
    density_types = development_template_dataset['density_type']
    parcels_acc_by_constr_wo_templ = {}
    parcels_acc_by_constr = {}
    def glu_to_restype(glu):
        if glu in [1, 2]:
            return ["residential"]
        if glu in [3, 4, 5]:
            return ["non-residential"]
        if glu == 6:
            return ["residential", "non-residential"]
        return []
    has_template_by_restype = {"residential": zeros(index1.size, dtype="bool8"),
                               "non-residential": zeros(index1.size, dtype="bool8")}
    
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
            if generic_land_use_type_id not in list(parcels_acc_by_constr_wo_templ.keys()):
                parcels_acc_by_constr_wo_templ[generic_land_use_type_id] = zeros(index1.size, dtype="int32")
            if generic_land_use_type_id not in list(parcels_acc_by_constr.keys()):
                parcels_acc_by_constr[generic_land_use_type_id] = zeros(index1.size, dtype="int32")
            #if generic_land_use_type_id not in [1,2]:
            #    continue
            is_size_fit = parcel_dataset.compute_variables(['psrc_parcel.parcel.is_size_fit_for_template_%s' % this_template_id],
                                                                dataset_pool=dataset_pool)[index1]
            for constraint_type, constraint in parcel_dataset.development_constraints[generic_land_use_type_id].items():
                if density_types[i_template] != constraint_type:
                    continue
                template_attribute = development_template_dataset.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
                if template_attribute == 0:
                    continue
                min_constraint = constraint[:, 0].copy()
                max_constraint = constraint[:, 1].copy()
                units_proposed = units_proposed_as_in_model(development_template_dataset, i_template, vacant_land,
                                                            constraint[:, 2], parcel_sqft, is_inside_ugb)
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
            for restype in glu_to_restype(generic_land_use_type_id):
                has_template_by_restype[restype] = logical_or(has_template_by_restype[restype], has_this_template)
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
    unique_glu = list(parcels_acc_by_constr_wo_templ.keys())
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
    # parcels accepted by constraints for some GLU of the res type, but without any template of that res type
    parcels_acc_by_constr_wo_templ_by_restype = {"residential": zeros(index1.size, dtype="bool8"),
                                                 "non-residential": zeros(index1.size, dtype="bool8")}
    for glu in unique_glu:
        if strict_res_nonres:
            for restype in glu_to_restype(glu):
                parcels_acc_by_constr_wo_templ_by_restype[restype] = logical_or(parcels_acc_by_constr_wo_templ_by_restype[restype],
                                                                    logical_and(parcels_acc_by_constr_wo_templ[glu], 
                                                                                logical_not(has_template_by_restype[restype])))
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
    if strict_res_nonres:
        for restype in ["residential", "non-residential"]:
            logger.log_status("%s without template: %7i" % (restype, parcels_acc_by_constr_wo_templ_by_restype[restype].sum()))
    
    if strict_res_nonres:
        parcels_wo_templ_all = zeros(index1.size, dtype='bool8')
        for dentyp in ["residential", "non-residential"]:
            parcels_wo_templ_all = logical_or(parcels_wo_templ_all, parcels_acc_by_constr_wo_templ_by_restype[dentyp])
    elif strict:
        parcels_wo_templ_all = zeros(index1.size, dtype='bool8')
        for glu in unique_glu:
            parcels_wo_templ_all = logical_or(parcels_wo_templ_all, parcels_acc_by_constr_wo_templ[glu])
    else:
        parcels_wo_templ_all = parcels_wo_templ
    
    #if len(no_glu_templ) > 0:
    #    logger.log_status("\nNo templates for GLUs: %s" % no_glu_templ)
        
    ### Create plots
    #################
    
    # plot groups: label -> (GLUs whose templates are drawn, parcels without template)
    plot_groups = {}
    if strict_res_nonres:
        for restype in ["residential", "non-residential"]:
            plot_groups[restype] = ([glu for glu in unique_glu if restype in glu_to_restype(glu)],
                                    parcels_acc_by_constr_wo_templ_by_restype[restype])
    else:
        for glu in unique_glu:
            plot_groups[glu] = ([glu], parcels_acc_by_constr_wo_templ[glu])

    templ_min_max = {}
    for group, (group_glus, group_wo_templ) in plot_groups.items():
        gidx = where(group_wo_templ)[0]
        logger.start_block("Creating figures for %s (GLU %s) using %s parcels" % (group, group_glus, gidx.size))
        templ_min_max[group] = []
        max_land_sqft = {'far': 0, 'units_per_acre': 0, 'units_per_lot': 0}
        min_land_sqft = {'far': 9999999, 'units_per_acre': 9999999, 'units_per_lot': 9999999}
        max_templ_attr = {'far': 0, 'units_per_acre': 0, 'units_per_lot': 0}
        min_templ_attr = {'far': 999999, 'units_per_acre': 9999999, 'units_per_lot': 9999999}
        xy = {'far':[], 'units_per_acre':[], 'units_per_lot':[]}
        points = {'far':zeros((0,3)), 'units_per_acre':zeros((0,3)), 'units_per_lot':zeros((0,3))}
        npoints = {'far': 0, 'units_per_acre': 0, 'units_per_lot': 0}
        for i_template in index2:
            glu = generic_land_use_type_ids[i_template]
            if glu not in group_glus:
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
            missed_to_match = zeros(index1.size, dtype='bool8')
            missed_to_match[(unique(array(parcels_to_template_acc_by_constr[this_template_id]).flatten())).astype('int32')] = True
            missed_to_match = where(logical_and(missed_to_match, group_wo_templ))[0]
            #missed_to_match = unique(array(parcels_to_template_acc_by_constr[this_template_id]).flatten())
            for constraint_type, constraint in parcel_dataset.development_constraints[glu].items():
                if density_types[i_template] != constraint_type:
                    continue
                template_attribute = development_template_dataset.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
                if template_attribute == 0:
                    continue
                templ_min_max[group].append([development_template_dataset["land_sqft_min"][i_template], 
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
                                      concatenate((vacant_land[thisidx][:,newaxis], 
                                                   template_attribute*ones((thisidx.size,1)), 
                                                   parcel_ids[index1][thisidx][:,newaxis]), axis=1)), axis=0)
                    max_land_sqft[constraint_type] = max(max_land_sqft[constraint_type], vacant_land[thisidx].max())
                    min_land_sqft[constraint_type] = min(min_land_sqft[constraint_type], vacant_land[thisidx].min())
                    max_templ_attr[constraint_type] = max(max_templ_attr[constraint_type], template_attribute)
                    min_templ_attr[constraint_type] = min(min_templ_attr[constraint_type], template_attribute)

        import matplotlib.ticker as ticker
        import matplotlib.pyplot as plt
        def myexp(x, pos):
            return '%i' % (round(exp(x)))
        def myexp2(x, pos):
            return '%.2f' % (round(exp(x), 2))

        for type in ['far', 'units_per_acre', 'units_per_lot']:
            if len(xy[type]) == 0: # no templates of this type
                continue
            #print xy[type]
            lxy = array(xy[type])
            dots = points[type][:,0:2]
            has_points = dots.shape[0] > 0
            if log_scale:
                lxy = log(lxy)
                dots = log(maximum(dots, 1e-3)) # avoid log(0) for parcels with (almost) no vacant land
            fig = plt.figure()
            ax = fig.add_subplot(111)
            lines = ax.plot(*lxy) # template lines
            po = ax.plot(dots[:,0], dots[:,1]) # parcel points (possibly none)
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

            # show the whole range of template lines (rows of lxy alternate x and y pairs) and parcel points
            allx = lxy[0::2].ravel()
            ally = lxy[1::2].ravel()
            if has_points:
                allx = concatenate((allx, dots[:,0]))
                ally = concatenate((ally, dots[:,1]))
            xmin, xmax = allx.min(), allx.max()
            ymin, ymax = ally.min(), ally.max()
            xmargin = max(0.02*(xmax - xmin), 0.1) # non-zero margin also if there is a single value
            ymargin = max(0.02*(ymax - ymin), 0.1)
            ax.axis([xmin - xmargin, xmax + xmargin, ymin - ymargin, ymax + ymargin])
            if strict_res_nonres:
                plt.title('%s, units: %s, missing: %s' % (group, type, npoints[type]))
            else:
                plt.title('GLU: %s, units: %s, missing: %s' % (group, type, npoints[type]))
            #ax.grid(True)
            plt.xlabel('land sqft range')
            plt.ylabel('density')
            log_suffix = ''
            if log_scale:
                log_suffix = '_log'
            plt.savefig(os.path.join(output_dir, 'match_templates%s_%s_%s.pdf' % (log_suffix, group, type)))
            plt.close()
            #plt.show()
            if output_points:
            #if glu == 3:
                write_table_to_text_file(os.path.join(output_dir, 'points_%s_%s.txt' % (group, type)), points[type], delimiter=', ')
        logger.end_block()

    logger.log_status('Resulting figures stored into %s' % output_dir)               
    return parcel_ids[index1][parcels_wo_templ_all]
    
class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage

    
if __name__ == '__main__':
    ### User's settings:
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_with_income_growth_NHoust/2000"
    #input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_data/2000"
    #input_cache =  "/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_73.run_2016_06_06/2014_match_cache"
    input_cache =  "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/run_55.2026_10_14_11_01_unlimited/2023devtempl"
    output_data_points = False # If true a text files are created that contain the x and y of the points in the figures
    #output_dir =  "/Users/hana/match_templ2" # where the resulting figures are going to be stored
    #output_dir =  "/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_73.run_2016_06_06/match_output"
    output_dir =  "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/run_55.2026_10_14_11_01_unlimited/match_output"
    log_scale = True
    ### End of user's settings
    instorage = FltStorage().get(input_cache)
    dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=instorage)
    parcel_dataset = dataset_pool.get_dataset('parcel')
    development_templates = dataset_pool.get_dataset('development_template')
    res = match_parcels_to_constraints_and_templates(parcel_dataset, development_templates, output_dir=output_dir, 
                    log_scale=log_scale, strict=False, strict_res_nonres=True, output_points=output_data_points, dataset_pool=dataset_pool)
    write_to_text_file(os.path.join(output_dir, 'dev_parcels_wo_templ.txt'), res, delimiter='\n')
    pass