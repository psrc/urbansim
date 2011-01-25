# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.misc import unique, DebugPrinter, write_to_text_file
from opus_core.logger import logger
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import arange, where, resize, zeros, array, logical_and, logical_or, logical_not, concatenate, ones
import os

def match_parcels_to_constraints_and_templates(parcel_dataset,
                                                development_template_dataset,
                                                parcel_index=None,
                                                template_index=None,
                                                consider_constraints_as_rules=True,
                                                template_opus_path="urbansim_parcel.development_template",
                                                dataset_pool=None,
                                                resources=None):
    """
    This function matches parcels to their constraints and templates and gives a summary about how many parcels had no match.
    parcel_index - 1D array, indices of parcel_dataset (default is all parcels).
    template_index - index to templates that are available (default is all templates).
    """

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
    #vacant_land = vacant_land*logical_or(parcels_glu==1, parcels_glu==2)                                                            
    is_developable_parcel = zeros(index1.size, dtype="int32")
    logger.start_block("Combine parcels, templates and constraints")
    for i_template in index2:
        this_template_id = template_ids[i_template]
        fit_indicator = ones(index1.size, dtype="bool8")
        if has_constraint_dataset:
            generic_land_use_type_id = generic_land_use_type_ids[i_template]
            #if generic_land_use_type_id not in [1,2]:
            #    continue
            units_proposed = parcel_dataset.compute_variables(['psrc_parcel.parcel.units_proposed_for_template_%s' % this_template_id],
                                                                dataset_pool=dataset_pool)[index1]
            for constraint_type, constraint in parcel_dataset.development_constraints[generic_land_use_type_id].iteritems():
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

                fit_indicator = logical_and(fit_indicator, 
                                            logical_and(logical_and(template_attribute >= min_constraint,
                                                        template_attribute <= max_constraint), units_proposed > 0))
                
                is_developable_parcel = logical_or(is_developable_parcel, max_constraint > 0)
                
            has_template = logical_or(has_template, fit_indicator)
    logger.end_block()
    parcels_wo_templ = where(logical_and(vacant_land>0, logical_and(is_developable_parcel, logical_not(has_template))))[0]
    nr_parcels_wo_templ = parcels_wo_templ.size
    is_vacant = vacant_land>0
    logger.log_status("\nGLU\tvacant land\tconstraint out\tno template")
    no_glu_templ = []
    unique_glu = unique(parcels_glu)
    for glu in unique_glu:
        if glu not in generic_land_use_type_ids:
            no_glu_templ.append(glu)
        idx = parcels_glu==glu
        if idx.size > 0:
            logger.log_status("%s\t%7i\t\t%7i\t\t%7i" % (glu, is_vacant[idx].sum(), 
                        is_vacant[idx].sum() - logical_and(is_vacant[idx], is_developable_parcel[idx]).sum(),
                        logical_and(is_vacant[idx], logical_and(is_developable_parcel[idx], logical_not(has_template[idx]))).sum()))                            
    logger.log_status("\nall\t%7i\t\t%7i\t\t%7i" % (is_vacant.sum(), is_vacant.sum() - logical_and(is_vacant, is_developable_parcel).sum(),
                          nr_parcels_wo_templ))
    if len(no_glu_templ) > 0:
        logger.log_status("\nNo templates for GLUs: %s" % no_glu_templ)
    return parcels_wo_templ
    
class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage

    
if __name__ == '__main__':
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/base_year_with_income_growth_NHoust/2000"
    output_dir =  "/Users/hana" # where the output file is going to be written
    instorage = FltStorage().get(input_cache)
    dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=instorage)
    parcel_dataset = dataset_pool.get_dataset('parcel')
    development_templates = dataset_pool.get_dataset('development_template')
    res = match_parcels_to_constraints_and_templates(parcel_dataset, development_templates, dataset_pool=dataset_pool)
    #write_to_text_file(os.path.join(output_dir, 'dev_parcels_wo_templ'), res, delimiter='\n')
    