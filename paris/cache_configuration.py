# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

from opus_core.configuration import Configuration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

class CacheConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = [
        'neighborhoods',
        'households',
        'jobs',
        #'gridcells',
        #'travel_data',
        #'zones',
        'urbansim_constants'
        ]
        
        return {
        'cache_directory' : r'/aalborg1/lmwang/urbansim_cache/paris/', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_database = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'/urbansim_cache/cache_source',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_copy_to_previous_years = {},                                          
            ),
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            database_name = 'paris_estimation',
            ),
        'estimation_database_configuration': EstimationDatabaseConfiguration(
            database_name = '',
            ),            
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['paris', 'urbansim', 'opus_core'],
            ),
        'base_year': 2000,
        }

    
