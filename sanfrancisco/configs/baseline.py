# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim.estimation.config import config
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from sanfrancisco.configs.controller_config import models_configuration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
import os

class Baseline(GeneralConfiguration):
    def __init__(self):
        config = AbstractUrbansimConfiguration()
        
        config_changes = {
            'project_name':'sanfrancisco',
            'description':'San Francisco baseline',
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'/Volumes/Data/opus/data/sanfrancisco/runs',
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'/Volumes/Data/opus/data/sanfrancisco/base_year_data',
                    ),                
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'business',
                    'households',
                    'buildings',
                    'parcels',
                    'zones',
                    "households_for_estimation",
                    "business_for_estimation",
                    "development_event_history",
                    "persons",
                    "travel_data",
                    "annual_relocation_rates_for_business",
#                    "buildings_for_estimation",
                    "building_use",
                    "building_use_classification",
                    'urbansim_constants',
                    "target_vacancies",
                    "business_location_choice_model_coefficients",
                    "business_location_choice_model_specification",
                    "household_location_choice_model_coefficients",
                    "household_location_choice_model_specification",
                    "housing_price_model_coefficients",
                    "housing_price_model_specification",
                    "nonresidential_building_location_choice_model_coefficients",
                    "nonresidential_building_location_choice_model_specification",
                    "real_estate_price_model_coefficients",
                    "real_estate_price_model_specification",
                    "residential_building_location_choice_model_coefficients",
                    "residential_building_location_choice_model_specification",
                    "annual_household_control_totals",
                    "annual_relocation_rates_for_households",
                    "household_characteristics_for_ht",
                    "annual_business_control_totals",
                    "annual_relocation_rates_for_business",
                    'development_event_history',
                    "development_events_exogenous",
                    "district24",
                    "district14",
                    "tracts",
                    "sectors"
                    ],  
                tables_to_cache_nchunks={'parcels': 1},
                unroll_gridcells = False
                ),           
            'scenario_database_configuration': ScenarioDatabaseConfiguration(
                database_name = 'sanfrancisco_baseyear_flattened',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['sanfrancisco', 'urbansim', 'opus_core'],
                ),                          
            'models_configuration':models_configuration,
            
            'base_year':2001,
            'years':(2002, 2030),
            'models':[ # models are executed in the same order as in this list 
                "process_pipeline_events",
                "real_estate_price_model",
                "building_transition_model",
                {'building_location_choice_model': {'group_members': '_all_'}},
                "household_transition_model",
                "business_transition_model",
                "household_relocation_model", 
                "household_location_choice_model",
                "business_relocation_model", 
                "business_location_choice_model",        
                ],

                'flush_dataset_to_cache_after_each_model':False,
                'flush_variables':False,
                'low_memory_run':False,
                'datasets_to_cache_after_each_model':[],
#                'unroll_gridcells':False            
                "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building':{},        
                    'parcel':{'package_name':'sanfrancisco'},
                    'business':{'package_name':'sanfrancisco'},
                    'person':{'package_name':'sanfrancisco'},        
                    "building_use":{'package_name':'sanfrancisco'},
                    "building_use_classification":{'package_name':'sanfrancisco'},
                    'travel_data':{},
                    'target_vacancy':{},
                    'development_event_history':{}
                    
                }
        }
        #use configuration in config as defaults and merge with config_changes
#        config = merge_resources_with_defaults(config_changes, config)
        config.replace(config_changes)
        self.merge(config)
#        self["datasets_to_preload"] = {
#                    'zone':{},
#                    'household':{},
#                    'building':{},        
#                    'parcel':{'package_name':'sanfrancisco'},
#                    'business':{'package_name':'sanfrancisco'},
#                    'person':{'package_name':'sanfrancisco'},        
#                    "building_use":{'package_name':'sanfrancisco'},
#                    "building_use_classification":{'package_name':'sanfrancisco'},
#                    'travel_data':{},
#                    'target_vacancy':{},
#                    'development_event_history':{}
#                    
#        }
 
