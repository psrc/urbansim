# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim.estimation.config import config
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.household_location_choice_model_by_zones_configuration_creator import HouseholdLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from numpy import array
import os

class ConfigHouseholds(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()

        config_changes = {
            'description':'data preparation for PSRC parcel (households)',
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
                 "household_relocation_model",
                 "household_location_choice_model",
                ],
            "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building': {}
                }
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)
        self['models_configuration']['household_location_choice_model'] = {}
        self['models_configuration']['household_location_choice_model']['controller'] = \
                   HouseholdLocationChoiceModelByZonesConfigurationCreator(
                                location_set = "building",
                                sampler = None,
                                input_index = 'hrm_index',
                                capacity_string = "urbansim_parcel.building.vacant_residential_units",
                                number_of_units_string = None,
                                nchunks=1,
                                lottery_max_iterations=20
                                ).execute()
        self['models_configuration']['household_relocation_model']['controller'] = \
                    HouseholdRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               probabilities = None,
                               rate_table=None,
                               output_index = 'hrm_index').execute()
                    