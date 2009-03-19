# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from baseline import Baseline
import os
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from sanfrancisco.configs.config_changes_for_estimation import ConfigChangesForEstimation

class BaselineEstimation(Baseline):

    def __init__(self):
        Baseline.__init__(self)
        self['config_changes_for_estimation'] = ConfigChangesForEstimation()
        self.merge(self._get_estimation_changes())
        
    def _get_estimation_changes(self):
        return {
     'cache_directory':r'e:/urbansim_cache/sanfrancisco/cache_source', ### TODO: Set this cache_directory to something useful.
    'scenario_database_configuration': ScenarioDatabaseConfiguration(
        database_name = "sanfrancisco_baseyear",
        ),

    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['sanfrancisco', 'urbansim', 'opus_core'],
        ),                          
    'estimation_database_configuration': EstimationDatabaseConfiguration(
        database_name = "sanfrancisco_baseyear_change_20080125",
        ),
    'dataset_pool_configuration': DatasetPoolConfiguration(
        package_order=['sanfrancisco', 'urbansim', 'opus_core'],
        ),     
    'datasets_to_cache_after_each_model':[],
    'base_year': 2001,
    'years': (2001,2001), 
    'datasets_to_cache_after_each_model':[],
    'low_memory_mode':False,
    "datasets_to_preload" : {
        'zone':{},
        'household':{},
        'building':{},        
        'parcel':{'package_name':'sanfrancisco'},
        'business':{'package_name':'sanfrancisco'},
        'person':{'package_name':'sanfrancisco'},        
        "building_use":{'package_name':'sanfrancisco'},
        "building_use_classification":{'package_name':'sanfrancisco'},
        'travel_data':{},
        'urbansim_constant':{}
        }
        }

    
