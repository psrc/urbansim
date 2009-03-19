# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration


my_configuration = {
    'cache_directory' : '/urbansim_cache/psrc_parcel/estimation/', # change or leave out
    'estimation_database_configuration': EstimationDatabaseConfiguration(
        database_name = 'psrc_2005_parcel_baseyear_change_20071011',
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year': 2000,
    'years': (2000,2000),                    
    }
