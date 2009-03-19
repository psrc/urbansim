# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from numpy import array

from opus_core.configuration import Configuration

from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


# This configuration contains all of the information needed for the code
# to know how to process the desired range of development projects.
# This should be globally accessible, so that models and datasets
# can know what flavors of development projects exist.
class CacheBaseyearConfiguration(Configuration):
    """Specifies additional information needed just for caching the baseyear data.
    
    These values over-ride values in the base configuration, via the .merge 
    method.  
    
    To make this class concrete, you need to specify the db_input_database 
    containing the name of the input database."""
    def __init__(self):
        my_config = self._get_initial_config()
        Configuration.__init__(self, my_config)
    
    def _get_initial_config(self):
        """Encapsulate dirty inner workings"""
        config = {
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                tables_to_cache = [
                    # tables needed for a standard set of UrbanSim models
                    'annual_employment_control_totals',
                    'annual_household_control_totals',
                    'development_event_history',
                    'gridcells',
                    'households',
                    'job_building_types',
                    'jobs',
                    'travel_data',
                    'zones',
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
                    'household_characteristics_for_ht',
                    'development_types',
                    'development_type_group_definitions',
                    'development_constraints',
                    'annual_relocation_rates_for_households',
                    'annual_relocation_rates_for_jobs',
                    'base_year',
                    'development_events',
                    'development_type_groups',
                    'employment_adhoc_sector_group_definitions',
                    'employment_adhoc_sector_groups',
                    'employment_sectors',
                    'plan_types',
                    'race_names',
                    'target_vacancies',
                    'development_events_exogenous',
                    #
                    # tables not needed for a standard set of medels
                    'jobs_for_estimation',
                    'households_for_estimation',
                    'counties',
                    'cities',
                    'large_areas',
                    'buildings',
                    'building_types',
                    'persons'
                    ],
                tables_to_cache_nchunks = {'gridcells':1},
                tables_to_copy_to_previous_years = {},
                ),
            'debuglevel':4,
            #'chunk_specification':{ # Default value
                #'nchunks':1,
                #},
            }
        
        return config