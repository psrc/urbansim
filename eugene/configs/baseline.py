# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


class Baseline(AbstractUrbansimConfiguration):
    """Eugene's baseline configuration.
    """
    def __init__(self):
        AbstractUrbansimConfiguration.__init__(self)
        
        config_changes = {
            'project_name':'eugene_gridcell',
            'description':'Eugene baseline',
            'base_year':1980,
            'years':(1981, 1982),
            'models': [   
                'prescheduled_events',
                'events_coordinator',
                'residential_land_share_model',
                'land_price_model',
                'development_project_transition_model',
                'residential_development_project_location_choice_model',
                'commercial_development_project_location_choice_model',
                'industrial_development_project_location_choice_model',
                'development_event_transition_model',
                'events_coordinator',
                'residential_land_share_model',
                'household_transition_model',
                'employment_transition_model',
                'household_relocation_model',
                'household_location_choice_model',
                'employment_relocation_model',
                {   'employment_location_choice_model': {   'group_members': '_all_'}},
                'distribute_unplaced_jobs_model',
                ],
            'scenario_database_configuration': ScenarioDatabaseConfiguration(database_name = 'eugene_1980_baseyear'),
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_gridcell/runs'),
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = os.path.join(os.environ['OPUS_HOME'], 'data/eugene_gridcell/base_year_data'),
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
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
                    #'fazes',
                    'urbansim_constants',
                    'household_location_choice_model_coefficients',
                    'household_location_choice_model_specification',
                    'land_price_model_coefficients',
                    'land_price_model_specification',
                    'residential_land_share_model_coefficients',
                    'residential_land_share_model_specification',
                    #'plan_type_group_definitions',
                    #'plan_type_groups',
                    #'large_areas',
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
                    'employment_sectors',
                    'plan_types',
                    'plan_type_groups',
                    'plan_type_group_definitions',                    
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    'households_for_estimation',
                    #'development_events_exogenous',
                    ],
                tables_to_cache_nchunks = {'gridcells': 1},
                tables_to_copy_to_previous_years = {
                    'development_type_group_definitions': 1975,
                    'development_type_groups': 1975,
                    'development_types': 1975,
                    'development_constraints':1975,
                    'urbansim_constants': 1975,
                    },
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['eugene', 'urbansim', 'opus_core'],
                ),
            }
        self.merge(config_changes)
        