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
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

my_configuration = {
     'cache_directory':r'/aalborg1/lmwang/urbansim_cache/paris/', ### TODO: Set this cache_directory to something useful.
    'input_configuration': DatabaseConfiguration(
        database_name = "paris_estimation",
        ),

    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['paris', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),                          
    'output_configuration': DatabaseConfiguration(
        database_name = "",
        ),
    'datasets_to_cache_after_each_model':[],
    'base_year': 2000,
    'years': (2000,2000), 
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    "datasets_to_preload" : {
#        'zone':{},
        'household':{},
        'neighborhood':{},
        'job':{},
        }
}

    
