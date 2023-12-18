# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.configuration import Configuration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

from psrc.configs.baseline import Baseline


class CacheConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
#        tables_to_cache = Baseline()['creating_baseyear_cache_configuration'].tables_to_cache
        tables_to_cache =[            
            #'development_event_history',
            'edges',
            'parcels',
            'gridcells',
            'households',
            'households_for_estimation',
            'jobs',
            'travel_data',
            'persons', #need to cache
            'persons_for_estimation',
            'zones',
            'cities',
            'buildings',
            'building_types',
            'urbansim_constants',
            'job_building_types',
            'tours',
            #'land_price_model_coefficients',
            #'land_price_model_specification',]
         ]
        return {
        'cache_directory' : 'C:/tmp/urbansim_cache/psrc_parcel', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_database = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'D:/urbansim_cache/full_psrc',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_cache_nchunks = {
                'parcels':8,
                'gridcells':5,
                'buildings':10,
                },
#            tables_to_copy_to_previous_years = {
#                'development_type_groups': 1995,
#                'development_types': 1995,
#                'development_type_group_definitions': 1995,
#                'development_constraints': 1995,
#                'urbansim_constants': 1995,
#                },
            ),
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            database_name = "psrc_activity2006_ver2" # 2006 PSRC Activity Survey for households_for_estimation,
            ),
        'estimation_database_configuration':EstimationDatabaseConfiguration(
            database_name = 'PSRC_2000_parcels_estimation_output',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['psrc', 'urbansim', 'opus_core'],
            ),
        'base_year': 2000,
        'years': (2000,2000),
        'datasets_to_preload' :{
            'gridcell':{
                'package_name':'urbansim',
                'nchunks':2,
                },
            'parcel':{
                'package_name':'psrc',
                'nchunks':3,
                },                                 
            'household':{
                'package_name':'urbansim',
                },
            'person':{
                'package_name':'psrc',
                },
            'zone':{
                'package_name':'urbansim',
                },
            'travel_data':{
                'package_name':'urbansim',
                },
            'building':{
                'package_name':'urbansim',
                },                
    #        'edge':{
    #            'package_name':'transit_accessibility',    
    #            } 
            },
        'seed':1,#(1,1)        
        }

if __name__ == '__main__':
    print("start caching with command create_baseyear_cache -cinprocess.psrc_parcel.baseyear_data_caching_configuration")