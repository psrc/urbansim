# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc.configs.baseline import Baseline

class CachingConfiguration(Baseline):
    """Configuration for creating the cache for the water demand model.
    """
    def __init__(self):
        Baseline.__init__(self)
        
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('exogenous_relationships')
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('weather_exogenous')
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('consumption_re')
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('consumption_co')
        self['creating_baseyear_cache_configuration'].tables_to_cache.append('consumption_mf')
        tables_to_copy_to_previous_years = self['creating_baseyear_cache_configuration'].tables_to_copy_to_previous_years
        for table_name, year in tables_to_copy_to_previous_years.iteritems():
            tables_to_copy_to_previous_years[table_name] = 1995
        self['cache_directory'] = 'c:/urbansim_cache/water_test'
        self['dataset_pool_configuration'] = DatasetPoolConfiguration(
            package_order=['waterdemand', 'psrc', 'urbansim', 'opus_core'],
            )
        self['scenario_database_configuration'].database_name = 'bellevue_consump_agg_month_year'