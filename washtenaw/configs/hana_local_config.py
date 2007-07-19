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

from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.database_configuration import DatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from baseline import Baseline

my_cache_config = CreatingBaseyearCacheConfiguration(
        cache_directory_root = '/Users/hana/urbansim_cache/washtenaw/runs',
        cache_from_mysql = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/Users/hana/urbansim_cache/washtenaw/cache_source_la',
            years_to_cache = range(2000,2001)
            ),
        cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
        tables_to_cache = Baseline.tables_to_cache,
    )

my_configuration = {
    'input_configuration': DatabaseConfiguration(
                host_name     = os.environ.get('MYSQLHOSTNAME','localhost'),
                user_name     = os.environ.get('MYSQLUSERNAME',''),
                password      = os.environ.get('MYSQLPASSWORD',''),
                database_name = 'washtenaw_hana',
                ),
     'models': [
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
                'household_transition_model',
                #'employment_transition_model',
                #'household_relocation_model',
                #'household_location_choice_model',
                #'employment_relocation_model',
                #{'employment_location_choice_model': {'group_members': ['industrial','commercial']}},
                #'distribute_unplaced_jobs_model'
                ],
    'cache_directory': None,
    #'cache_directory': '/Users/hana/urbansim_cache/washtenaw/cache_source_la',
    'remove_cache': False, # remove cache after finishing the simulation
    'creating_baseyear_cache_configuration': my_cache_config,
    'datasets_to_cache_after_each_model': [],
    'base_year':2000,
    'years':(2001, 2001),
    'seed':1,#(1,1),
    'debuglevel': 10
    }
