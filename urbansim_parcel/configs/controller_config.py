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
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from opus_core.configuration import Configuration
from numpy import array
import os
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator

class UrbansimParcelConfiguration(AbstractUrbansimConfiguration):
    def __init__(self):
        AbstractUrbansimConfiguration.__init__(self)
        models_configuration = self['models_configuration']
        
        if "home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["home_based_employment_location_choice_model"]
        if "non_home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["non_home_based_employment_location_choice_model"]
        models_configuration["business_location_choice_model"] = {
                             "estimation":"opus_core.bhhh_mnl_estimation",
                             "sampler":"opus_core.samplers.weighted_sampler",
                             "sample_size_locations":30,
        #                     "weights_for_estimation_string":"urbansim.zone.number_of_non_home_based_jobs",
                             "specification_table":"business_location_choice_model_specification",
                             "coefficients_table":"business_location_choice_model_coefficients",
                             "compute_capacity_flag":True,
                             "capacity_string":"urbansim_parcel.building.building_sqft",
                             "number_of_agents_string":"business.sqft",
                             "number_of_units_string":"urbansim_parcel.building.vacant_building_sqft",
           }
        
        my_controller_configuration = {
         'real_estate_price_model': {
            "import": {"urbansim.models.real_estate_price_model":
                                                "RealEstatePriceModel"},
            "init": {
                "name": "RealEstatePriceModel",
                "arguments": {"submodel_string": "'land_use_type_id'",
                              "outcome_attribute": "'ln_unit_price=ln(urbansim_parcel.parcel.unit_price)'",
                              "filter_attribute": "'numpy.logical_or(parcel.aggregate(urbansim_parcel.building.building_sqft), urbansim_parcel.parcel.is_land_use_type_vacant)'",
                              "dataset_pool": "dataset_pool"
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                               "coefficients_storage": "base_cache_storage",
                               "coefficients_table": "'real_estate_price_model_coefficients'"},
                "output": "(specification, coefficients)"
                },
            "run": {
                "arguments": {
                              "specification": "specification",
                              "coefficients":"coefficients",
                              "dataset": "parcel",
                              "data_objects": "datasets",
                              "run_config": "Resources({'exclude_missing_values_from_initial_error': True})"
                              }
                    },
            "prepare_for_estimate": {
                "name": "prepare_for_estimate",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                              "filter_variable":"'urbansim_parcel.parcel.unit_price'",
                              "dataset": "parcel",
                              "threshold": 1},
                "output": "(specification, index)"
                },
            "estimate": {
                "arguments": {
                              "specification": "specification",
                              "outcome_attribute": "'ln_unit_price=ln(urbansim_parcel.parcel.unit_price)'",
                              "dataset": "parcel",
                              "index": "index",
                              "data_objects": "datasets",
                              "debuglevel": 'debuglevel'
                              },
                "output": "(coefficients, dummy)"
                }
        
          },

         'employment_transition_model': 
                  EmploymentTransitionModelConfigurationCreator(
            location_id_name="building_id"
            ).execute(),
 
        'employment_relocation_model': 
                  EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               output_index = 'erm_index').execute(),
                                       
         'employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                estimation_weight_string = "pre_2001=building.year_built<=2000",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                estimation_size_agents = 0.01,
                                number_of_units_string = "total_SSS_job_space",
                                filter = "building.non_residential_sqft",
                                filter_for_estimation = "job.building_id",
                                portion_to_unplace = 0,
                                capacity_string = "vacant_SSS_job_space",
                                variable_package = "urbansim_parcel"
                                ).execute(),
                                       
            'home_based_employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                estimation_weight_string = "pre_2001=building.year_built<=2000",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                estimation_size_agents = 0.2,
                                number_of_units_string = "total_SSS_job_space",
                                filter = "numpy.logical_and(building.residential_units, building.sqft_per_unit)", 
                                filter_for_estimation = "numpy.logical_and(job.building_id>0, job.disaggregate(building.sqft_per_unit>0))",
                                portion_to_unplace = 0,
                                capacity_string = "vacant_SSS_job_space",
                                variable_package = "urbansim_parcel"
                                ).execute(),
                                       
          "business_transition_model" : {
                    "import": {"urbansim_parcel.models.business_transition_model":
                                    "BusinessTransitionModel"
                              },
                    "init": {
                        "name": "BusinessTransitionModel",
                        "arguments": {
                                      "debuglevel": 'debuglevel'
                                      },
                        },
                     "prepare_for_run": {
                         "name": "prepare_for_run",
                         "arguments": {"storage": "base_cache_storage",
                                       "in_table_name":"'annual_business_control_totals'",
                                       "id_name":"['year', 'building_use_id']"},
                         "output": "control_totals"
                        },
                    "run": {
                        "arguments": {
                            "year": "year",
                            "business_set": "business",
                            "control_totals": "control_totals",
                            }
                        }
                    },
        
          "business_relocation_model" : {
                    "import": {"urbansim.models.agent_relocation_model":
                                    "AgentRelocationModel"
                              },
                    "init": {
                        "name": "AgentRelocationModel",
                        "arguments": {
                                      "probabilities":"'urbansim_parcel.business_relocation_probabilities'",
                                      "model_name":"'Business Relocation Model'",
                                      "location_id_name":"'building_id'",
                                      "debuglevel": 'debuglevel'
                                      },
                        },
                    "prepare_for_run": {
                        "name": "prepare_for_run",
                        "arguments": {"what": "'business'",  "rate_storage": "base_cache_storage",
                                           "rate_table": "'annual_relocation_rates_for_business'"},
                        "output": "brm_resources"
                        },
                    "run": {
                        "arguments": {"agent_set": "business", "resources": "brm_resources"},
                        "output": "brm_index"
                        }
            },
        
         'business_location_choice_model': {
            "import": {"urbansim_parcel.models.business_location_choice_model":"BusinessLocationChoiceModel"},
            "init": {
                "name": "BusinessLocationChoiceModel",
                "arguments": {
                              "location_set":"building",
                              "model_name":"'Business Location Choice Model'",
                              "short_name":"'BLCM'",
                              "choices":"'urbansim.lottery_choices'",
                              "submodel_string":"'business.building_use_id'",
                              "filter": "'urbansim_parcel.building.building_sqft'",
                              "location_id_string":"'building_id'",
                              "run_config":"models_configuration['business_location_choice_model']",
                              "estimate_config":"models_configuration['business_location_choice_model']"
                     }},
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage", #"models_configuration['specification_storage']",
                              "specification_table": "models_configuration['business_location_choice_model']['specification_table']",
                              "coefficients_storage": "base_cache_storage", #"models_configuration['coefficients_storage']",
                              "coefficients_table": "models_configuration['business_location_choice_model']['coefficients_table']",
                              },
                "output": "(specification, coefficients)"
                },
        
            "run": {
                "arguments": {"specification": "specification",
                              "coefficients":"coefficients",
                              "agent_set": "business",
                              "agents_index": 'brm_index',
                              "data_objects": "datasets",
                              "chunk_specification":"{'records_per_chunk':1000}",
                              "debuglevel": 'debuglevel' }
                },
        # the estimate method is not availible before the estimation data is ready
            "prepare_for_estimate": {
                "name": "prepare_for_estimate",
                "arguments": {
                              "agent_set":"business",
                              "join_datasets": "False",
                              "agents_for_estimation_storage": "base_cache_storage",
                              "agents_for_estimation_table": "'business_for_estimation'",
                              "filter":None,
                              "index_to_unplace":  "brm_index",
                              "portion_to_unplace": 1/12.0,
                              "data_objects": "datasets"
                                },
                "output": "(specification, index)"
                },
            "estimate": {
                "arguments": {
                              "specification": "specification",
                              "agent_set": "business",
                             "agents_index": "index",
                              "data_objects": "datasets",
                              "debuglevel": 'debuglevel'},
                "output": "(coefficients, dummy)"
                },
           },
        
           #'building_transition_model': {
                    #"import": {"urbansim_parcel.models.building_transition_model": "BuildingTransitionModel"},
                    #"init": {"name": "BuildingTransitionModel"},
                    #"run": {"arguments": {
                                  #"building_set": "building",
        ##                          "building_types_table": "building_type",
                                  #"building_use_classification_table":"building_use_classification",
                                  #"vacancy_table": "target_vacancy",
                                  #"history_table": "development_event_history",
                                  #"year": "year",
                                  #"location_set": "parcel",
                                  #"resources": "model_resources"
                            #},
                            #"output": "new_building_index",
                    #}
                  #},
        
           #'building_location_choice_model':{
                        #"group_by_attribute": ("building_use_classification", "name"),
                        #"import": {"urbansim_parcel.models.building_location_choice_model":
                                            #"BuildingLocationChoiceModel",
                                    #},
                        #"init": {
                            #"name": "BuildingLocationChoiceModel",
                            #"arguments": {
                                #"location_set" : "parcel",
                                #"submodel_string" : "'building.building_use_id'",
                                #"capacity_string" : "'UNITS_capacity'",
                                #"filter" : None,
                                #"developable_maximum_unit_variable" : "'UNITS_capacity'", #"developable_maximum_UNITS",
                                #"developable_minimum_unit_variable" : None, # None means don't consider any minimum. For default, set it to empty string
                                #"agents_grouping_attribute":"'urbansim_parcel.building.building_class_id'",
                                #"estimate_config" : {'weights_for_estimation_string':"'urbansim_parcel.parcel.uniform_capacity'"},
                                #"run_config":{"agent_units_string" : "urbansim_parcel.building.building_size"}
                                #}
                            #},
                        #"prepare_for_run": {
                            #"name": "prepare_for_run",
                        #"arguments": {"specification_storage": "base_cache_storage",
                                      #"specification_table": "'building_location_choice_model_specification'",
                                      #"coefficients_storage": "base_cache_storage",
                                      #"coefficients_table": "'building_location_choice_model_coefficients'",
                                      #},
                            #"output": "(specification, coefficients)"
                            #},
                        #"run": {
                            #"arguments": {"specification": "specification",
                                          #"coefficients":"coefficients",
                                          #"agent_set": "building",
                                          #"agents_index": "new_building_index",  #?
                                          #"data_objects": "datasets" ,
                                          #"chunk_specification":"{'records_per_chunk':500}"}
                            #},
        
                        #"prepare_for_estimate": {
                            #"name": "prepare_for_estimate",
                            #"arguments": {"specification_storage": "base_cache_storage",
                                          #"specification_table": "'development_location_choice_model_specification'",
                                          #"building_set":"building",
                                          #"buildings_for_estimation_storage": "base_cache_storage",
                                          #"buildings_for_estimation_table": "'development_event_history'",
                                          #"constants": "urbansim_constant",
                                          #"base_year":"resources['base_year']",
        ##                                 "building_categories":None, #"{'residential': array([1,2,3,5,10,20]), 'commercial': 1000*array([1, 2, 5, 10]), 'industrial': 1000*array([1,2,5,10])}",
        ##                                 "id_name":"['building_id','scheduled_year']",
                                          #"data_objects": "datasets",
                                               #},
                            #"output": "(specification, index)"
                                #},
                        #"estimate": {
                                #"arguments": {"specification": "specification",
                                              #"agent_set": "building",
                                              #"agents_index":"index",
                                              #"data_objects": "datasets"},
                                 #"output": "(coefficients, dummy)"
                           #}
                 #},
        
                "household_relocation_model" : {
                    "import": {"urbansim.models.household_relocation_model_creator":
                                    "HouseholdRelocationModelCreator"
                              },
                    "init": {
                        "name": "HouseholdRelocationModelCreator().get_model",
                        "arguments": {
                                      "debuglevel": 'debuglevel',
                                      "location_id_name": "'building_id'",
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
                    },
                "process_pipeline_events":{
                     "import": {"urbansim_parcel.models.process_pipeline_events":
                                                         "ProcessPipelineEvents"},
                     "init": {
                        "name": "ProcessPipelineEvents"},
                     "run": {
                        "arguments": {'building_dataset': 'building',
                                      'year':'year',
                                      "storage": "base_cache_storage"},
                        "output": "scheduled_development_events"
                        }
                 },
        
        # configuration for parcel-based developer model
         'expected_sale_price_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_regression_model":
                       "DevelopmentProjectProposalRegressionModel"},
            "init": {
                "name": "DevelopmentProjectProposalRegressionModel",
                "arguments": {"submodel_string": "'land_use_type_id=development_project_proposal.disaggregate(parcel.land_use_type_id)'", 
                              #"submodel_string": "'building_type_id=development_project_proposal.disaggregate(development_template.building_type_id)'", 
                              #"filter_attribute": "'urbansim_parcel.development_project_proposal.is_viable'",
                              "filter_attribute": "'urbansim_parcel.development_project_proposal.is_size_fit'",
                              "outcome_attribute_name":"'ln_unit_price_expected'",
                              "dataset_pool": "dataset_pool"
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"parcel_filter":"'is_vacant_developable=parcel.land_use_type_id==26'",
                              "specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                               "coefficients_storage": "base_cache_storage",
                               "coefficients_table": "'real_estate_price_model_coefficients'",
                               "spec_replace_module_variable_pair": "('psrc_parcel.estimation.repm_specification', 'variables_for_development_project_proposal')",
                               "dataset_pool": "dataset_pool",},
                "output": "(development_project_proposal, specification, coefficients)"
                },
            "run": {
                "arguments": {
                              "specification": "specification",
                              "coefficients":"coefficients",
                              "dataset": 'development_project_proposal',  
                              "data_objects": "datasets" },
                "output":"development_project_proposal"  #get the development project proposal back
                    },
          },

         'development_proposal_choice_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_sampling_model":
                       "DevelopmentProjectProposalSamplingModel"},
            "init": {
                "name": "DevelopmentProjectProposalSamplingModel",
                "arguments": {"proposal_set": "development_project_proposal",
                              #weight_string omitted to use defalut value "exp_ROI = exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",                      
                              "filter_attribute": None, # the filter has been handled in the process of creating proposal set 
                                                        # (prepare_for_run in expected_sale_price_model)
                              },
                },
            "run": {
                "arguments": {'n':500,  # sample 500 proposal at a time, evaluate them one by one
                              },
                "output":"development_project_proposal"
                    },
          },
                                       
         'building_construction_model': {
             "import": {"urbansim_parcel.models.building_construction_model":
                       "BuildingConstructionModel"},
             "init": {
                "name": "BuildingConstructionModel"
                },
             "run": {
                "arguments": {
                   "development_proposal_set": "development_project_proposal",
                   "building_dataset": "building",
                   "dataset_pool": "dataset_pool"
                   }
                 }
          },

