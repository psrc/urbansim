#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.configuration import Configuration
from opus_core.database_management.database_configuration import DatabaseConfiguration
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
            cache_from_mysql = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'/urbansim_cache/cache_source',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_copy_to_previous_years = {},                                          
            ),
        'input_configuration': DatabaseConfiguration(
            database_name = 'paris_estimation',
            ),
        'output_configuration': DatabaseConfiguration(
            database_name = '',
            ),            
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['paris', 'urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'base_year': 2000,
        }

    
