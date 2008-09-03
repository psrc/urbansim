#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

from urbansim_zone.configs.controller_config import UrbansimZoneConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


class Baseline(UrbansimZoneConfiguration):
    """Eugene's baseline configuration for runs on zonal level.
    """
    def __init__(self):
        UrbansimZoneConfiguration.__init__(self)
        
        config_changes = {
            'project_name':'eugene_zone',
            'description':'Eugene zone baseline',
            'base_year':1980,
            'years':(1981, 1982),
            'models': [
                'real_estate_price_model',
                'household_transition_model',
                'employment_transition_model',
                'household_relocation_model',
                'household_location_choice_model',
                'employment_relocation_model',
                {   'employment_location_choice_model': {   'group_members': '_all_'}},
                'distribute_unplaced_jobs_model',
                ],
            'scenario_database_configuration': ScenarioDatabaseConfiguration(database_name = 'eugene_1980_baseyear_zone'),

            #'cache_directory':'c:/opusworkspace/eugene',
            'cache_directory':'/Users/hana/urbansim_cache/eugene/baseyear_cache_zone',
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = '/Users/hana/urbansim_cache/eugene/zone',
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = '/Users/hana/urbansim_cache/eugene/baseyear_cache_zone'
                    #existing_cache_to_copy = 'c:/urbansim_cache/eugene_1980_baseyear_cache',
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'annual_employment_control_totals',
                    'annual_household_control_totals',
                    'households',
                    'job_building_types',
                    'jobs',
                    'travel_data',
                    'zones',
                    'pseudo_buildings',
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
                    #'fazes',
                    'urbansim_constants',
                    'household_location_choice_model_coefficients',
                    'household_location_choice_model_specification',
                    'household_characteristics_for_ht',
                    'development_types',
                    'development_type_group_definitions',
                    'development_constraints',
                    'annual_relocation_rates_for_households',
                    'annual_relocation_rates_for_jobs',
                    'base_year',
                    'cities',
                    #'development_events',
                    'development_type_groups',
                    'employment_adhoc_sector_group_definitions',
                    'employment_adhoc_sector_groups',
                    'employment_events',
                    'employment_sectors',
                    #'land_use_events',
                    'plan_types',
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    'households_for_estimation',
                    #'development_events_exogenous',
                    ],
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['eugene_zone', 'eugene', 'urbansim_zone', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            }
        self.merge(config_changes)
        