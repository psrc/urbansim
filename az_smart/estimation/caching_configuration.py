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
from opus_core.configuration import Configuration
from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from az_smart.configs.baseline import Baseline


class CachingConfiguration(Configuration):
    
    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = [
#            'business',
#            'households',
            'buildings',
            'parcels',
#            'zones',
#            "households_for_estimation",
#            "business_for_estimation",
#            "persons",
#            "travel_data",
#            "annual_relocation_rates_for_business",
#            "buildings_for_estimation",
            "building_types",
            #"generic_building_types",            
            #'urbansim_constants',
            #'land_use_types',
            #'gridcells',
            #'jobs',
            #'employment_sectors',
            #'employment_adhoc_sector_groups',
            #'employment_adhoc_sector_group_definitions',
            #'development_templates',
            #'development_template_components',
            #'development_constraints',
            #'target_vacancies'
            ]
        
        return {
        'cache_directory' : '/urbansim_cache/az_smart_lmwang/estimation/', # change or leave out
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_mysql = False,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'D:/urbansim_cache/az_smart',
                ),
            cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
            tables_to_cache = tables_to_cache,
            tables_to_cache_nchunks = {
                'parcels':4,
                'buildings':5
                },
            tables_to_copy_to_previous_years = {},                                          
            ),
        'input_configuration': DatabaseConfiguration(
            host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
            user_name     = os.environ.get('MYSQLUSERNAME',''),
            password      = os.environ.get('MYSQLPASSWORD',''),
            database_name = 'psrc_2005_parcel_baseyear',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['az_smart', 'urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'base_year': 2000,
        }

    