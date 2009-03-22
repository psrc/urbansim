# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim.estimation.config import config
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.employment_location_choice_model_by_zones_configuration_creator import EmploymentLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator

class ConfigJobs(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()
 
        config_changes = {
            'description':'data preparation for PSRC parcel',
            'cache_directory': None,
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
                #cache_directory_root = r'/urbansim_cache/psrc_parcel',
                #cache_directory_root = r'/workspace/urbansim_cache/psrc_parcel',
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                  existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
                    #existing_cache_to_copy = r'/urbansim_cache/psrc_parcel/cache_source',
                    #existing_cache_to_copy = r'/workspace/urbansim_cache/psrc_parcel/estimation',
                    years_to_cache = [2000]
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                ),
            'base_year':2000,
            'years':(2001, 2001),
            'models':[ # models are executed in the same order as in this list
                 "employment_relocation_model",
                {"employment_location_choice_model": {"group_members": "_all_" }},
                ],
            "datasets_to_preload":{
                    'zone':{},
                    'job':{},
                    "job_building_type":{},
                    'building': {}
                }
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)
        self['models_configuration']['non_home_based_employment_location_choice_model'] = {}
        self['models_configuration']['non_home_based_employment_location_choice_model']['controller'] = \
                   EmploymentLocationChoiceModelByZonesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                sampler = None,
                                capacity_string = "urbansim_parcel.building.vacant_non_home_based_job_space",
                                number_of_units_string = None,
                                lottery_max_iterations=30
                                ).execute()
        self['models_configuration']['home_based_employment_location_choice_model'] = {}
        self['models_configuration']['home_based_employment_location_choice_model']['controller'] = \
                   EmploymentLocationChoiceModelByZonesConfigurationCreator(
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
                    