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

from numpy import array

from opus_core.configuration import Configuration
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.estimation_base_config import run_configuration as config
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration


config_changes = {
    'input_configuration':DatabaseConfiguration(
        database_name = 'PSRC_2000_parcels',
        ),
    'cache_directory':'C:/tmp/urbansim_cache/psrc_parcel_hana/06_06_13_11_39_48',
    'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
        #cache_directory_root = 'C:/tmp/urbansim_cache/psrc_parcel_hana',        
        unroll_gridcells = False,
        cache_from_mysql = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = 'C:/tmp/urbansim_cache/psrc_parcel_hana',
            ),
        tables_to_cache = [
            #'development_event_history',
            'edges',
            'parcels',
            'gridcells',
            'households',
            'households_for_estimation',
            'jobs',
            'travel_data',
            'persons', #need to cache
            'zones',
            #'urbansim_constants',
            #'land_price_model_coefficients',
            #'land_price_model_specification',
            ],
        tables_to_cache_nchunks = {
            'parcels':4,
            'gridcells':5
            },
        tables_to_copy_to_previous_years = {},
        ),
    'base_year':2000,
    'models_configuration':{
        'development_project_types':{
            'residential':{
                'units':'residential_units',
                'developable_maximum_unit_variable_full_name':'zone.aggregate(urbansim.gridcell.developable_maximum_residential_units)',
                'categories':array([1,2,3,5,10,20]),
                'residential':True,
                },
            'commercial':{
                'units':'commercial_sqft',
                'developable_maximum_unit_variable_full_name':'zone.aggregate(urbansim.gridcell.developable_maximum_commercial_sqft)',
                'categories':1000*array([1, 2, 5, 10]),
                'residential':False,                  
                },
            'industrial':{
                'units':'industrial_sqft',
                'developable_maximum_unit_variable_full_name':'zone.aggregate(urbansim.gridcell.developable_maximum_industrial_sqft)',
                'categories':1000*array([1,2,5,10]),
                'residential':False,                         
                },
            },
        },
    'datasets_to_preload':{
        'gridcell':{
            'package_name':'urbansim',
            'nchunks':5,
            },
        'parcel':{
            'package_name':'psrc',
            'nchunks':3,
            },                                 
        'household':{
            'package_name':'urbansim',
            },
#        'person':{
#            'package_name':'psrc',
#            },
        'zone':{
            'package_name':'urbansim',
            },
        'travel_data':{
            'package_name':'urbansim',
            },
#        'edge':{
#            'package_name':'transit_accessibility',    
#            } 
        },
    }
config.merge(config_changes)