# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration


my_configuration = {
    'cache_directory':'/urbansim_cache/eugene', # change or leave out
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'eugene_1980_baseyear',
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = 'eugene_1980_baseyear_estimation',
        ),
    
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year':1980,
    'years':(1980,1980),
    'seed':10,#(10,10)
    }