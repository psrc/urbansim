# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

#from urbansim.estimation.config import config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from numpy import array
import os
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange

run_configuration = AbstractUrbansimConfiguration()
models_configuration = run_configuration['models_configuration']

config_changes = {
    'landuse_development_types':{
        'residential':{
            'units':'residential_units',
            'residential':True,
            },
        'commercial':{
            'units':'commercial_sqft',
            'residential':False,                  
            },
        'industrial':{
            'units':'industrial_sqft',
            'residential':False,                         
            },
        'governmental':{
            'units':'governmental_sqft',
            'residential':False,                         
            },
     },
    'events_coordinator':{
        'default_type_of_change':DevelopmentEventTypeOfChange.REPLACE,
        },
  }
models_configuration.merge(config_changes)

my_controller_configuration = {
 'housing_price_model': {
    "import": {"urbansim.models.housing_price_model":
                                        "HousingPriceModel"},
    "init": { 
        "name": "HousingPriceModel" },
    "prepare_for_run": {
        "name": "prepare_for_run",
        "arguments": {"specification_storage": "base_cache_storage",
                      "specification_table": "'housing_price_model_specification'",
                       "coefficients_storage": "base_cache_storage",
                       "coefficients_table": "'housing_price_model_coefficients'"},
        "output": "(specification, coefficients)"
        },
    "run": {                 
        "arguments": {
                      "specification": "specification",
                      "coefficients":"coefficients",
                      "dataset": "gridcell",
                      "data_objects": "datasets" }
            },
    "prepare_for_estimate": {
        "name": "prepare_for_estimate",
        "arguments": {"specification_storage": "base_cache_storage",
                      "specification_table": "'housing_price_model_specification'",
                      "dataset": "gridcell", 
                      "threshold": 1},
        "output": "(specification, index)"
        },
    "estimate": {
        "arguments": {
                      "specification": "specification",
                      "dataset": "gridcell",
                      "index": "index",
                      "data_objects": "datasets",
                      "debuglevel": run_configuration['debuglevel']
                      },
        "output": "(coefficients, dummy)"
        }                                  

  },

  "development_transition_model": {
    "import":{"randstad.models.development_transition_model":"DevelopmentTransitionModel"},
    "init": { 
        "name": "DevelopmentTransitionModel"                                      
        },
    "run": {
        "arguments": {
#            "model_configuration": "model_configuration",
            "vacancy_table": "target_vacancy", 
            "frequency_table": "development_event_frequency",
            "template_table": "development_event_template",
            "year": "year",
            "location_set": "gridcell", 
            "resources": "datasets"
            },
        "output": "dptm_results"
        }
  },
 'landuse_development_location_choice_model': {
        "import":{"randstad.models.landuse_development_location_choice_model_creator":
                                            "LandUseDevelopmentLocationChoiceModelCreator"},                                       
        "init": { 
            "name": "LandUseDevelopmentLocationChoiceModelCreator().get_model",
            "arguments": {
                "location_set": "gridcell",
                }
            },
        "prepare_for_run": {
            "name": "prepare_for_run",
            "arguments": {"specification_storage": "base_cache_storage",
                      "specification_table": "'landuse_development_location_choice_model_specification'",
                      "coefficients_storage": "base_cache_storage",
                      "coefficients_table": "'landuse_development_location_choice_model_coefficients'",
                     },
            "output": "(specification, coefficients)"
            },
        "run": {                 
            "arguments": {"specification": "specification",
                          "coefficients":"coefficients",
                          "agent_set": "dptm_results",
                          "data_objects": "datasets" }
            },
        "prepare_for_estimate": {
            "name": "prepare_for_estimate",
            "arguments": {"specification_storage": "base_cache_storage",
                          "specification_table": "'landuse_development_location_choice_model_specification'",
                          "events_for_estimation_storage": "base_cache_storage",
                          "events_for_estimation_table": "'development_event_history'",
                          },
            "output": "(specification, development)"
                },
        "estimate": {
                "arguments": {"specification": "specification",
                              "agent_set": "development",
                              "data_objects": "datasets",
                              "debuglevel": run_configuration['debuglevel']},
                 "output": "(coefficients, dummy)"
           }   

    },
   "development_event_transition_model": {
    "import":{"randstad.models.development_event_transition_model":"DevelopmentEventTransitionModel"},
    "init": { 
        "name": "DevelopmentEventTransitionModel"                                      
        },
    "prepare_for_run": {
        "name": "prepare_for_run",
        "arguments": {
            "model_configuration": "model_configuration"
            },                                  
        "output": "(all_types, all_units)"
        },                                          
    "run": {
        "arguments": {
            "developments":"dptm_results",
            "landuse_types":"all_types",
            "units":"all_units",
            "year": "year"
            },
        "output": "development_events"   
        }
    },
  "divide_jobs_model":{
    "import":{"urbansim.models.divide_jobs_model":"DivideJobsModel"},
    "init": { 
        "name": "DivideJobsModel",
        },
    "prepare_for_run": {
        "name": "prepare_for_run",
        "arguments": {
            "storage": "base_cache_storage",
            "comm_spec_table":"'employment_commercial_location_choice_model_specification'", 
            "ind_spec_table":"'employment_industrial_location_choice_model_specification'", 
            "hb_spec_table":None
            },
        "output": "(elcm_com_submodels, elcm_ind_submodels, elcm_hb_submodels, commercial_specification, industrial_specification, home_based_specification)",
        },
    "run": {                 
        "arguments": {"job_set": "job", "index":"erm_index",
                      "sectors_hb": "elcm_hb_submodels", 
                      "sectors_nhbcom": "elcm_com_submodels", "sectors_nhbind":"elcm_ind_submodels", 
                      "resources": "model_resources"},
        "output":"divided_job_indices"
        }
    },
 
    "events_coordinator":{
    "import": {"randstad.models.events_coordinator":
                    "EventsCoordinator"},
    "init": {
        "name": "EventsCoordinator"},
    "run": {
        "arguments": {
            "model_configuration": "model_configuration",
            "location_set": "gridcell",
            "development_event_set": "development_events",
            "development_type_set": "development_type",
            "current_year": "year"
            },
        "output": "(changed_indices, processed_development_event_indices)"
        }
    }
 
}

for model in my_controller_configuration.keys():
    if model not in run_configuration["models_configuration"].keys():
        run_configuration["models_configuration"][model] = {}    
    models_configuration[model]['controller'] = my_controller_configuration[model]
