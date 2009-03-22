# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

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
        ),        
    'seed':(1,1)
    }