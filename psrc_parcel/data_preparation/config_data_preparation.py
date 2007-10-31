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
from opus_core.configuration import Configuration
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.household_location_choice_model_by_zones_configuration_creator import HouseholdLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from psrc_parcel.configs.employment_location_choice_model_by_zones_configuration_creator import EmploymentLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from numpy import array
import os

class ConfigDataPreparation(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()

        config_changes = {
            'description':'data preparation for PSRC parcel (buildings)',
            'flush_variables': False,
            'cache_directory': None,
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                cache_directory_root = r'/Users/hana/urbansim_cache/psrc/data_preparation/run',
                #cache_directory_root = r'/urbansim_cache/psrc_parcel',
                #cache_directory_root = r'/home/lmwang/urbansim_cache/psrc_parcel',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/data_preparation/cache',
                    #existing_cache_to_copy = r'/urbansim_cache/psrc_parcel/cache_source',
                    #existing_cache_to_copy = r'/home/lmwang/urbansim_cache/psrc_parcel/cache_source',
                    years_to_cache = [2000]
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            'base_year':2000,
            'years':(2001, 2005),
            'models_in_year': {
               2001: # Step 2 (Create new residential buildings)
               [ 
                 "real_estate_price_model",
                 "expected_sale_price_model",
                 "development_proposal_choice_model",
                 "building_construction_model",
                ],
               2002: # Step 3 (Assign buildings to households)
               [
                 "household_relocation_model",
                 "household_location_choice_model",
                ],
               2003: # Step 4 (Assign buildings to jobs with known parcel_id)
               [
                'assign_buildings_to_jobs'
                ],
               2004: # Step 5 (Create new non-residential buildings)
               [
                 "expected_sale_price_model",
                 "development_proposal_choice_model_nr",
                 "building_construction_model",
                ],
              2005: # Step 6 (Assign buildings to remaining jobs)
              [
                "employment_relocation_model",
                {"employment_location_choice_model": {"group_members": "_all_" }},
               ]
           },
            "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'job': {},
                    'building': {},
                    'parcel': {},
                    "job_building_type":{},
                    #'development_project_proposal': {}
                },
            #"low_memory_mode": True,
            "datasets_to_cache_after_each_model": [
                     'parcel', 'building', 'development_project_proposal', 'household', 'job',
                     'development_project_proposal_component'
                     ]
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)
        self['models_configuration']['development_proposal_choice_model']['controller']["import"] =  {
                       "psrc_parcel.models.development_proposal_sampling_model_by_zones":
                       "DevelopmentProposalSamplingModelByZones"
                       }
        self['models_configuration']['development_proposal_choice_model']['controller']["init"]["name"] =\
                        "DevelopmentProposalSamplingModelByZones"
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["zones"] = 'zone'
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["type"] = "'residential'"
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["n"] = 50
        self['models_configuration']['development_proposal_choice_model_nr'] = Configuration(self['models_configuration']['development_proposal_choice_model'])
        self['models_configuration']['development_proposal_choice_model_nr']['controller']['run']['arguments']["type"] = "'non_residential'"
        self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["parcel_filter_for_redevelopment"] = None
        #self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["create_proposal_set"] = False
        self['models_configuration']['expected_sale_price_model']['controller']["run"]['arguments']["chunk_specification"] = "{'nchunks': 5}"
        #self['models_configuration']['building_construction_model']['controller']["run"]['arguments']["consider_amount_built_in_parcels"] = False
        self['models_configuration']['building_construction_model']['controller']['run']['arguments']["current_year"] = 2000
        
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
                               
        self['models_configuration']['assign_buildings_to_jobs'] = {}
        self['models_configuration']['assign_buildings_to_jobs']['controller'] = {
                  "import": {
                     "psrc_parcel.data_preparation.assign_bldgs_to_jobs_when_multiple_bldgs_in_parcel": "RunAssignBldgsToJobs"
                     },
                  "init": {
                           "name": "RunAssignBldgsToJobs"
                           },
                  "run": {
                          "arguments": {
                                        "job_dataset": "job",
                                        "dataset_pool": "dataset_pool"}
                          }
                      }