# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from baseline import Baseline
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from urbansim_parcel.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimation(Baseline):

    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        ## set base_year and years to 2006 for HLCM for the psrc_parcel project
        #self['config_changes_for_estimation']['household_location_choice_model'].merge({'base_year': 2006, 'years':(2006, 2006)})

        self['cache_directory'] = '/Users/hana/urbansim_cache/psrc/cache_source_parcel'
        self['estimation_database_configuration'] = EstimationDatabaseConfiguration(
                                                             database_name = 'psrc_2005_parcel_baseyear_change_estimation',
                                                             )
        self['dataset_pool_configuration'] = DatasetPoolConfiguration(
                                                                      package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
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


