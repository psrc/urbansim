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
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

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
            package_order_exceptions={},
            )
        self['input_configuration'].database_name = 'bellevue_consump_agg_month_year'