# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.configuration import Configuration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

from psrc.configs.baseline import Baseline


class UrbbuildCachingConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = Baseline()['creating_baseyear_cache_configuration'].tables_to_cache
        tables_to_cache.append('workers_for_estimation')
        
        return {
        'cache_directory' : 'D:/urbansim_cache/psrc/estimation', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = True,
            cache_from_database = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'D:/urbansim_cache/full_psrc',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_cache_nchunks = {
                'parcels':4,
                'gridcells':5
                },
            tables_to_copy_to_previous_years = {},                                          
            ),
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            database_name = 'GSPSRC_2000_baseyear_change_20070102',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['psrc', 'urbansim', 'opus_core'],
            ),
        'base_year': 2000,
        }

    