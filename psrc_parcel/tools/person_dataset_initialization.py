# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

from psrc.config.wlcm_config import run_configuration

    
run_configuration["models"] = [
    "household_person_consistency_keeper",
    "home_based_choice_model",
    "home_based_workplace_choice_model",
    "workplace_location_choice_model_for_resident"
    ]

#run_configuration["models_configuration"]['household_location_choice_model']['controller']['run']['arguments']['agents_index']=None
config_changes = {                   
    'creating_baseyear_cache_configuration':{
        'cache_from_database': False,
        'cache_directory_root':r'/projects/urbansim7/urbansim_cache/psrc', #'/projects/urbansim7/urbansim_cache/psrc',
        'baseyear_cache':{
            'existing_cache_to_copy':r'/projects/urbansim7/urbansim_cache/psrc/wlcm_initialization_source',
            'years':list(range(2000,2001))
            },
     "tables_to_cache":[
                     "persons",
                     "home_based_choice_model_coefficients",
                     "home_based_choice_model_specification",
                     "home_based_workplace_choice_model_coefficients",
                     "home_based_workplace_choice_model_specification",
                     "workplace_location_choice_model_for_resident_specification",
                     "workplace_location_choice_model_for_resident_coefficients",
                     "workplace_location_choice_model_for_immigrant_specification",
                     "workplace_location_choice_model_for_immigrant_coefficients",                     
                     ],                                          
        'unroll_gridcells':False,
        'tables_to_cache_nchunks': {
                    'gridcells':4,
                    },
        },

    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'GSPSRC_2000_baseyear_change_20060924_wlcm_init',
        ),

    'datasets_to_cache_after_each_model':['person'],
    'low_memory_mode':True,
    'base_year': 2000,
    'years': (2001,2001),
    "datasets_to_preload": {
        'gridcell': {},
        'job': {},                                            
        'person': {'package_name':'psrc'},
        'zone': {},
        'household': {},
        }
    }

from urbansim.simulation.run_simulation import RunSimulation
from urbansim.model_coordinators.model_system import ModelSystem

if __name__ == "__main__":
    simulation = RunSimulation()
    run_configuration.merge(config_changes)
    simulation.prepare_and_run(run_configuration, 
                               simulation_instance=ModelSystem(),
                               remove_cache=False)