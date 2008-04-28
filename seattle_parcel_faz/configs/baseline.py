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

from opus_core.database_management.database_configuration import DatabaseConfiguration
from opus_core.configuration import Configuration
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.resources import merge_resources_with_defaults
from numpy import array
import os

class Baseline(UrbansimParcelConfiguration):
    multiple_runs = False

    def __init__(self):
        config = UrbansimParcelConfiguration()
        config_changes = {
            'description':'Seattle parcel baseline',
            'cache_directory':None,
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
            cache_directory_root = r'c:/opus/data/seattle_parcel/runs',
            #cache_directory_root = '/Users/hana/urbansim_cache/seattle',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    years_to_cache = [2000],
                    #existing_cache_to_copy = '/Users/hana/urbansim_cache/seattle/seattle_parcel_2000_cache'
                    existing_cache_to_copy = r'c:/opus/data/seattle_parcel/base_year_data',
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'households',
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
            'input_configuration': DatabaseConfiguration(
                database_name = 'seattle_2000_parcel_baseyear_data',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['seattle_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),

            'base_year':2000,
            'years':(2001, 2002),
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
        config['models_configuration']["development_proposal_choice_model"]["controller"]["import"] = \
                {"seattle_parcel_faz.models.regional_development_proposal_sampling_model" : "RegionalDevelopmentProposalSamplingModel"}
        config['models_configuration']["development_proposal_choice_model"]["controller"]["init"]["name"] = \
                "RegionalDevelopmentProposalSamplingModel"
        config['models_configuration']["employment_transition_model"]["controller"]["import"] = \
                {"seattle_parcel_faz.models.regional_employment_transition_model" : "RegionalEmploymentTransitionModel"}
        config['models_configuration']["employment_transition_model"]["controller"]["init"]["name"] = \
                "RegionalEmploymentTransitionModel"
        config['models_configuration']["household_transition_model"]["controller"]["import"] = \
                {"seattle_parcel_faz.models.regional_household_transition_model" : "RegionalHouseholdTransitionModel"}
        config['models_configuration']["household_transition_model"]["controller"]["init"]["name"] = \
                "RegionalHouseholdTransitionModel"
        config['models_configuration']["household_location_choice_model"]["controller"]["import"] = \
                {"seattle_parcel_faz.models.regional_household_location_choice_model" : "RegionalHouseholdLocationChoiceModel"}
        config['models_configuration']["household_location_choice_model"]["controller"]["init"]["name"] = \
                "RegionalHouseholdLocationChoiceModel"
        config['models_configuration']["employment_location_choice_model"]['controller']["import"] = \
                {"seattle_parcel_faz.models.regional_employment_location_choice_model" : "RegionalEmploymentLocationChoiceModel"}
        config['models_configuration']["employment_location_choice_model"]["controller"]["init"]["name"] = \
                "RegionalEmploymentLocationChoiceModel"
        config['models_configuration']["home_based_employment_location_choice_model"]['controller']["import"] = \
                {"seattle_parcel_faz.models.regional_employment_location_choice_model" : "RegionalEmploymentLocationChoiceModel"}
        config['models_configuration']["home_based_employment_location_choice_model"]["controller"]["init"]["name"] = \
                "RegionalEmploymentLocationChoiceModel"
        config['models_configuration']["distribute_unplaced_jobs_model"]["controller"]["import"] = \
                {"seattle_parcel_faz.models.regional_distribute_unplaced_jobs_model" : "RegionalDistributeUnplacedJobsModel"}
        config['models_configuration']["distribute_unplaced_jobs_model"]["controller"]["init"]["name"] = \
                "RegionalDistributeUnplacedJobsModel"
        if self.multiple_runs:
            from multiple_runs_modification import MultipleRunsModification
            MultipleRunsModification().modify_configuration(config)

        self.merge(config)