# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from opus_core.configuration import Configuration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from psrc_parcel.configs.baseline import Baseline


class CachingConfiguration(Configuration):

    def __init__(self):
        Configuration.__init__(self, self.__my_configuration())

    def __my_configuration(self):
        tables_to_cache = [
                    'households',
                    'buildings',
                    'parcels',
                    'gridcells',
                    'zones',
                    "jobs",
                    "households_for_estimation",
                    "jobs_for_estimation",
                    #"development_event_history",
                    "persons",
                    "persons_for_estimation",
                    "travel_data",
                    "building_types",
                    "job_building_types",
                    'urbansim_constants',
                    "target_vacancies",
                    "home_based_employment_location_choice_model_coefficients",
                    "home_based_employment_location_choice_model_specification",
                    "non_home_based_employment_location_choice_model_coefficients",
                    "non_home_based_employment_location_choice_model_specification",
                    "household_location_choice_model_coefficients",
                    "household_location_choice_model_specification",
                    "real_estate_price_model_coefficients",
                    "real_estate_price_model_specification",
                    "annual_household_control_totals",
                    "annual_relocation_rates_for_households",
                    "household_characteristics_for_ht",
                    "annual_employment_control_totals",
                    "annual_relocation_rates_for_jobs",
                    "land_use_types",
                    "generic_land_use_types",
                    'employment_sectors',
                    'employment_adhoc_sector_groups',
                    'employment_adhoc_sector_group_definitions',
                    'development_templates',
                    'development_template_components',
                    'development_constraints',
                    "building_sqft_per_job",
                    "fazes",
                    "large_areas",
                    "demolition_cost_per_sqft",
                    'constant_taz_columns',
                    'zipcodes',
                    'cities',
                    'districts',
                    'area_types',
                    "work_at_home_choice_model_coefficients",
                    "work_at_home_choice_model_specification",
                    "workplace_choice_model_for_resident_coefficients",
                    "workplace_choice_model_for_resident_specification",
                    "development_project_proposals",
                   'development_project_proposals_for_estimation',
                   'tours',
                   'households_2001',
            ]

        return {
        'cache_directory' : '/urbansim_cache/psrc_parcel/developer_model', # change or leave out
        #'cache_directory' : '/workspace/urbansim_cache/psrc_parcel_lmwang/estimation/',
        'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
    #        cache_directory_root = '/tmp/urbcache/sandbox_runs/estimation',
            unroll_gridcells = False,
            cache_from_database = True,
            baseyear_cache = BaseyearCacheConfiguration(
                existing_cache_to_copy = r'/urbansim_cache/psrc_parcel_2005/cache_source',
                ),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            tables_to_cache = tables_to_cache,
            tables_to_cache_nchunks = {
                'parcels':4,
                'buildings':5
                },
            tables_to_copy_to_previous_years = {},
            ),
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            #database_name = 'psrc_2005_parcel_baseyear_change_20070608',
            database_name = 'psrc_2005_parcel_baseyear_change_20080622_2006',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
            ),
        'base_year': 2006,
        }

