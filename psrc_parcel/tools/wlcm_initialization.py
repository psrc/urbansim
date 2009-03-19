# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from psrc.config.wlcm_config import run_configuration

    
run_configuration["models"] = [
    {"workplace_location_choice_model_for_resident": ["run"]}
    ]

#run_configuration["models_configuration"]['household_location_choice_model']['controller']['run']['arguments']['agents_index']=None
config_changes = {
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'PSRC_2000_baseyear',
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = 'GSPSRC_2000_baseyear_change_200609021',
        ),
    'datasets_to_cache_after_each_model':['person'],
    'low_memory_mode':True,
    'creating_baseyear_from_cache':{
        'cache_directory':'/projects/urbansim7/urbansim_cache/psrc',
        'cache_from_database':True,
        'tables_to_cache':[
            'gridcells',
            'households',
            'jobs',
            'travel_data',
            'zones',
            'persons',
            'workplace_location_choice_model_for_resident_coefficients',
            'workplace_location_choice_model_for_resident_specification',
            #'household_location_choice_model_coefficients',
            #'household_location_choice_model_specification',        
            #'employment_adhoc_sector_group_definitions',
            #'employment_adhoc_sector_groups',
            #'employment_sectors',
            #'development_types',
            #'development_type_groups',
            #'development_type_group_definitions',
            #'race_names'
            ],
        'tables_to_cache_nchunks':{
            'gridcells':4,
            },
        'unroll_gridcells':False,
        },
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
                               remove_cache=True)