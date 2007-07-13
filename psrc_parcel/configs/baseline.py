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
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.resources import merge_resources_with_defaults
from numpy import array
import os

class Baseline(UrbansimParcelConfiguration):
    def __init__(self):
        config = AbstractUrbansimConfiguration()

        config_changes = {
            'description':'PSRC parcel baseline',
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
            cache_directory_root = r'/Users/lmwang/urbansim_cache/psrc_parcel',
            #cache_directory_root = r'/workspace/urbansim_cache/psrc_parcel',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'/Users/lmwang/urbansim_cache/psrc_parcel/cache_source',
                    #existing_cache_to_copy = r'/workspace/urbansim_cache/psrc_parcel/estimation',
                    ),
                cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
                tables_to_cache = [
                    #'business',
                    'households',
                    'buildings',
                    'parcels',
                    'zones',
                    "jobs",
                    "households_for_estimation",
                    "jobs_for_estimation",
                    "development_event_history",
                    #"persons",
                    "travel_data",
                    "building_types",
                    "job_building_types",
                    'urbansim_constants',
                    "target_vacancies",
                    "home_based_employment_location_choice_model_coefficients",
                    "home_based_employment_location_choice_model_coefficients",
                    "non_home_based_employmen_location_choice_model_specification",
                    "non_home_based_employmen_location_choice_model_specification",
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
                    ],
                tables_to_cache_nchunks={'parcels': 1},
                unroll_gridcells = False
                ),
            'input_configuration': DatabaseConfiguration(
                host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
                user_name     = os.environ.get('MYSQLUSERNAME',''),
                password      = "urbo?!sauR", #os.environ.get('MYSQLPASSWORD',''),
                database_name = 'psrc_2005_parcel_baseyear',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
#            'models_configuration':models_configuration,

            'base_year':2000,
            'years':(2001, 2002),
            'models':[ # models are executed in the same order as in this list
#                "process_pipeline_events",
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
                ],

                'flush_dataset_to_cache_after_each_model':False,
                'flush_variables':False,
                'low_memory_run':False,
                'datasets_to_cache_after_each_model':["parcel", "building"],
                'unroll_gridcells':False,
                "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building':{},
                    'parcel':{'package_name':'urbansim_parcel'},
                    'development_template': {'package_name':'urbansim_parcel'},
                    'development_template_component': {'package_name':'urbansim_parcel'},
                    'job':{},
#                    'person':{'package_name':'urbansim_parcel'},        
                    "building_type":{'package_name':'urbansim_parcel'},
                    'travel_data':{},

                }
        }
        #use configuration in config as defaults and merge with config_changes
#        config = merge_resources_with_defaults(config_changes, config)
        config.replace(config_changes)
        self.merge(config)

