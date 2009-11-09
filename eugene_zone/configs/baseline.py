# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

from urbansim_zone.configs.controller_config import UrbansimZoneConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

class Baseline(UrbansimZoneConfiguration):
    """Eugene's baseline configuration for runs on zonal level.
    """
    def __init__(self):
        UrbansimZoneConfiguration.__init__(self)
        
        config_changes = {
            'project_name':'eugene_zone',
            'description':'Eugene zone baseline',
            'base_year':1980,
            'years':(1981, 1985),
            'debuglevel': 4,
            'models': [
                'real_estate_price_model',
                'development_project_transition_model',
                'commercial_development_project_location_choice_model',
                'industrial_development_project_location_choice_model',
                'residential_development_project_location_choice_model',
                'add_projects_to_buildings',
                'household_transition_model',
                'employment_transition_model',
                'household_relocation_model',
                'household_location_choice_model',
                'employment_relocation_model',
                {   'employment_location_choice_model': {   'group_members': '_all_'}},
                'distribute_unplaced_jobs_model',
                ],
            'scenario_database_configuration': ScenarioDatabaseConfiguration(database_name = 'eugene_1980_baseyear_zone'),
            'cache_directory': os.path.join(os.environ['OPUS_HOME'], 'data/eugene_zone/base_year_data'),
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_zone/runs'),
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_zone/base_year_data')
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    'annual_employment_control_totals',
                    'annual_household_control_totals',
                    'households',
                    'job_building_types',
                    'building_types',
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
                    'annual_relocation_rates_for_households',
                    'annual_relocation_rates_for_jobs',
                    'base_year',
                    'cities',
                    'development_event_history',
                    'employment_adhoc_sector_group_definitions',
                    'employment_adhoc_sector_groups',
                    'employment_sectors',
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    'households_for_estimation',
                    ],
                unroll_gridcells= False
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['eugene_zone', 'eugene', 'urbansim_zone', 'urbansim', 'opus_core'],
                ),
            }
        self.merge(config_changes)
        