#        "household_location_choice_model": 
#                  'HouseholdLocationChoiceModelConfigurationCreator(
#                                location_set = "building",
#                                sampler = "opus_core.samplers.weighted_sampler",
#                                input_index = 'hrm_index',
#                                submodel_string = None,
#                                capacity_string = "urbansim_parcel.building.vacant_residential_units",
#                                nchunks=12,
#                                lottery_max_iterations=20
#                                ).execute(),

        }
        
        for model in my_controller_configuration.keys():
            if model not in self["models_configuration"].keys():
                self["models_configuration"][model] = {}
            self['models_configuration'][model]['controller'] = my_controller_configuration[model]
        
        #BLDGLCM
        #bldglcm_controller = config["models_configuration"]["building_location_choice_model"]["controller"]
        ##bldglcm_controller = Configuration()
        #
        #config["models_configuration"]['building_location_choice_model']["controller"].merge(bldglcm_controller)
        #HLCM
        hlcm_controller = self["models_configuration"]["household_location_choice_model"]["controller"]
        hlcm_controller["init"]["arguments"]["location_set"] = "building"
        hlcm_controller["init"]["arguments"]["location_id_string"] = "'building_id'"
        hlcm_controller["init"]["arguments"]["estimate_config"] = {"weights_for_estimation_string":"building.residential_units"} #"urbansim.zone.vacant_residential_units"
