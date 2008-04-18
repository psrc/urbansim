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

from math import exp, log
from numpy import array
from opus_core.configuration import Configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.distribute_unplaced_jobs_model_configuration_creator import DistributeUnplacedJobsModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.household_transition_model_configuration_creator import HouseholdTransitionModelConfigurationCreator
from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator
import os, copy


UNIT_PRICE_RANGE = (exp(3), exp(7))
class UrbansimZoneConfiguration(AbstractUrbansimConfiguration):
    def __init__(self):
        AbstractUrbansimConfiguration.__init__(self)
        models_configuration = self['models_configuration']
        
        ## employment_location_choice_model is defined for gridcells at urbansim package 
        if "home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["home_based_employment_location_choice_model"]
        if "non_home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["non_home_based_employment_location_choice_model"]

        my_controller_configuration = {
        'employment_transition_model': 
                  EmploymentTransitionModelConfigurationCreator(
            location_id_name="zone_id"
            ).execute(),
        'household_transition_model': 
                  HouseholdTransitionModelConfigurationCreator(
            location_id_name="zone_id"
            ).execute(),
 
        'employment_relocation_model': 
                  EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'zone_id',
                               output_index = 'erm_index').execute(),
                                       
         'employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "zone",
                                input_index = 'erm_index',
                                agents_for_estimation_table = "jobs_for_estimation",
                                estimation_weight_string = None,
                                number_of_units_string = None,
                                portion_to_unplace = 0,
                                capacity_string = "vacant_SSS_job_space",
                                variable_package = "urbansim"
                                ).execute(),
                                       
            'home_based_employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "zone",
                                input_index = 'erm_index',
                                estimation_weight_string = "vacant_home_based_job_space",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                estimation_size_agents = 0.4,
                                number_of_units_string = None,
                                portion_to_unplace = 0,
                                capacity_string = "vacant_home_based_job_space",
                                variable_package = "urbansim",
                                ).execute(),
            'governmental_employment_location_choice_model': 
                   GovernmentalEmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        location_set = 'zone'
                        ).execute(),      
            'distribute_unplaced_jobs_model':  DistributeUnplacedJobsModelConfigurationCreator(
                                    location_set = 'zone'
                                            ).execute(),
                 
            "household_relocation_model" : {
                    "import": {"urbansim.models.household_relocation_model_creator":
                                    "HouseholdRelocationModelCreator"
                              },
                    "init": {
                        "name": "HouseholdRelocationModelCreator().get_model",
                        "arguments": {
                                      "debuglevel": 'debuglevel',
                                      "location_id_name": "'zone_id'",
                                      },
                        },
                     "prepare_for_run": {
                         "name": "prepare_for_run",
                         "arguments": {"what": "'households'",  "rate_storage": "base_cache_storage",
                                           "rate_table": "'annual_relocation_rates_for_households'"},
                         "output": "hrm_resources"
                        },
                    "run": {
                        "arguments": {"agent_set": "household", "resources": "hrm_resources"},
                        "output": "hrm_index"
                        }
                    }
            }
                    
            

        for model in my_controller_configuration.keys():
            if model not in self["models_configuration"].keys():
                self["models_configuration"][model] = {}
            self['models_configuration'][model]['controller'] = my_controller_configuration[model]
        
        #settings for the HLCM
        hlcm_controller = self["models_configuration"]["household_location_choice_model"]["controller"]
        hlcm_controller["init"]["arguments"]["location_set"] = "zone"
        hlcm_controller["init"]["arguments"]["location_id_string"] = "'zone_id'"
        hlcm_controller["init"]["arguments"]["estimation_weight_string"] = "'urbansim.zone.vacant_residential_units'"
        hlcm_controller["init"]["arguments"]["capacity_string"] = "'vacant_residential_units'"
        hlcm_controller["init"]["arguments"]['sample_size_locations']=30
        hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
        hlcm_controller["init"]["arguments"]["variable_package"] = "'urbansim'"
        hlcm_controller["prepare_for_estimate"]["arguments"]["agents_for_estimation_table"] = "'households_for_estimation'"
        hlcm_controller["run"]["arguments"]["chunk_specification"] ="{'records_per_chunk':50000}"
        hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = True
        hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = None
        
        models_configuration['household_location_choice_model']["controller"].replace(hlcm_controller)
                
        self["datasets_to_preload"] = {
                'zone':{},
                'household':{},
                'job': {},
                #'travel_data':{},
                'job_building_type':{}
                }
        models_configuration['distribute_unplaced_jobs_model']['controller']['import'] =  {
           'urbansim_parcel.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'}

config = UrbansimZoneConfiguration()
