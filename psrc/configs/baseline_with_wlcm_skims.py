# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.storage_factory import StorageFactory
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

from psrc.config.wlcm_config import run_configuration as config
from opus_core.database_management.database_server import DatabaseServer

db_server = DatabaseServer(ScenarioDatabaseConfiguration())
db = db_server.get_database('PSRC_2000_baseyear')
        
config_changes = {
    'description':'baseline with wlcm and skims',
    'in_storage':StorageFactory().get_storage('sql_storage',
            storage_location = db
                ),
    'cache_directory':None, ### TODO: Set this cache_directory to something useful.
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        cache_directory_root = 'd:/urbansim_cache',
        unroll_gridcells = True,
        cache_from_database = True,
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
            'job_building_types',
            'persons',
            'workplace_choice_model_for_resident_specification',
            'workplace_choice_model_for_resident_coefficients',
            'workplace_choice_model_for_immigrant_specification',
            'workplace_choice_model_for_immigrant_coefficients'
            ],
        tables_to_cache_nchunks = {'gridcells': 4},
        tables_to_copy_to_previous_years = {},
        ),
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'PSRC_2000_baseyear',
        ),
    'base_year':2000,
    'years':(2001, 2003),
    }
run_configuration = config.copy()    
run_configuration.merge(config_changes)

from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc', mode='skims')
run_configuration['travel_model_configuration'] = travel_model_configuration