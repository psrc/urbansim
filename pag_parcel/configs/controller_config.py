# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

#from urbansim.estimation.config import config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from opus_core.configuration import Configuration
from numpy import array
import os

config = AbstractUrbansimConfiguration()
models_configuration = config['models_configuration']

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
                      "filter_attribute": "'numpy.logical_or(parcel.aggregate(urbansim_parcel.building.building_sqft), urbansim_parcel.parcel.is_land_use_type_vacant)'"
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
                      "debuglevel": config['debuglevel']
                      },
        "output": "(coefficients, dummy)"
        }

  },

  "business_transition_model" : {
            "import": {"pag_parcel.models.business_transition_model":
                            "BusinessTransitionModel"
                      },
            "init": {
                "name": "BusinessTransitionModel",
                "arguments": {
                              "debuglevel": config['debuglevel']
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
                              "probabilities":"'pag_parcel.business_relocation_probabilities'",
                              "model_name":"'Business Relocation Model'",
                              "location_id_name":"'building_id'",
                              "debuglevel": config['debuglevel']
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
    "import": {"pag_parcel.models.business_location_choice_model":"BusinessLocationChoiceModel"},
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
                      "debuglevel": config['debuglevel'] }
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
                      "debuglevel": config['debuglevel']},
        "output": "(coefficients, dummy)"
        },
   },

   #'building_transition_model': {
            #"import": {"pag_parcel.models.building_transition_model": "BuildingTransitionModel"},
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
                #"import": {"pag_parcel.models.building_location_choice_model":
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
                              "debuglevel": config['debuglevel'],
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
             "import": {"pag_parcel.models.process_pipeline_events":
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
    "import": {"pag_parcel.models.development_project_proposal_regression_model":
               "DevelopmentProjectProposalRegressionModel"},
    "init": {
        "name": "DevelopmentProjectProposalRegressionModel",
        "arguments": {"submodel_string": "'land_use_type_id=development_project_proposal.disaggregate(parcel.land_use_type_id)'", 
                      #"submodel_string": "'building_type_id=development_project_proposal.disaggregate(development_template.building_type_id)'", 
                      "filter_attribute": "'pag_parcel.development_project_proposal.is_viable'",
                      "outcome_attribute_name":"'ln_unit_price_expected'",
                      "dataset_pool": "dataset_pool"
                      },
        },
    "prepare_for_run": {
        "name": "prepare_for_run",
        "arguments": {"parcel_filter":"'is_vacant_developable=numpy.logical_and(parcel.land_use_type_id==21, numpy.logical_and(parcel.plan_type_id != 18, parcel.plan_type_id != 2))'",
                      "specification_storage": "base_cache_storage",
                      "specification_table": "'real_estate_price_model_specification'",
                       "coefficients_storage": "base_cache_storage",
                       "coefficients_table": "'real_estate_price_model_coefficients'",
                       "spec_replace_module_variable_pair": "('pag_parcel.estimation.repm_specification', 'variables_for_development_project_proposal')",
                       "dataset_pool": "dataset_pool",},
        "output": "(proposal_set, specification, coefficients)"
        },
    "run": {
        "arguments": {
                      "specification": "specification",
                      "coefficients":"coefficients",
                      "dataset": 'proposal_set',  
                      "data_objects": "datasets" },
        "output":"proposal_set"  #get the development project proposal back
            },
  },
 'development_proposal_choice_model': {
    "import": {"pag_parcel.models.development_project_proposal_sampling_model":
               "DevelopmentProjectProposalSamplingModel"},
    "init": {
        "name": "DevelopmentProjectProposalSamplingModel",
        "arguments": {"proposal_set": "proposal_set",
                      #weight_string omitted to use defalut value "exp_ROI = exp(pag_parcel.development_project_proposal.expected_rate_of_return_on_investment)",                      
                      "filter_attribute": None, # the filter has been handled in the process of creating proposal set 
                                                # (prepare_for_run in expected_sale_price_model)
                      },
        },
    "run": {
        "arguments": {'n':500,  # sample 500 proposal at a time, evaluate them one by one
                      },
        "output":"scheduled_development_events"
            },
  },
                               
 'building_construction_model': {
     "import": {"pag_parcel.models.building_construction_model":
               "BuildingConstructionModel"},
     "init": {
        "name": "BuildingConstructionModel"
        },
     "run": {
        "arguments": {
           "development_proposal_set": "proposal_set",
           "building_dataset": "building",
           "dataset_pool": "dataset_pool"
           }
         }
  }
}

for model in my_controller_configuration.keys():
    if model not in config["models_configuration"].keys():
        config["models_configuration"][model] = {}
    models_configuration[model]['controller'] = my_controller_configuration[model]

#BLDGLCM
#bldglcm_controller = config["models_configuration"]["building_location_choice_model"]["controller"]
##bldglcm_controller = Configuration()
#
#config["models_configuration"]['building_location_choice_model']["controller"].merge(bldglcm_controller)


#HLCM
hlcm_controller = config["models_configuration"]["household_location_choice_model"]["controller"]
hlcm_controller["init"]["arguments"]["location_set"] = "building"
hlcm_controller["init"]["arguments"]["location_id_string"] = "'building_id'"
hlcm_controller["init"]["arguments"]["estimate_config"] = {"weights_for_estimation_string":"building.residential_units"} #"urbansim.zone.vacant_residential_units"
hlcm_controller["init"]["arguments"]["run_config"] = {"capacity_string":"urbansim_parcel.building.vacant_residential_units"} #"urbansim.zone.vacant_residential_units"
hlcm_controller["init"]["arguments"]['sample_size_locations']=30
hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
hlcm_controller["controller"]["init"]["arguments"]["submodel_string"] =  None #"'household_size'"
hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
config["models_configuration"]['household_location_choice_model']["controller"].merge(hlcm_controller)


config["datasets_to_preload"] = {
#        'zone':{},
        #'household':{},
        'building':{},
        'parcel':{'package_name':'pag_parcel'},
#        'business':{'package_name':'pag_parcel'},
#        'person':{'package_name':'pag_parcel'},
        "building_type":{'package_name':'pag_parcel'},
#        'travel_data':{}
        }

#config["datasets_to_preload"]['business'] = {'package_name':'pag_parcel'}
#config["base_year"] = 2001
