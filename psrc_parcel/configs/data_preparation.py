#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

#from urbansim.estimation.config import config
from opus_core.configurations.database_configuration import DatabaseConfiguration
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.employment_location_choice_model_by_zones_configuration_creator import EmploymentLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from opus_core.resources import merge_resources_with_defaults
from numpy import array
import os

class DataPreparation(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()

        config_changes = {
            'description':'data preparation for PSRC parcel',
            'cache_directory': None,
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
                #cache_directory_root = r'/workspace/urbansim_cache/psrc_parcel',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
                    #existing_cache_to_copy = r'/workspace/urbansim_cache/psrc_parcel/estimation',
                    ),
                cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            'base_year':2005,
            'years':(2006, 2006),
            'models':[ # models are executed in the same order as in this list
                 "employment_relocation_model",
                {"employment_location_choice_model": {"group_members": "_all_"}},
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
                                #capacity_string = "non_residential_sqft",
                                compute_capacity_flag = False,
                                #agent_units_string = "sqft",
                                choices = 'opus_core.random_choices_from_index'
                                ).execute()
        self['models_configuration']['home_based_employment_location_choice_model'] = {}
        self['models_configuration']['home_based_employment_location_choice_model']['controller'] = \
                   EmploymentLocationChoiceModelByZonesConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                capacity_string = "building.aggregate(psrc_parcel.household.minimum_persons_and_2)",
                                number_of_units_string = None,
                                #agent_units_string = "sqft",
                                #choices = 'opus_core.random_choices_from_index'
                                ).execute()
        self['models_configuration']['employment_relocation_model']['controller'] = \
                    EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               probabilities = None,
                               rate_table=None,
                               output_index = 'erm_index').execute()
                    