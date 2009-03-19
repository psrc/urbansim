# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

#from urbansim.estimation.config import config
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from pag_parcel.configs.controller_config import models_configuration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

class Baseline(GeneralConfiguration):
    def __init__(self):
        config = AbstractUrbansimConfiguration()

        config_changes = {
            'project_name':'pag_parcel',
            'description':'PAG parcel baseline',
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
            #cache_directory_root = r'/workspace/urbansim_cache/pag_parcel',
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
           #existing_cache_to_copy = r'/workspace/urbansim_cache/pag_parcel/estimation',
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'business',
                    'households',
                    'buildings',
                    'parcels',
                    'zones',
                    "jobs",
                    "households_for_estimation",
                    "business_for_estimation",
                    "development_event_history",
                    "persons",
                    "travel_data",
                    "annual_relocation_rates_for_business",
                    "annual_relocation_rates_for_jobs",
#                    "buildings_for_estimation",
                    "building_types",
                    "job_building_types",
                    "generic_building_types",
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
                    "development_project_proposals",
                    "land_use_types",
                    'employment_sectors',
                    'employment_adhoc_sector_groups',
                    'employment_adhoc_sector_group_definitions',
                    'development_templates',
                    'development_template_components',
                    'development_constraints',
                    ],
                tables_to_cache_nchunks={'parcels': 1},
                unroll_gridcells = False
                ),
            'scenario_database_configuration': ScenarioDatabaseConfiguration(
                database_name = 'pag_parcel_baseyear',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['pag_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                ),
            'models_configuration':models_configuration,

            'base_year':2005,
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
                    'zone':{},
#                    'household':{},
                    'building':{},
                    'parcel':{'package_name':'urbansim_parcel'},
                    'development_template': {'package_name':'urbansim_parcel'},
                    'development_template_component': {'package_name':'urbansim_parcel'},
#                    'business':{'package_name':'urbansim_parcel'},
#                    'person':{'package_name':'urbansim_parcel'},        
                    "building_type":{'package_name':'urbansim_parcel'},
                    'travel_data':{},

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
#                    'parcel':{'package_name':'urbansim_parcel'},
#                    'business':{'package_name':'urbansim_parcel'},
#                    'person':{'package_name':'urbansim_parcel'},        
#                    "building_use":{'package_name':'urbansim_parcel'},
#                    "building_use_classification":{'package_name':'urbansim_parcel'},
#                    'travel_data':{},
#                    'target_vacancy':{},
#                    'development_event_history':{}
#
#        }

