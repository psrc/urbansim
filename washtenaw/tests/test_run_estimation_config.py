#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os

from opus_core.configuration import Configuration
from opus_core.database_management.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from urbansim.configs.base_config_zone import tables_to_cache
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

class TestRunEstimationConfig(Configuration):
    def __init__(self):
        Configuration.__init__(self, data = {
            'input_configuration':DatabaseConfiguration(
                database_name = "washtenaw_class",
                ),
            'datasets_to_cache_after_each_model':[],
            'low_memory_mode':False,
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                unroll_gridcells = True,
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = '/urbansim_cache/workshop/cache_source',
                    #years_to_cache  = range(1996,2001)
                    ),
                tables_to_cache = [
                    'annual_employment_control_totals',
                    'annual_household_control_totals',
                    'buildings',
                    'building_types',
                    'development_event_history',
                    'gridcells',
                    'households',
                    'job_building_types',
                    'jobs',
                    'travel_data',
                    'zones',
                    'counties',
                    'commercial_development_location_choice_model_coefficients',
                    'commercial_development_location_choice_model_specification',
                    'commercial_employment_location_choice_model_coefficients',
                    'commercial_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_specification',
                    'industrial_development_location_choice_model_coefficients',
                    'industrial_development_location_choice_model_specification',
                    'residential_development_location_choice_model_coefficients',
                    'residential_development_location_choice_model_specification',
                    'fazes',
                    'urbansim_constants',
                    'household_location_choice_model_coefficients',
                    'household_location_choice_model_specification',
                    'land_price_model_coefficients',
                    'land_price_model_specification',
                    'residential_land_share_model_coefficients',
                    'residential_land_share_model_specification',
                    'plan_type_group_definitions',
                    'plan_type_groups',
                    'large_areas',
                    'household_characteristics_for_ht',
                    'development_types',
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
                    'employment_sectors',
                    'land_use_events',
                    'plan_types',
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    'households_for_estimation',
                    'development_events_exogenous',
                    'job_building_types'
                    ],
                tables_to_cache_nchunks = {'gridcells':1},
                tables_to_copy_to_previous_years = {
                    'development_type_group_definitions':1995,
                    'development_type_groups':1995,
                    'development_types':1995,
                    'development_constraints':1995,
                    'urbansim_constants':1995,
                    },
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['washtenaw', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            'base_year': 2000,
            'years': (2000,2000),
            })