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
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

from sanfrancisco.configs.baseline import Baseline


class SynthesizerConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = [
#        'business',
        'households',
        'buildings',
        'parcels',
        'zones',
#        "households_for_estimation"
        ]
        
        return {
        'cache_directory' : r'/home/lmwang/work/sf/cache_source_0125', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_mysql = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'/urbansim_cache/sanfrancisco/cache_source',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_copy_to_previous_years = {},                                          
            ),
        'input_configuration': DatabaseConfiguration(
            database_name = 'sanfrancisco_baseyear_start',
            ),
        'output_configuration': DatabaseConfiguration(
            database_name = 'sanfrancisco_baseyear_change_20080121',
            ),            
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['sanfrancisco', 'urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'base_year': 2001,
        }

    
