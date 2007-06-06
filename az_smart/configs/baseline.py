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
from opus_core.configurations.database_configuration import DatabaseConfiguration
from az_smart.configs.controller_config import models_configuration
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
            'description':'AZ-SMART baseline',
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                #cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
               cache_directory_root = r'/urbansim_cache/az_smart',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    #existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
                   existing_cache_to_copy = r'/workspace/urbansim_cache/az_smart/estimation',
                    ),                
                cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
                tables_to_cache = [
                    #'business',
                    #'households',
                    'buildings',
                    'parcels',
                    #'zones',
                    #"households_for_estimation",
                    #"business_for_estimation",
                    #"development_event_history",
                    #"persons",
                    #"travel_data",
                    #"annual_relocation_rates_for_business",
##                    "buildings_for_estimation",
                    #"building_types",
                    #"generic_building_types",
                    #'urbansim_constants',
                    #"target_vacancies",
                    #"business_location_choice_model_coefficients",
                    #"business_location_choice_model_specification",
                    #"household_location_choice_model_coefficients",
                    #"household_location_choice_model_specification",
                    #"housing_price_model_coefficients",
                    #"housing_price_model_specification",
                    #"nonresidential_building_location_choice_model_coefficients",
                    #"nonresidential_building_location_choice_model_specification",
                    #"real_estate_price_model_coefficients",
                    #"real_estate_price_model_specification",
                    #"residential_building_location_choice_model_coefficients",
                    #"residential_building_location_choice_model_specification",
                    #"annual_household_control_totals",
                    #"annual_relocation_rates_for_households",
                    #"household_characteristics_for_ht",
                    #"annual_business_control_totals",
                    #"annual_relocation_rates_for_business",
                    #"development_project_proposals",
                    #"land_use_types",
                    #'employment_sectors',
                    #'employment_adhoc_sector_groups',
                    #'employment_adhoc_sector_group_definitions',
                    #'development_templates',
                    #'development_template_components',
                    #'development_constraints',
                    ],  
                tables_to_cache_nchunks={'parcels': 1},
                unroll_gridcells = False
                ),           
            'input_configuration': DatabaseConfiguration(
                host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
                user_name     = os.environ.get('MYSQLUSERNAME',''),
                password      = os.environ.get('MYSQLPASSWORD',''),
                database_name = 'az_smart_baseyear',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['az_smart', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),                          
            'models_configuration':models_configuration,
            
            'base_year':2000,
            'years':(2006, 2006),
            'models':[ # models are executed in the same order as in this list 
#                "process_pipeline_events",
                "real_estate_price_model",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
#                "building_transition_model",
#                {'building_location_choice_model': {'group_members': '_all_'}},
#                "household_transition_model",
#                "business_transition_model",
#                "household_relocation_model", 
#                "household_location_choice_model",
#                "business_relocation_model", 
#                "business_location_choice_model",        
                ],

                'flush_dataset_to_cache_after_each_model':False,
                'flush_variables':False,
                'low_memory_run':False,
                'datasets_to_cache_after_each_model':["parcel", "building"],
#                'unroll_gridcells':False            
                "datasets_to_preload":{
#                    'zone':{},
#                    'household':{},
                    'building':{},        
                    'parcel':{'package_name':'az_smart'},
#                    'development_template': {'package_name':'az_smart'},
#                    'development_template_component': {'package_name':'az_smart'},
#                    'business':{'package_name':'az_smart'},
#                    'person':{'package_name':'az_smart'},        
                    "building_type":{'package_name':'az_smart'},
#                    'travel_data':{},
                    
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
#                    'parcel':{'package_name':'az_smart'},
#                    'business':{'package_name':'az_smart'},
#                    'person':{'package_name':'az_smart'},        
#                    "building_use":{'package_name':'az_smart'},
#                    "building_use_classification":{'package_name':'az_smart'},
#                    'travel_data':{},
#                    'target_vacancy':{},
#                    'development_event_history':{}
#                    
#        }
 
