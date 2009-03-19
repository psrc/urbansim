# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

from opus_core.storage_factory import StorageFactory
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.database_management.database_server import DatabaseServer


config = AbstractUrbansimConfiguration()
db_server = DatabaseServer(ScenarioDatabaseConfiguration())
db = db_server.get_database('PSRC_2000_baseyear')

config_changes = {
    'description':'simulation with elcm only',
    'in_storage':StorageFactory().get_storage('sql_storage',
            storage_location = db
                ),
    'cache_directory':None, ### TODO: Set this cache_directory to something useful.
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        cache_directory_root = 'd:/urbansim_cache',
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
        tables_to_cache_nchunks = {'gridcells': 1},
        tables_to_copy_to_previous_years = {},
        ),
    'scenario_database_configuration': ScenarioDatabaseConfiguration(
        database_name = 'PSRC_2000_baseyear',
        ),
    'base_year':2000,
    'years':(2001, 2030),
    'models':[
#        'household_relocation_model', 
#        'household_location_choice_model',
#        'employment_transition_model',
        'employment_relocation_model', 
        'home_based_employment_location_choice_model',
        'commercial_employment_location_choice_model', 
        'industrial_employment_location_choice_model',
#        'scaling_jobs_model', 
#        'land_price_model', 
#        'development_project_transition_model',
#        'residential_development_project_location_choice_model', 
#        'commercial_development_project_location_choice_model',
#        'industrial_development_project_location_choice_model', 
#        'residential_land_share_model', 
#        'development_event_transition_model',
#        'household_transition_model'
        ],
    }
run_configuration = config.copy()  
del run_configuration['models']
run_configuration.merge(config_changes)