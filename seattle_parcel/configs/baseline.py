# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.configuration import Configuration
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
import os

class Baseline(UrbansimParcelConfiguration):
    multiple_runs = False

    def __init__(self):
        opus_home = os.environ['OPUS_HOME']
        config = UrbansimParcelConfiguration()
        config_changes = {
            'project_name':'seattle_parcel',
            'description':'Seattle parcel baseline',
            'cache_directory':  os.path.join(opus_home, 'data/seattle_parcel/base_year_data'),
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
            cache_directory_root = os.path.join(opus_home, 'data/seattle_parcel/runs'),
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    years_to_cache = [2000],
                    existing_cache_to_copy = r'/Users/borning/opus_home/data/seattle_parcel/base_year_data',
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'households',
                    'persons',
                    'buildings',
                    'parcels',
                    'gridcells',
                    'zones',
                    "jobs",
                    "households_for_estimation",
                    "jobs_for_estimation",
                    "development_event_history",
                    "travel_data",
                    "building_types",
                    "job_building_types",
                    'urbansim_constants',
                    "target_vacancies",
                    "home_based_employment_location_choice_model_coefficients",
                    "home_based_employment_location_choice_model_specification",
                    "non_home_based_employment_location_choice_model_coefficients",
                    "non_home_based_employment_location_choice_model_specification",
                    "household_location_choice_model_coefficients",
                    "household_location_choice_model_specification",
                    "real_estate_price_model_coefficients",
                    "real_estate_price_model_specification",
                    "annual_household_control_totals",
                    "annual_relocation_rates_for_households",
                    "household_characteristics_for_ht",
                    "annual_employment_control_totals",
                    "annual_relocation_rates_for_jobs",
                    "land_use_types",
                    "generic_land_use_types",
                    'employment_sectors',
                    'employment_adhoc_sector_groups',
                    'employment_adhoc_sector_group_definitions',
                    'development_templates',
                    'development_template_components',
                    'development_constraints',
                    "building_sqft_per_job",
                    "fazes",
                    "large_areas",
                    "demolition_cost_per_sqft",
                    'constant_taz_columns'
                    ],
                tables_to_cache_nchunks={'parcels': 1},
                unroll_gridcells = False
                ),
            'scenario_database_configuration': ScenarioDatabaseConfiguration(
                database_name = 'seattle_2000_parcel_baseyear_data',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                ),

            'base_year':2000,
            'years':(2001, 2006),
            'models':[ # models are executed in the same order as in this list
                #"process_pipeline_events",
                "real_estate_price_model",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "household_transition_model",
                "employment_transition_model",
                "household_relocation_model",
                "household_location_choice_model",
                "employment_relocation_model",
                {"employment_location_choice_model":{'group_members': '_all_'}},
                'distribute_unplaced_jobs_model'
                ],
            'models_in_year': {2000: [ # This is not run anymore, since all jobs are located and only a few households are not.
                 "household_relocation_model_for_2000",
                "household_location_choice_model_for_2000",
                "employment_relocation_model_for_2000",
                {"employment_location_choice_model":{'group_members': '_all_'}}
                                       ]
                                       },
                'flush_dataset_to_cache_after_each_model':False,
                'flush_variables':False,
                'low_memory_run':False,
                'datasets_to_cache_after_each_model':["parcel", "building", 'household', 'job',
                                                      'development_project_proposal_component',  #to be cached for diagnostic purpose (lmwang)
                                                      'development_project_proposal', 'travel_data'],
                'unroll_gridcells':False,
                "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building':{},
                    'parcel':{'package_name':'urbansim_parcel'},
                    'person':{'package_name':'urbansim_parcel'},
                    'development_template': {'package_name':'urbansim_parcel'},
                    'development_template_component': {'package_name':'urbansim_parcel'},
                    'job':{},
                    "building_type":{'package_name':'urbansim_parcel'},
                    'travel_data':{},
                    "job_building_type":{}
                }
        }
        config.replace(config_changes)

        config['models_configuration']["household_location_choice_model"]["controller"]["import"] = \
                {"psrc_parcel.models.household_location_choice_model" : "HouseholdLocationChoiceModel"}
        config['models_configuration']["employment_location_choice_model"]['controller']["import"] = \
                {"psrc_parcel.models.employment_location_choice_model" : "EmploymentLocationChoiceModel"}
        config['models_configuration']["home_based_employment_location_choice_model"]['controller']["import"] = \
                {"psrc_parcel.models.employment_location_choice_model" : "EmploymentLocationChoiceModel"}
        config['models_configuration']['household_relocation_model_for_2000'] = {}
        config['models_configuration']['household_relocation_model_for_2000']['controller'] = \
                    HouseholdRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               probabilities = None,
                               rate_table=None,
                               output_index = 'hrm_index').execute()
        config['models_configuration']['household_location_choice_model_for_2000'] = Configuration(
                                   config['models_configuration']['household_location_choice_model']
                                                                                                   )
        config['models_configuration']['household_location_choice_model_for_2000']['controller']['run']['arguments']['chunk_specification'] = "{'nchunks':1}"
        config['models_configuration']['household_location_choice_model_for_2000']['controller']['run']['arguments']['maximum_runs'] = 1
        config['models_configuration']['employment_relocation_model_for_2000'] = {}
        config['models_configuration']['employment_relocation_model_for_2000']['controller'] = \
                    EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               probabilities = None,
                               rate_table=None,
                               output_index = 'erm_index').execute()

        if self.multiple_runs:
            from multiple_runs_modification import MultipleRunsModification
            MultipleRunsModification().modify_configuration(config)

        self.merge(config)