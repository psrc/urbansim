# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.hlcm_estimation_config import run_configuration as config
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


my_configuration_general = {
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'washtenaw_class',
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = 'washtenaw_estimation_output',
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_directory':'/urbansim_cache/workshop/washtenaw_estimation', # change or leave out
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
        unroll_gridcells = True,
        cache_from_database = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/urbansim_cache/workshop/cache_source',
            #years_to_cache = range(1996,2001),
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
            'employment_sectors',
            'plan_types',
            'race_names',
            'target_vacancies',
            'jobs_for_estimation',
            'households_for_estimation',
            'development_events_exogenous',
            'job_building_types',
            ],
        tables_to_cache_nchunks = {'gridcells':1},
        tables_to_copy_to_previous_years = {},
        ),
    'base_year':2000,
    'years':(2000,2000),
}

my_configuration = config.copy()

hlcm_controller = my_configuration["models_configuration"]["household_location_choice_model"]["controller"]

hlcm_controller["estimate"]["arguments"]["procedure"] = "'biogeme.mnl_estimation'"

my_configuration["models_configuration"]["household_location_choice_model"]["controller"].merge(hlcm_controller)
my_configuration.merge(my_configuration_general)