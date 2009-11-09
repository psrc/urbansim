# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

my_configuration = {
     'cache_directory':r'/aalborg1/lmwang/urbansim_cache/paris/', ### TODO: Set this cache_directory to something useful.
    'scenario_database_configuration': ScenarioDatabaseConfiguration(
        database_name = "paris_estimation",
        ),

    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['paris', 'urbansim', 'opus_core'],
        ),                          
    'estimation_database_configuration': EstimationDatabaseConfiguration(
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

    
