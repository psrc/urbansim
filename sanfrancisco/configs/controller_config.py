# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim.estimation.config import config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from opus_core.configuration import Configuration
import os

config = AbstractUrbansimConfiguration()
models_configuration = config['models_configuration']

models_configuration["business_location_choice_model"] = {
                     "estimation":"opus_core.bhhh_mnl_estimation",
                     "sampler":"opus_core.samplers.weighted_sampler",
                     "sample_size_locations":50,
#                     "weights_for_estimation_string":"urbansim.zone.number_of_non_home_based_jobs",
                     "specification_table":"business_location_choice_model_specification",
                     "coefficients_table":"business_location_choice_model_coefficients",
                     "compute_capacity_flag":True,
                     "capacity_string":"building.non_residential_sqft",
                     "number_of_agents_string":"business.sqft",
                     "number_of_units_string":"sanfrancisco.building.vacant_non_residential_sqft",
   }

my_controller_configuration = {
 'real_estate_price_model': {
    "import": {"urbansim.models.real_estate_price_model":
                                        "RealEstatePriceModel"},
    "init": {
        "name": "RealEstatePriceModel",
        "arguments": {"submodel_string": "'building_use_id'",
                      "outcome_attribute":"'ln_unit_price=ln(building.unit_price)'",
                      "filter_attribute": None}, # "'valid'"}, # 
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
                      "dataset": "building",
                      "data_objects": "datasets" }
            },
    "prepare_for_estimate": {
        "name": "prepare_for_estimate",
        "arguments": {"specification_storage": "base_cache_storage",
                      "specification_table": "'real_estate_price_model_specification'",
                      "filter_variable":"'building.unit_price'",
                      "dataset": "building",
                      "threshold": 0},
        "output": "(specification, index)"
        },
    "estimate": {
        "arguments": {
                      "specification": "specification",
 #                     "procedure": None, #Diagnostics
                      "outcome_attribute": "'ln_unit_price=ln(building.unit_price)'",
                      "dataset": "building",
                      "index": "index",
                      "data_objects": "datasets",
                      "debuglevel": config['debuglevel']
                      },
        "output": "(coefficients, dummy)"
        }

  },

  "business_transition_model" : {
            "import": {"sanfrancisco.models.business_transition_model":
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
                               "id_name":"['year', 'sector_id']"},
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
                              "probabilities":"'sanfrancisco.business_relocation_probabilities'",
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
    "import": {"sanfrancisco.models.business_location_choice_model":"BusinessLocationChoiceModel"},
    "init": {
        "name": "BusinessLocationChoiceModel",
        "arguments": {
                      "location_set":"building",
                      "model_name":"'Business Location Choice Model'",
                      "short_name":"'BLCM'",
                      "choices":"'urbansim.lottery_choices'",
                      "submodel_string":"'business.sector_id'",
                      "filter": None, #"'building.unit_price > 1'",
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
        "output": "(specification, coefficients, _index)"
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
                      "index_to_unplace":  "None",
                      "portion_to_unplace": 1/12.0,
                      "data_objects": "datasets"
                        },
        "output": "(specification, index)"
        },
    "estimate": {
        "arguments": {
                      "specification": "specification",
                      "procedure": None,
                      "agent_set": "business",
                     "agents_index": "index",
                      "data_objects": "datasets",
                      "debuglevel": config['debuglevel']},
        "output": "(coefficients, dummy)"
        },
   },

   'building_transition_model': {
            "import": {"sanfrancisco.models.building_transition_model": "BuildingTransitionModel"},
            "init": {"name": "BuildingTransitionModel"},
            "run": {"arguments": {
                          "building_set": "building",
#                          "building_types_table": "building_type",
                          "building_use_classification_table":"building_use_classification",
                          "vacancy_table": "target_vacancy",
                          "history_table": "development_event_history",
                          "year": "year",
                          "location_set": "parcel",
                          "resources": "model_resources"
                    },
                    "output": "new_building_index",
            }
          },

   'building_location_choice_model':{
                "group_by_attribute": ("building_use_classification", "name"),
                "import": {"sanfrancisco.models.building_location_choice_model":
                                    "BuildingLocationChoiceModel",
                            },
                "init": {
                    "name": "BuildingLocationChoiceModel",
                    "arguments": {
                        "location_set" : "parcel",
                        "submodel_string" : "'building.building_use_id'",
                        "capacity_string" : "'UNITS_capacity'",
                        "filter" : None, # will be set internally
                        "number_of_agents_string":"'sanfrancisco.parcel.UNITS'",
                        #"number_of_units_string":"'sanfrancisco.parcel.UNITS_capacity'",
                        "number_of_units_string":None,
                        "developable_maximum_unit_variable" : "'UNITS_capacity'", #"developable_maximum_UNITS",
                        "developable_minimum_unit_variable" : None, # None means don't consider any minimum. For default, set it to empty string
                        "agents_grouping_attribute":"'sanfrancisco.building.building_class_id'",
                        "estimate_config" : {'weights_for_estimation_string': None}, #"'sanfrancisco.parcel.uniform_capacity'"},
                        "run_config":{"agent_units_string" : "sanfrancisco.building.building_size"},
                        "dataset_pool": "dataset_pool" 
                        }
                    },
                "prepare_for_run": {
                    "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'building_location_choice_model_specification'",
                              "coefficients_storage": "base_cache_storage",
                              "coefficients_table": "'building_location_choice_model_coefficients'",
                              },
                    "output": "(specification, coefficients)"
                    },
                "run": {
                    "arguments": {"specification": "specification",
                                  "coefficients":"coefficients",
                                  "agent_set": "building",
                                  "agents_index": "new_building_index",  #?
                                  "data_objects": "datasets" ,
                                  "chunk_specification":"{'records_per_chunk':500}"}
                    },

                "prepare_for_estimate": {
                    "name": "prepare_for_estimate",
                    "arguments": {"specification_storage": "base_cache_storage",
                                  "specification_table": "'development_location_choice_model_specification'",
                                  "building_set":"building",
                                  "buildings_for_estimation_storage": "base_cache_storage",
                                  "buildings_for_estimation_table": "'development_event_history'",
                                  "constants": "urbansim_constant",
                                  "base_year":"resources['base_year']",
#                                 "building_categories":None, #"{'residential': array([1,2,3,5,10,20]), 'commercial': 1000*array([1, 2, 5, 10]), 'industrial': 1000*array([1,2,5,10])}",
#                                 "id_name":"['building_id','scheduled_year']",
                                  "data_objects": "datasets",
                                       },
                    "output": "(specification, index)"
                        },
                "estimate": {
                        "arguments": {"specification": "specification",
                                      "agent_set": "building",
                                      "agents_index":"index",
                                      "data_objects": "datasets"},
                         "output": "(coefficients, dummy)"
                   }
         },
         
        'household_transition_model': {
            'import': {
                'urbansim.models.household_transition_model': 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'location_id_name':'"building_id"',
                              'debuglevel':'debuglevel'},
                'name': 'HouseholdTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': '(control_totals, characteristics)'
                },
            'run': {
                'arguments': {
                    'year': 'year',
                    'household_set': 'household',
                    'control_totals': 'control_totals',
                    'characteristics': 'characteristics',
                    }
                }
            },
         
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
             "import": {"sanfrancisco.models.process_pipeline_events":
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

##HLCM
        "household_location_choice_model":{
            "import": {"urbansim.models.household_location_choice_model_creator":
                        "HouseholdLocationChoiceModelCreator",
                      },
            "init": {
                "name": "HouseholdLocationChoiceModelCreator().get_model",
                "arguments": {"location_set": "building",
                              "location_id_string":"'building_id'",
                              "choices":"'urbansim.lottery_choices'",
                              "submodel_string":"'sanfrancisco.household.household_size_category'",
                              "sample_size_locations":50,
                              "dataset_pool": "dataset_pool",
                              "run_config":{"capacity_string" : "sanfrancisco.building.vacant_residential_units",
                                            "number_of_agents_string": "sanfrancisco.building.number_of_households",
                                            "number_of_units_string": "building.residential_units",
                                            },
                              "estimate_config":{"weights_for_estimation_string" : None,
                                            }
                              }
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'household_location_choice_model_specification'",
                              "coefficients_storage": "base_cache_storage",
                              "coefficients_table": "'household_location_choice_model_coefficients'",
                              },
                "output": "(specification, coefficients)"
                },
            "run": {
                "arguments": {"specification": "specification",
                              "coefficients":"coefficients",
                              "agent_set": "household",
                              "agents_index": "hrm_index",
                              "data_objects": "datasets",
                              "chunk_specification":"{'nchunks':12}",
                              "debuglevel": "debuglevel" }
                },
            "prepare_for_estimate": {
                "name": "prepare_for_estimate",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'household_location_choice_model_specification'",
                              "agent_set": "household",
                              "agents_for_estimation_storage": "base_cache_storage",
                              "agents_for_estimation_table": "'households_for_estimation'",
                              "join_datasets": "True",
                              "index_to_unplace":  None,
                              "portion_to_unplace": 1/12.0,
                              "data_objects": "datasets"
                                  },
                "output": "(specification, index)"
                },
            "estimate": {
                "arguments": {"specification": "specification",
                              "procedure": None, # Only for diagnostic purposes
                              "agent_set": "household",
                              "agents_index": "index",
                              "data_objects": "datasets",
                              "debuglevel": "debuglevel"},
                 "output": "(coefficients, dummy)"
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
#hlcm_controller = config["models_configuration"]["household_location_choice_model"]["controller"]
#hlcm_controller["init"]["arguments"]["location_set"] = "building"
#hlcm_controller["init"]["arguments"]["location_id_string"] = "'building_id'"
#hlcm_controller["init"]["arguments"]["estimate_config"] = {"weights_for_estimation_string":None} #"urbansim.zone.vacant_residential_units"
#hlcm_controller["init"]["arguments"]["run_config"] = {"capacity_string":"sanfrancisco.building.vacant_residential_units"} #"urbansim.zone.vacant_residential_units"
#hlcm_controller["init"]["arguments"]['sample_size_locations']=50
#hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
#hlcm_controller["controller"]["init"]["arguments"]["submodel_string"] = "'household_size'"
#hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
#hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'
#config["models_configuration"]['household_location_choice_model']["controller"].merge(hlcm_controller)


config["datasets_to_preload"] = {
        'zone':{},
        'household':{},
        'building':{},
        'parcel':{'package_name':'sanfrancisco'},
        'business':{'package_name':'sanfrancisco'},
        'person':{'package_name':'sanfrancisco'},
        "building_use":{'package_name':'sanfrancisco'},
        "building_use_classification":{'package_name':'sanfrancisco'},
        'travel_data':{}
        }

#config["datasets_to_preload"]['business'] = {'package_name':'sanfrancisco'}
#config["base_year"] = 2001
