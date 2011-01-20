# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration


my_configuration = {
    'cache_directory' : 'C:/urbansim_cache/psrc/estimation', # change or leave out
    'estimation_database_configuration': EstimationDatabaseConfiguration(
        database_name = 'GSPSRC_2000_baseyear_change_20070102',
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['psrc', 'urbansim', 'opus_core'],
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year': 2000,
    'years': (2000,2000),                    
    }