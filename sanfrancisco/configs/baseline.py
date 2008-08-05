#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

#from urbansim.estimation.config import config
from opus_core.database_management.database_configuration import DatabaseConfiguration
from sanfrancisco.configs.controller_config import models_configuration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.resources import merge_resources_with_defaults
from numpy import array
import os

class Baseline(GeneralConfiguration):
    def __init__(self):
        config = AbstractUrbansimConfiguration()
        
        config_changes = {
            'project_name':'sanfrancisco',
            'description':'San Francisco baseline',
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'e:/urbansim_cache/sanfrancisco',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'e:/urbansim_cache/sanfrancisco/cache_source',
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
            'input_configuration': DatabaseConfiguration(
                database_name = 'sanfrancisco_baseyear_flattened',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['sanfrancisco', 'urbansim', 'opus_core'],
                package_order_exceptions={},
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
 
