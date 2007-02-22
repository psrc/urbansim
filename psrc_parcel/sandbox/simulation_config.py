#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import os

#from opus_core.misc import get_host_name
from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.base_config_zone import tables_to_cache
#from urbansim.configs.base_config_zone import run_configuration
from urbansim.configs.cache_baseyear_configuration import CacheBaseyearConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


cache_configuration = CacheBaseyearConfiguration()
my_cache_config = CreatingBaseyearCacheConfiguration(
        cache_directory_root = '/tmp/urbcache/sandbox_runs/zones',
        unroll_gridcells = True,
        cache_from_mysql = True,
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
        host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
        user_name     = os.environ.get('MYSQLUSERNAME',''),
        password      = os.environ.get('MYSQLPASSWORD',''),
        database_name = 'PSRC_2000_estimation_zone_pwaddell', #change
        ),                      
    'base_year':2000,
    'years':(2001, 2002),
    'seed':(1,1),
    }