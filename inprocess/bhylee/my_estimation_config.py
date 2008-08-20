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

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

my_configuration = {
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'PSRC_2000_parcels', # change
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = 'PSRC_2000_parcels_estimation_output',
        ),  
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_directory':r'C:\tmp\urbansim_cache\psrc_parcel', # change or leave out
    'base_year': 2006,
    'years': (2006,2006),
    'datasets_to_preload' :{
        'gridcell':{
            'package_name':'urbansim',
            'nchunks':2,
            },
        'parcel':{
            'package_name':'psrc',
            'nchunks':3,
            },                                 
        'household':{
            'package_name':'urbansim',
            },
        'person':{
            'package_name':'psrc',
            },
        'zone':{
            'package_name':'urbansim',
            },
        'travel_data':{
            'package_name':'urbansim',
            },
        'building':{},
#        'edge':{
#            'package_name':'transit_accessibility',    
#            } 
        },
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','psrc','urbansim','opus_core'],
        package_order_exceptions={},
        ),        
    'seed':(1,1)
    }