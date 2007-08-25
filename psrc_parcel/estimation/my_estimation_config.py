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

from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

my_configuration = {
    'cache_directory' : '/urbansim_cache/psrc_parcel/cache_source/', # change or leave out
    'output_configuration': DatabaseConfiguration(
        host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
        user_name     = os.environ.get('MYSQLUSERNAME',''),
        password      = os.environ.get('MYSQLPASSWORD',''),
        database_name = 'psrc_2005_parcel_baseyear_change_20070824',
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
        package_order_exceptions={},
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year': 2000,
    'years': (2000,2000),                    
    }
