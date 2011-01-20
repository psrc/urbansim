# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

#from opus_core.misc import get_host_name
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.base_config_zone import tables_to_cache
#from urbansim.configs.base_config_zone import run_configuration
from urbansim.configs.cache_baseyear_configuration import CacheBaseyearConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


cache_configuration = CacheBaseyearConfiguration()
my_cache_config = CreatingBaseyearCacheConfiguration(
        cache_directory_root = '/tmp/urbcache/sandbox_runs/zones',
        unroll_gridcells = True,
        cache_from_database = True,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/urbansim_cache/psrc_zone',
            years_to_cache = range(1996,2000),
            ),
        tables_to_cache = tables_to_cache().get_tables_to_cache(),
        tables_to_cache_nchunks = {
            'gridcells':5,
            },
    )
cache_configuration['creating_baseyear_cache_configuration'] = my_cache_config
my_configuration = {
    'remove_cache': False, # remove cache after finishing the simulation
    'cache_directory': '/urbansim_cache/psrc_zone', ### TODO: Set this cache_directory to something useful.
    'creating_baseyear_cache_configuration': cache_configuration['creating_baseyear_cache_configuration'],
    'input_configuration': DatabaseConfiguration(
        database_name = 'PSRC_2000_estimation_zone_pwaddell', #change
        ),                      
    'base_year':2000,
    'years':(2001, 2002),
    'seed':1,#(1,1),
    }