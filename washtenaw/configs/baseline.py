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
from getpass import getuser
from opus_core.storage_factory import StorageFactory
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from washtenaw.configs.controller_configuration import ControllerConfiguration

# ATTENTION:
#***********
# Do not modify this file by adding your own local settings, such as directory names.
# Create a file called username_local_config.py in this directory 
# and put your own setting in a dictionary called 'my_configuration' (see hana_local_config.py as an example).
# This way people do not have to modify the Baseline configuration every time somebody else modifies it.

class Baseline(GeneralConfiguration):
    """Washtenaw's baseline configuration.
    """
    tables_to_cache = [
                    'annual_employment_control_totals',
                    'annual_household_control_totals',
                    'buildings',
                    'building_types',
                    'development_event_history',
                    'gridcells',
                    'households',
                    'job_building_types',
                    'jobs',
                    'travel_data',
                    'zones',
                    'counties',
                    'commercial_development_location_choice_model_coefficients',
                    'commercial_development_location_choice_model_specification',
                    'commercial_employment_location_choice_model_coefficients',
                    'commercial_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_specification',
                    'home_based_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_coefficients',
                    'industrial_employment_location_choice_model_specification',
                    'industrial_development_location_choice_model_coefficients',
                    'industrial_development_location_choice_model_specification',
                    'residential_development_location_choice_model_coefficients',
                    'residential_development_location_choice_model_specification',
                    'fazes',
                    'urbansim_constants',
                    'household_location_choice_model_coefficients',
                    'household_location_choice_model_specification',
                    'land_price_model_coefficients',
                    'land_price_model_specification',
                    'residential_land_share_model_coefficients',
                    'residential_land_share_model_specification',
#                    'plan_type_group_definitions',
#                    'plan_type_groups',
                    'large_areas',
                    'household_characteristics_for_ht',
                    'development_types',
                    'development_type_group_definitions',
                    'development_constraints',
                    'annual_relocation_rates_for_households',
                    'annual_relocation_rates_for_jobs',
                    'base_year',
                    'cities',
                    'development_events_exogenous',
                    'development_type_groups',
                    'employment_adhoc_sector_group_definitions',
                    'employment_adhoc_sector_groups',
                    'employment_events',
                    'employment_sectors',
                    #'land_use_events',
                    'plan_types',
                    'race_names',
                    'target_vacancies',
                    'jobs_for_estimation',
                    'households_for_estimation',
                    'job_building_types',
                    'deletion_events'
                    ]
    
    tables_to_copy_to_previous_years = {
                    'development_type_group_definitions': 1990,
                    'development_type_groups': 1990,
                    'development_types': 1990,
                    'urbansim_constants': 1990,
                    }
    
    def __init__(self):
        config = AbstractUrbansimConfiguration()
        
        config_changes = {
            'description':'Region Pilot Baseline',
            'input_configuration': DatabaseConfiguration(
                host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
                user_name     = os.environ.get('MYSQLUSERNAME',''),
                password      = os.environ.get('MYSQLPASSWORD',''),
                database_name = 'washtenaw_class',
                ),
            'models': [
                'prescheduled_events',
                'events_coordinator',
                'residential_land_share_model',
                'land_price_model',
                'regional_development_project_transition_model',
                'residential_regional_development_project_location_choice_model',
                'commercial_regional_development_project_location_choice_model',
                'industrial_regional_development_project_location_choice_model',
                'development_event_transition_model',
                'events_coordinator',
                'residential_land_share_model',
                #'deletion_event_model',
                'regional_household_transition_model',
                'regional_household_location_choice_model',
                'regional_employment_transition_model',
                {'regional_employment_location_choice_model': {'group_members': ['home_based', 'commercial', 'industrial']}},
                'household_relocation_model',
                'household_location_choice_model',
                'employment_relocation_model',
                {'employment_location_choice_model': {'group_members': ['_all_']}},
                'distribute_unplaced_jobs_model'
                ],
            'cache_directory':None, ### TODO: Set this cache_directory to something useful.
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_directory_root = "/urbansim_cache/washtenaw",
                cache_from_mysql = True,
                 baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = "/urbansim_cache/washtenaw/cache_source",
                    ),
                cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
                tables_to_cache = self.tables_to_cache,
                tables_to_cache_nchunks = {'gridcells': 1},
                tables_to_copy_to_previous_years = self.tables_to_copy_to_previous_years,
                ),
            'datasets_to_preload': {
                'development_constraint': {},
                'development_event_history': {},
                'development_type': {},
                'gridcell': {'nchunks': 2},
                'household': {},
                'job': {},
                'job_building_type': {},
                'target_vacancy': {},
                'zone': {},
                'deletion_event': {}
                },
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['washtenaw', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            'base_year':2005,
            'years':(2006, 2010),
            }
        config.merge(config_changes)
        self.merge(config)
        self.merge_with_controller()
        try:
            exec('from %s_local_config import my_configuration' % getuser())
            local_config = True
        except:
            logger.note("No user's settings found or error occured when loading.")
            local_config = False
        if local_config:
            self.merge(my_configuration)
      
    def merge_with_controller(self):
        controller = ControllerConfiguration()
        self["models_configuration"].merge(controller)
            
#if __name__ == '__main__':
#    c = Baseline()
