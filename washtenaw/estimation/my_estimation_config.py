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

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


my_configuration = {
    'input_configuration':DatabaseConfiguration(
        database_name = "semcog_baseyear", #change
        ),
    'output_configuration':DatabaseConfiguration(
        database_name = "semcog_baseyear_estimation",
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_directory':'/urbansim_cache/semcog/cache_source', # change or leave out
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        unroll_gridcells = True,
        cache_from_mysql = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/urbansim_cache/semcog/cache_source',
            #years_to_cache  = range(1996,2001)
            ),
        tables_to_cache = [],
        tables_to_cache_nchunks = {'gridcells':1},
        tables_to_copy_to_previous_years = {},
        ),
    'base_year': 2005,
    'years': (2005,2005),
    }