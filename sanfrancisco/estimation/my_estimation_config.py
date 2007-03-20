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
from opus_core.configurations.database_configuration import DatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

my_configuration = {
     'cache_directory':r'/urbansim_cache/sanfrancisco/estimation', ### TODO: Set this cache_directory to something useful.
     'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
#           cache_directory_root = 'd:/urbansim_cache/sanfrancisco',
        cache_from_mysql = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = r'/urbansim_cache/sanfrancisco/cache_source',
            ),                
        cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
        unroll_gridcells = False,
        tables_to_cache = [
            'business',
            'households',
            'buildings',
            'parcels',
            'zones',
            "households_for_estimation",
            "business_for_estimation",
            "persons",
            "travel_data",
            "annual_relocation_rates_for_business",
            "buildings_for_estimation",
            "building_use",
            "building_use_classification",
            'urbansim_constants'
        ],  
        ),
    'input_configuration': DatabaseConfiguration(
        host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
        user_name     = os.environ.get('MYSQLUSERNAME',''),
        password      = os.environ.get('MYSQLPASSWORD',''),
        database_name = "san_francisco_baseyear_change_20061214",
        ),

    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['sanfrancisco', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),                          
    'output_configuration': DatabaseConfiguration(
        host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
        user_name     = os.environ.get('MYSQLUSERNAME',''),
        password      = os.environ.get('MYSQLPASSWORD',''),
        database_name = "san_francisco_baseyear_change_20061228",
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

    