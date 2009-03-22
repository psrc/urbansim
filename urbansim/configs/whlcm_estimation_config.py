# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config
"""estimation config for HLCM with worker specific accessibility"""

run_configuration = config.copy()

estimation_configuration = {}
estimation_configuration["models"] = [
    #{"land_price_model": ["run"]},                                      
    {"household_relocation_model": ["run"]},
    {"worker_specific_household_location_choice_model": ["estimate"]}
]

estimation_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'household':{},
        'person':{'package_name':'psrc'}
        }

run_configuration.merge(estimation_configuration)

#add persons to tables_to_cache
run_configuration["creating_baseyear_cache_configuration"].tables_to_cache += ["persons"]

run_configuration["models_configuration"]["worker_specific_household_location_choice_model"] = \
    run_configuration["models_configuration"]["household_location_choice_model"].copy()
    
controller = run_configuration["models_configuration"]["worker_specific_household_location_choice_model"]["controller"]                              
controller["init"]["arguments"]["submodel_string"] = "'psrc.household.nonhome_based_workers_category'"
#the persons set must have all persons in both the households and households_for_estimation
controller["prepare_for_estimate"]["arguments"]["join_datasets"] = False  
run_configuration["models_configuration"]["worker_specific_household_location_choice_model"]["controller"].merge(controller)
