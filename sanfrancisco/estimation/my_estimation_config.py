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
from opus_core.database_management.database_configuration import DatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

my_configuration = {
     'cache_directory':r'e:/urbansim_cache/sanfrancisco/cache_source', ### TODO: Set this cache_directory to something useful.
    'input_configuration': DatabaseConfiguration(
        database_name = "sanfrancisco_baseyear",
        ),

    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['sanfrancisco', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),                          
    'output_configuration': DatabaseConfiguration(
        database_name = "sanfrancisco_baseyear_change_20080125",
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['sanfrancisco', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),     
    'datasets_to_cache_after_each_model':[],
    'base_year': 2001,
    'years': (2001,2001), 
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    "datasets_to_preload" : {
        'zone':{},
        'household':{},
        'building':{},        
        'parcel':{'package_name':'sanfrancisco'},
        'business':{'package_name':'sanfrancisco'},
        'person':{'package_name':'sanfrancisco'},        
        "building_use":{'package_name':'sanfrancisco'},
        "building_use_classification":{'package_name':'sanfrancisco'},
        'travel_data':{},
        'urbansim_constant':{}
        }
}

    
