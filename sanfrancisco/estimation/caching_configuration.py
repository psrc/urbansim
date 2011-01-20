# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.configuration import Configuration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


class CachingConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = ['business',
            'households',
            'buildings',
            'development_event_history',
            'target_vacancies',
            'annual_household_control_totals',
            'annual_business_control_totals',
            'annual_relocation_rates_for_business',
            'annual_relocation_rates_for_households',
            'household_characteristics_for_ht',
            'parcels',
            'zones',
            "tracts",
            "households_for_estimation",
            "business_for_estimation",
            "persons",
            "travel_data",
            "annual_relocation_rates_for_business",
            "buildings_for_estimation",
            "building_use",
            "building_use_classification",
            'urbansim_constants'
        ]
        
        return {
        'cache_directory' : r'/urbansim_cache/sanfrancisco/cache_source', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_database = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'/urbansim_cache/sanfrancisco/cache_source',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_copy_to_previous_years = {},                                          
            ),
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            database_name = 'sanfrancisco_baseyear',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['sanfrancisco', 'urbansim', 'opus_core'],
            ),
        'base_year': 2001,
        }

    