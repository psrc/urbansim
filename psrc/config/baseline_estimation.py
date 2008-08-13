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


from baseline import Baseline
from opus_core.database_management.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimation(Baseline):

    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self.merge(self._get_estimation_changes())
        
    def _get_estimation_changes(self):
        return {    
    'cache_directory' : 'C:/urbansim_cache/psrc/estimation', # change or leave out
    'output_configuration': DatabaseConfiguration(
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