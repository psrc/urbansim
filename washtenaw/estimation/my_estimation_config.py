# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


my_configuration = {
    'scenario_database_configuration':ScenarioDatabaseConfiguration(
        database_name = "semcog_baseyear", #change
        ),
    'estimation_database_configuration':EstimationDatabaseConfiguration(
        database_name = "semcog_baseyear_estimation",
        ),
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    'cache_directory':'/urbansim_cache/semcog/cache_source', # change or leave out
    'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
        unroll_gridcells = True,
        cache_from_database = False,
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