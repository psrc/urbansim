# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from baseline import Baseline

my_cache_config = CreatingBaseyearCacheConfiguration(
        cache_directory_root = '/urbansim_cache/semcog/runs',
        cache_from_database = False,
        baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = '/urbansim_cache/semcog/cache_source',
            #years_to_cache = range(2000,2001)
            ),
        cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
        tables_to_cache = Baseline.tables_to_cache,
        tables_to_copy_to_previous_years = Baseline.tables_to_copy_to_previous_years,
    )

my_configuration = {
    'scenario_database_configuration': ScenarioDatabaseConfiguration(
                database_name = 'semcog_baseyear',
                ),
#     'models': [
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
#                'household_transition_model',
                #'employment_transition_model',
                #'household_relocation_model',
                #'household_location_choice_model',
                #'employment_relocation_model',
                #{'employment_location_choice_model': {'group_members': ['industrial','commercial']}},
                #'distribute_unplaced_jobs_model'
#                ],
    'cache_directory': None,
    #'cache_directory': '/Users/hana/urbansim_cache/washtenaw/cache_source_la',
    'remove_cache': False, # remove cache after finishing the simulation
    'creating_baseyear_cache_configuration': my_cache_config,
    'datasets_to_cache_after_each_model': [],
    'base_year':2005,
    'years':(2006, 2010),
    'seed':1,#(1,1),
    'debuglevel': 10
    }
