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


my_configuration = {
    'cache_directory': "/urbansim_cache/psrc_parcel", # change or leave out
    'cache_directory_root': "/urbansim_cache/psrc_parcel",
    'input_configuration': { 
    'db_input_database': "san_francisco_baseyear" #change
        },
    'output_configuration': {
        "db_output_database":"san_francisco_estimation_output"
    },
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_from_mysql': True,
    'debuglevel':7,
    'baseyear_cache':{'directory_to_cache':"/urbansim_cache/psrc_parcel/cache_source",
                      #'years':range(1996,2001)
                     },
    'base_year': 2001,
    'years': (2001,2001),
    #below settings are specified in controller setting
#    'tables_to_cache':[
#        'business',
#        'households',
#        'buildings',
#        'parcels',
#        'zones',
#        "households_for_estimation",
#        "business_for_estimation",
#        "persons",
#        "travel_data",
#        "annual_relocation_rates_for_business"
#        ],
#     "datasets_to_preload" : {
#        'zone':{},
#        'household':{},
#        'building':{},        
#        'parcel':{'package_name':'psrc_parcel'},
#        'business':{'package_name':'psrc_parcel'},
#        'person':{'package_name':'psrc_parcel'},        
#        'travel_data':{}
#        }     
    }

    