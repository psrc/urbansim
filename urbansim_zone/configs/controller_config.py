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

from opus_core.configuration import Configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.real_estate_price_model_configuration_creator import RealEstatePriceModelConfigurationCreator
from urbansim.configurations.distribute_unplaced_jobs_model_configuration_creator import DistributeUnplacedJobsModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.household_transition_model_configuration_creator import HouseholdTransitionModelConfigurationCreator
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator

class UrbansimZoneConfiguration(Configuration):
    def __init__(self):
        Configuration.__init__(self)

        my_controller_configuration = {
        'real_estate_price_model': RealEstatePriceModelConfigurationCreator(
            dataset='pseudo_building', 
            outcome_attribute = 'ln_unit_price=ln(pseudo_building.avg_value)',
            submodel_string = 'building_type_id',
            filter_variable = None                                                   
            ).execute(),
        'employment_transition_model': 
                  EmploymentTransitionModelConfigurationCreator(
            location_id_name="pseudo_building_id"
            ).execute(),
        'household_transition_model': 
                  HouseholdTransitionModelConfigurationCreator(
            location_id_name="pseudo_building_id"
            ).execute(),
 
        'employment_relocation_model': 
                  EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'pseudo_building_id',
                               output_index = 'erm_index').execute(),
                               
        'household_relocation_model': HouseholdRelocationModelConfigurationCreator(
                        location_id_name = 'pseudo_building_id',
                        output_index = 'hrm_index',
                        ).execute(),
        'household_location_choice_model': {
                    'controller': HouseholdLocationChoiceModelConfigurationCreator(
                        location_set = "pseudo_building",                                                           
                        input_index = 'hrm_index',
                        ).execute(),
                    },
         'employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "pseudo_building",
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
                                location_set = "pseudo_building",
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
                        location_set = 'pseudo_building'
                        ).execute(),      
            'distribute_unplaced_jobs_model':  DistributeUnplacedJobsModelConfigurationCreator(
                                    location_set = 'pseudo_building'
                                            ).execute(),
                 
        }
        self['models_configuration'] = {}
        for model in my_controller_configuration.keys():
            if model not in self["models_configuration"].keys():
                self["models_configuration"][model] = {}
            self['models_configuration'][model]['controller'] = my_controller_configuration[model]

                
        self["datasets_to_preload"] = {
                'pseudo_building':{},
                'zone':{},
                'household':{},
                'job': {},
                #'travel_data':{},
                'job_building_type':{}
                }


