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

from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration


my_configuration = {
    'cache_directory' : 'C:/urbansim_cache/psrc/estimation', # change or leave out
    'estimation_database_configuration': EstimationDatabaseConfiguration(
        database_name = 'GSPSRC_2000_baseyear_change_20070102',
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['psrc', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year': 2000,
    'years': (2000,2000),                    
    }