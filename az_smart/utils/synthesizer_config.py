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
from opus_core.configuration import Configuration

config = Configuration({
    'cache_directory': "/urbansim_cache/az_smart", # change or leave out
    'cache_directory_root': "/urbansim_cache/az_smart",

    'db_host_name':os.environ['MYSQLHOSTNAME'],
    'db_user_name':os.environ['MYSQLUSERNAME'], 
    'db_password':os.environ['MYSQLPASSWORD'],
    'input_configuration': { 
        'db_input_database': "san_francisco_baseyear" #change
        },
    'output_configuration': {
        "db_output_database":"san_francisco_estimation_output"
        },

    'low_memory_mode':False,
    'cache_from_mysql': True,
    'debuglevel':7,
    'baseyear_cache':{'directory_to_cache':"/urbansim_cache/az_smart/cache_source",
                      #'years':range(1996,2001)
                     },
    'base_year': 2000,
    'years': (2000,2000),
    'tables_to_cache':[
        'households',
        'buildings',
        'parcels',
        'zones',
        "households_for_estimation"
        ],
     "datasets_to_preload" : {
        'zone':{},
        'household':{},
        'building':{},        
        'parcel':{'package_name':'az_smart'},        
        }    
    }
)    