#       hlcm_controller["init"]["arguments"]["run_config"] = {"capacity_string":"urbansim_parcel.building.vacant_residential_units"}
        hlcm_controller["init"]["arguments"]["capacity_string"] = "'vacant_residential_units'"
        hlcm_controller["init"]["arguments"]['sample_size_locations']=30
        hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
        hlcm_controller["init"]["arguments"]["submodel_string"] = None #"'household_size'"
        hlcm_controller["init"]["arguments"]["estimation_size_agents"] = 0.005
        hlcm_controller["init"]["arguments"]["number_of_units_string"] = None
        hlcm_controller["init"]["arguments"]["variable_package"] = "'urbansim_parcel'"
        hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(building.residential_units, building.sqft_per_unit)'"
        hlcm_controller["prepare_for_estimate"]["arguments"]["agents_for_estimation_table"] = None
        hlcm_controller["prepare_for_estimate"]["arguments"]["filter"] = "'numpy.logical_and(household.building_id>0, household.disaggregate(building.sqft_per_unit>0))'" # filtering out agents for estimation with valid location
        hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = True
        hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = None
        #hlcm_controller["estimate"]["arguments"]["procedure"] = 'None'
        models_configuration['household_location_choice_model']["controller"].replace(hlcm_controller)
                
        self["datasets_to_preload"] = {
                'zone':{},
                'household':{},
                'building':{},
                'parcel':{'package_name':'urbansim_parcel'},
        #        'business':{'package_name':'urbansim_parcel'},
        #        'person':{'package_name':'urbansim_parcel'},
                "building_type":{'package_name':'urbansim_parcel'},
                'travel_data':{}
                }
        
        #config["datasets_to_preload"]['business'] = {'package_name':'urbansim_parcel'}
        #config["base_year"] = 2001
        

        
config = UrbansimParcelConfiguration()