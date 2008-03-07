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

from baseline import Baseline
from opus_core.database_management.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimation(Baseline):

    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self['cache_directory'] = '/Users/hana/urbansim_cache/psrc/cache_source_parcel_est'
        self['output_configuration'] = DatabaseConfiguration(
                                                             database_name = 'psrc_2005_parcel_baseyear_change_20080305',
                                                             )
        self['dataset_pool_configuration'] = DatasetPoolConfiguration(
                                                                      package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
                                                                      package_order_exceptions={},
                                                                      )
        self['datasets_to_cache_after_each_model'] = []
        self["datasets_to_preload"] = {
            'zone':{},
            'household':{},
            'building':{},
            'parcel':{'package_name':'urbansim_parcel'},
        #'development_template': {'package_name':'urbansim_parcel'},
        #'development_template_component': {'package_name':'urbansim_parcel'},
        #"job_building_type":{}
            'job':{},
            'person':{'package_name':'urbansim_parcel'},        
            "building_type":{'package_name':'urbansim_parcel'},
            'travel_data':{},
            }
        self['base_year'] = 2000
        self['years'] = (2000,2000)
        #self['low_memory_mode'] = True
        if 'models_in_year' in self.keys():
            del self['models_in_year']          


