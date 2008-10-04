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

from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration


# General information about the indicators to create.
config = {
    'cache_directory':'U:/urbansim_cache/run_1741.2007_01_03_11_20',
   #'cache_directory':'L:/urbansim_cache/run_330.2006_04_21_22_18',
   #'cache_directory':'M:/urbansim_cache/run_332.2006_04_21_22_25',
   #'cache_directory':'H:/urbansim_cache/run_333.2006_04_21_22_28',
    'run_description':'(run 329 - baseline 5/2)',
#    'run_description':'(run 330 - highway 5/2)',
#    'run_description':'(run 332 - no ugb + highway 5/2)',
#    'run_description':'(run 333 - constrained King 5/2)',

    #'output_directory':'C:/Temp/cee530',
    'resources':{
        'input_configuration':DatabaseConfiguration(
            host_name     = os.environ['MYSQLHOSTNAME'],
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = 'PSRC_2000_baseyear',
            ),
        }, 
    'datasets_to_preload':{
        'gridcell':{
            'package_name':'urbansim',
            'nchunks':2
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
        },
    'dataset_pool_configuration': DatasetPoolConfiguration(
      package_order=['psrc', 'urbansim', 'opus_core'],
      ),
    }
