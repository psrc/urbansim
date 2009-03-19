# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.configuration import Configuration
from psrc_parcel.configs.baseline import Baseline as PsrcParcelConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.employment_location_choice_model_by_zipcodes_configuration_creator import EmploymentLocationChoiceModelByZipcodesConfigurationCreator
from psrc_parcel.configs.scaling_jobs_model_by_zipcodes_configuration_creator import ScalingJobsModelByZipcodesConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from numpy import array
import os

class ConfigDataPreparationForJobsWithZipcodes(PsrcParcelConfiguration):
    def __init__(self):
        config = PsrcParcelConfiguration()
        config['creating_baseyear_cache_configuration'].cache_directory_root = r'/Users/hana/urbansim_cache/psrc/data_preparation/run_zipcodes'
        config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/data_preparation/cache_for_zipcodes'
        #config['scenario_database_configuration'].database_name = 'psrc_2005_parcel_baseyear_data_prep_start'
        config['scenario_database_configuration'].database_name = 'psrc_2005_parcel_baseyear_data_prep_business_zip'
        config_changes = {
            'description':'data preparation for PSRC parcel (buildings)',
            'flush_variables': False,
            'cache_directory': '/Users/hana/urbansim_cache/psrc/data_preparation/cache_for_zipcodes',
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                ),
            'base_year':2000,
            'years':(2001, 2003),
            'models_in_year': {
              2001: 
              [
                "employment_relocation_model",
                {"employment_location_choice_model": {"group_members": "_all_" }}
              ],
              2002: [
                "employment_relocation_model",
                "governmental_employment_location_choice_model",
                    ],
              2003: [
                "employment_relocation_model",
                "governmental_employment_location_choice_model_without_filter"
               ]
           },
            "datasets_to_preload":{
                    'zone':{},
                    'job': {},
                    'building': {},
                    "job_building_type":{},
                    "zipcode": {}
                },
            "datasets_to_cache_after_each_model": [
                     'parcel', 'building',  'job'
                     ]
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)

        self['models_configuration']['non_home_based_employment_location_choice_model'] = {}
        self['models_configuration']['non_home_based_employment_location_choice_model']['controller'] = \
                   EmploymentLocationChoiceModelByZipcodesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                sampler = None,
                                records_per_chunk = 3000,
                                capacity_string = "urbansim_parcel.building.vacant_non_home_based_job_space",
                                number_of_units_string = None,
                                lottery_max_iterations=30
                                ).execute()
        self['models_configuration']['governmental_employment_location_choice_model'] = {}
        self['models_configuration']['governmental_employment_location_choice_model']['controller'] = \
                   ScalingJobsModelByZipcodesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                filter = "urbansim_parcel.building.is_governmental"
                                ).execute()
        self['models_configuration']['governmental_employment_location_choice_model_without_filter'] = {}
        self['models_configuration']['governmental_employment_location_choice_model_without_filter']['controller'] = \
                   ScalingJobsModelByZipcodesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                ).execute()
        self['models_configuration']['home_based_employment_location_choice_model'] = {}
        self['models_configuration']['home_based_employment_location_choice_model']['controller'] = \
                   EmploymentLocationChoiceModelByZipcodesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                sampler = None,
                                capacity_string = "urbansim_parcel.building.vacant_home_based_job_space",
                                number_of_units_string = None,
                                lottery_max_iterations=30
                                ).execute()
        self['models_configuration']['employment_relocation_model']['controller'] = \
                    EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               probabilities = None,
                               rate_table=None,
                               output_index = 'erm_index').execute()
                               
