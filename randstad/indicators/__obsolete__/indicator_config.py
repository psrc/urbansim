#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from randstad.run_config.randstad_baseline import run_configuration as config

# General information about the indicators to create.
config = {
    'run_description':'(run no. 235)',
#    'cache_directory':"C:/urbansim_cache/randstad",
    'cache_directory':"C:/urbansim_cache/randstad/run_1.2006_07_12_14_23",
    'resources':{
        'input_configuration':{
            'db_host_name':config['input_configuration'].host_name,
            'db_input_database':config['input_configuration'].database_name,
            'db_user_name':config['input_configuration'].user_name,
            'db_password':config['input_configuration'].password,
            }, 
        },
          
    'required_datasets':['job', 'household', 'gridcell', 'zone', 'travel_data', 
                         'faz', 'large_area', 'county', 'development_event',
                         'city', 'ring'],
    'datasets_to_preload':{
        'gridcell':{
            'package_name':'urbansim',
            },
        'household':{
            'package_name':'urbansim',
            },
        'job':{
            'package_name':'urbansim',
            },
        'zone':{
            'package_name':'urbansim',
            },
        'travel_data':{
            'package_name':'urbansim',
            },
        'ring':{
            'package_name':'randstad',
            },
      
        },

   }
