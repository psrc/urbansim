# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration


my_configuration = {
    'cache_directory':None, ### TODO: Set this cache_directory to something useful.
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = 'randstad_021105_estimation',
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = 'randstad_estimation_output',
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_directory':'/tmp/urbansim_cache/randstad', # change or leave out
    'base_year': 1995,
    'years': (1995,1995),
    }