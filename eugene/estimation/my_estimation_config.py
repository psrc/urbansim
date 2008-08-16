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

from opus_core.database_management.database_configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration


my_configuration = {
    'cache_directory':'/urbansim_cache/eugene', # change or leave out
    'input_configuration':DatabaseConfiguration(
        database_name = 'eugene_1980_baseyear',
        ),
    'output_configuration':DatabaseConfiguration(
        database_name = 'eugene_1980_baseyear_estimation',
        ),
    
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'base_year':1980,
    'years':(1980,1980),
    'seed':10,#(10,10)
    }