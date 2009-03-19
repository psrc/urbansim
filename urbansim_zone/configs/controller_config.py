# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.configuration import Configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.real_estate_price_model_configuration_creator import RealEstatePriceModelConfigurationCreator
from urbansim_zone.configs.add_projects_to_buildings_configuration_creator import AddProjectsToBuildingsConfigurationCreator
from urbansim_zone.configs.development_project_transition_model_configuration_creator import DevelopmentProjectTransitionModelConfigurationCreator
from urbansim_zone.configs.development_project_location_choice_model_configuration_creator import DevelopmentProjectLocationChoiceModelConfigurationCreator
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
        self['models'] = [
                'real_estate_price_model',
                'development_project_transition_model',
                'commercial_development_project_location_choice_model',
                'industrial_development_project_location_choice_model',
                'residential_development_project_location_choice_model',
                'add_projects_to_buildings',
                'household_transition_model',
                'employment_transition_model',
                'household_relocation_model',
                'household_location_choice_model',
                'employment_relocation_model',
                {   'employment_location_choice_model': {   'group_members': '_all_'}},
                'distribute_unplaced_jobs_model',
                ]
        self['model_system'] = 'urbansim.model_coordinators.model_system'
        my_controller_configuration = {
        'real_estate_price_model': RealEstatePriceModelConfigurationCreator(
            dataset='pseudo_building', 
            outcome_attribute = 'ln_unit_price=ln(pseudo_building.avg_value)',
            submodel_string = 'building_type_id',
            filter_variable = None,
            ).execute(),
        'residential_development_project_location_choice_model': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'residential',
                        coefficients_table = 'residential_development_location_choice_model_coefficients',
                        specification_table = 'residential_development_location_choice_model_specification',
                        units = 'residential_units',
                        sampler = None,
                        capacity_string = 'urbansim_zone.zone.developable_residential_units',
                        ).execute(),
        'commercial_development_project_location_choice_model': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'commercial',
                        coefficients_table = 'commercial_development_location_choice_model_coefficients',
                        specification_table = 'commercial_development_location_choice_model_specification',
                        units = 'commercial_job_spaces',
                        sampler = None,
                        ).execute(),
        'industrial_development_project_location_choice_model': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'industrial',
                        coefficients_table = 'industrial_development_location_choice_model_coefficients',
                        specification_table = 'industrial_development_location_choice_model_specification',
                        units = 'industrial_job_spaces',
                        sampler = None,
                        ).execute(),
         'development_project_transition_model': DevelopmentProjectTransitionModelConfigurationCreator(
                        vacancy_variables = {"commercial": "urbansim_zone.zone.number_of_vacant_commercial_jobs",
                                             "industrial": "urbansim_zone.zone.number_of_vacant_industrial_jobs"
                                            },
                        output_results = 'dptm_results',
                        ).execute(),
        'add_projects_to_buildings': AddProjectsToBuildingsConfigurationCreator().execute(), 
        'employment_transition_model': 
                  EmploymentTransitionModelConfigurationCreator(
            location_id_name="zone_id",
            ).execute(),
        'household_transition_model': 
                  HouseholdTransitionModelConfigurationCreator(
            location_id_name="zone_id",
            ).execute(),
 
        'employment_relocation_model': 
                  EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'zone_id',
                               output_index = 'erm_index').execute(),
                               
        'household_relocation_model': HouseholdRelocationModelConfigurationCreator(
                        location_id_name = 'zone_id',
                        output_index = 'hrm_index',
                        ).execute(),
        'household_location_choice_model': HouseholdLocationChoiceModelConfigurationCreator(
                        location_set = "zone",
                        capacity_string = 'urbansim_zone.zone.vacant_residential_units',
                        estimation_weight_string = 'urbansim_zone.zone.vacant_residential_units',
                        portion_to_unplace = 1/3.0,
                        nchunks = 3,
                        number_of_units_string = None,                       
                        input_index = 'hrm_index',
                        ).execute(),
         'employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "zone",
                                input_index = 'erm_index',
                                agents_for_estimation_table = "jobs_for_estimation",
                                estimation_weight_string = None,
                                number_of_units_string = None,
                                portion_to_unplace = 0,
                                capacity_string = "urbansim_zone.zone.number_of_vacant_SSS_jobs",
                                ).execute(),
                                       
          'home_based_employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "zone",
                                input_index = 'erm_index',
                                estimation_weight_string = "urbansim.zone.number_of_households",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                estimation_size_agents = 0.5,
                                number_of_units_string = None,
                                portion_to_unplace = 0,
                                capacity_string = "urbansim.zone.number_of_households",
                                ).execute(),
            'governmental_employment_location_choice_model': 
                   GovernmentalEmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        location_set = 'zone'
                        ).execute(),      
            'distribute_unplaced_jobs_model':  DistributeUnplacedJobsModelConfigurationCreator(
                                    location_set = 'zone'
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
                'job_building_type':{},
                'target_vacancy':{},
                'development_event_history':{},
                'building_type': {}
                }


