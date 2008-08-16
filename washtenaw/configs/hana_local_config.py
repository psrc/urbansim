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
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.database_management.database_configurations.database_configuration import DatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from baseline import Baseline

my_cache_config = CreatingBaseyearCacheConfiguration(
        cache_directory_root = '/Users/hana/urbansim_cache/washtenaw/runs',
        cache_from_mysql = False,
        unroll_gridcells = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/Users/hana/urbansim_cache/washtenaw/cache_source',
            #years_to_cache = range(2005,2006)
            ),
        cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
        tables_to_cache = Baseline.tables_to_cache,
        tables_to_copy_to_previous_years = Baseline.tables_to_copy_to_previous_years,
    )

my_configuration = {
    'input_configuration': DatabaseConfiguration(
                database_name = 'region_pilot_baseyear',
                ),
 #    'models': [
                #'prescheduled_events',
                #'events_coordinator',
                #'residential_land_share_model',
                #'land_price_model',
                #'development_project_transition_model',
                #'residential_development_project_location_choice_model',
                #'commercial_development_project_location_choice_model',
                #'industrial_development_project_location_choice_model',
                #'development_event_transition_model',
                #'events_coordinator',
                #'residential_land_share_model',
#                'deletion_event_model',
                #'regional_household_transition_model',
                #'regional_household_relocation_model',
                #'regional_household_location_choice_model',
#                'regional_employment_transition_model',
#                'regional_employment_relocation_model',
#                {'regional_employment_location_choice_model': {'group_members': ['_all_']}},
#                'regional_distribute_unplaced_jobs_model'
#                ],
    #'cache_directory': None,
    'cache_directory': '/Users/hana/urbansim_cache/washtenaw/cache_source',
    'remove_cache': False, # remove cache after finishing the simulation
    'creating_baseyear_cache_configuration': my_cache_config,
    #'datasets_to_cache_after_each_model': [],
    'base_year':2005,
    'years':(2006, 2010),
    'seed':1,#(1,1),
    'debuglevel': 2
    }
