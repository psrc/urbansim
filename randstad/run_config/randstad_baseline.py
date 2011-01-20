# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

#from urbansim.estimation.config import config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

from randstad.run_config.controller_config import models_configuration


run_configuration = AbstractUrbansimConfiguration()
my_run_configuration = {    
    'models_configuration':models_configuration,
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'randstad_021105_estimation',
        ),
    #'cache_directory':'C:/urbansim_cache/randstad_source',
    'cache_directory':None, ### TODO: Set this cache_directory to something useful.
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        cache_directory_root = 'C:/urbansim_cache/randstad',
        cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
        unroll_gridcells = False,
        cache_from_database = False,
        # location of existing baseyear cache to use
        baseyear_cache = BaseyearCacheConfiguration( 
            existing_cache_to_copy = r'C:\urbansim_cache\randstad\run_618.2006_07_16_18_06',
            years_to_cache = [1995],
            ),
        tables_to_cache = [
            'annual_employment_control_totals', 
            'annual_household_control_totals', 
            'development_event_history', 
            'gridcells', 
            'households', 
            'jobs', 
            'travel_data', 
            'zones', 
            'counties', 
    #        'commercial_development_location_choice_model_coefficients', 
    #        'commercial_development_location_choice_model_specification', 
            'employment_commercial_location_choice_model_coefficients', 
            'employment_commercial_location_choice_model_specification', 
            'employment_home_based_location_choice_model_coefficients', 
            'employment_home_based_location_choice_model_specification', 
            'employment_industrial_location_choice_model_coefficients', 
            'employment_industrial_location_choice_model_specification', 
    #        'industrial_development_location_choice_model_coefficients', 
    #        'industrial_development_location_choice_model_specification', 
    #        'residential_development_location_choice_model_coefficients', 
    #        'residential_development_location_choice_model_specification', 
            'landuse_development_location_choice_model_coefficients',
            'landuse_development_location_choice_model_specification',
    #        'fazes',
            'rings',
            'urbansim_constants', 
            'household_location_choice_model_coefficients', 
            'household_location_choice_model_specification', 
            'land_price_model_coefficients', 
            'land_price_model_specification', 
            'housing_price_model_coefficients', 
            'housing_price_model_specification', 
            'residential_land_share_model_specification', 
    #        'plan_type_group_definitions', 
    #        'plan_type_groups', 
    #        'large_areas', 
            'household_characteristics_for_ht', 
            'development_types', 
            'transition_types', 
            'development_type_group_definitions', 
            'development_constraints', 
            'annual_relocation_rates_for_households', 
            'annual_relocation_rates_for_jobs', 
            'base_year', 
            'cities', 
            'development_events', 
            'development_type_groups', 
            'employment_adhoc_sector_group_definitions', 
            'employment_adhoc_sector_groups', 
            'employment_events', 
            'employment_location_choice_model_coefficients', 
            'employment_location_choice_model_specification', 
            'employment_sectors', 
            'household_characteristics_for_hlc', 
            'land_use_events', 
            'plan_types', 
            'race_names', 
            'residential_land_share_model_coefficients', 
            'target_vacancies', 
            'development_event_frequency',
            'development_filters',
            'development_event_template',
            ],
        tables_to_cache_nchunks = {},
        tables_to_copy_to_previous_years = {},
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['randstad', 'urbansim', 'opus_core'],
        ),
    "base_year":1995,
    'years':(1996, 2005), 
    'seed':1,#(1,1),
    'models':[ # models are executed in the same order as in this list 
        "prescheduled_events",
        "events_coordinator", 
        #"residential_land_share_model",
        "housing_price_model", 
        "development_transition_model",
        "landuse_development_location_choice_model",  
        "development_event_transition_model",
        "events_coordinator", 
        #"residential_land_share_model",
        "household_transition_model",
        "employment_transition_model",
        "household_relocation_model", 
        "household_location_choice_model",
        "employment_relocation_model", "divide_jobs_model",
#       "employment_home_based_location_choice_model",
        "employment_commercial_location_choice_model", 
        "employment_industrial_location_choice_model",
        "scaling_jobs_model", 
        ],
    'debuglevel':120, 
    'flush_dataset_to_cache_after_each_model':True,
    'flush_variables':False,
    'low_memory_run':True,
    'datasets_to_cache_after_each_model':[ # datasets to be cached after each model, 
        'gridcell',       # if 'flush_dataset_to_cache_after_each_model' is True
        'household',
        'job'],
    'datasets_to_preload': { # Datasets that should be loaded before each year, e.g. in order to pass them as model arguments.
        'gridcell':{         # All remaining datasets are used via SessionConfiguration
            },               # linked to the cache.
        'household':{
            },
        'job':{
            },
        'zone':{
            },
        'development_type':{},
        'development_group':{},                            
        'target_vacancy':{},
        'development_event_history':{},
        'development_filter':{'package_name':'randstad'},
        'development_event_template':{'package_name':'randstad'},
        'development_event_frequency':{'package_name':'randstad'},
        },  
    }

run_configuration.merge(my_run_configuration)

run_configuration['models_configuration']["household_location_choice_model"]['controller']['run']['arguments']['chunk_specification'] = "{'nchunks':1}"

from opus_core.tests import opus_unittest
if __name__ == '__main__':
    class ConfigTests(opus_unittest.OpusTestCase):
        def test_merge(self):
            self.assertEqual(run_configuration['base_year'], 1995)
            
            
    opus_unittest.main()