# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from opus_core.resources import merge_resources_if_not_None
import copy

"""this configuration file specifying workplace choice models: 
home_based_workplace_choice_model, workplace_choice_model_for_residents, 
workplace_choice_model_for_immigrants, and 
simple models keeping consistency between persons and households/jobs.
Home base choice model is defined in urbansim.configs.general_configuration_with_changed_elcm
"""
config = AbstractUrbansimConfiguration()

wlcm_model_configuration = {
                       "estimation":"opus_core.bhhh_mnl_estimation",
                       "sampler":"opus_core.samplers.weighted_sampler",
                       "sample_size_locations":30,
#                       "weights_for_estimation_string":"urbansim.zone.number_of_non_home_based_jobs",
                       "compute_capacity_flag":True,
                       "capacity_string":"psrc.job.capacity",
                       "number_of_units_string":"psrc.job.capacity",
                       }
run_configuration = config.copy()
run_configuration['models_configuration']['workplace_choice_model_for_resident']= wlcm_model_configuration
    
my_controller_configuration = {
 'household_person_consistency_keeper':{
    "import": {"psrc.models.persons_consistency_keeper_model":"PersonDatasetConsistencyKeeperModel"},
    "init": { 
        "name": "PersonDatasetConsistencyKeeperModel",
        "arguments": {},
     },               
    "run": {
        "arguments": {"household_set": "household",
                      "person_set":"person",
                      "expand_person_set":True,
                      }
        },
    },
 'job_person_consistency_keeper':{
    "import": {"psrc.models.persons_consistency_keeper_model":"PersonDatasetConsistencyKeeperModel"},
    "init": { 
        "name": "PersonDatasetConsistencyKeeperModel",
        "arguments": {},
     },                                  
    "run": {
        "arguments": {"job_set": "job",
                      "person_set":"person",
                      "expand_person_set":False,
                      }
        },
    },
 'workplace_choice_model_for_resident': {
    "import": {"urbansim.models.agent_location_choice_model":"AgentLocationChoiceModel"},
    "init": { 
        "name": "AgentLocationChoiceModel",
        "arguments": {
                      "location_set":"job",
                      "model_name":"'Non-home-based Work Choice Model for residents'",
                      "short_name":"'NHBWLCM'",
                      "choices":"'urbansim.lottery_choices'",
                      "submodel_string":"'psrc.person.household_income'",
                      "filter": "'psrc.job.is_untaken_non_home_based_job'",
                      "location_id_string":"'job_id'",
                      "run_config":"models_configuration['workplace_choice_model_for_resident']",
                      "estimate_config":"models_configuration['workplace_choice_model_for_resident']"
             }},
    "prepare_for_run": {
        "name": "prepare_for_run",
        "arguments": {"specification_storage": "base_cache_storage", #"models_configuration['specification_storage']",
                      "specification_table": "'workplace_choice_model_for_resident_specification'",
                      "coefficients_storage": "base_cache_storage", #"models_configuration['coefficients_storage']",
                      "coefficients_table": "'workplace_choice_model_for_resident_coefficients'",
                      },
        "output": "(specification, coefficients)"
        },
    "run": {
        "arguments": {"specification": "specification",
                      "coefficients":"coefficients",
                      "agent_set": "person",
                      "agents_index": None,
                      "agents_filter":"'psrc.person.is_non_home_based_worker_without_job'",
                      "data_objects": "datasets",
                      "chunk_specification":"{'records_per_chunk':5000}",
                      "debuglevel": run_configuration['debuglevel'] }
        },

# the estimate method is not availible before the estimation data is ready
#    "prepare_for_estimate": {
#        "name": "prepare_for_estimate",
#        "arguments": {
#                      "agent_set":"person",
#                      "join_datasets": "True",
#                      "agents_for_estimation_storage": "base_cache_storage",
#                      "agents_for_estimation_table": "'persons'",                      
#                      "filter":None,
#                      "data_objects": "datasets"
#                        },
#        "output": "(specification, index)"
#        },
#    "estimate": {
#        "arguments": {          
#                      "specification": "specification",
#                      "agent_set": "person",
#                     "agents_index": "index",
#                      "data_objects": "datasets",
#                      "debuglevel": run_configuration['debuglevel']},
#        "output": "(coefficients, dummy)"
#        },  
      },
    "job_change_model":{
            "import": {"urbansim.models.agent_relocation_model":
                            "AgentRelocationModel"
                      },
                                            
            "init": {
                "name": "AgentRelocationModel",
                "arguments": {"choices":"opus_core.random_choices",
                              "probabilities":"opus_core.upc.rate_based_probabilities",
                              "location_id_name":"job_id",
                              "model_name":"job change model",
                              "debuglevel": config['debuglevel']
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"what": "'person'",  "rate_storage": "base_cache_storage",
                                   "rate_table": "'annual_job_change_rates_for_workers'"},
                "output": "jcm_resources"
                },
            "run": {
                "arguments": {"agent_set": "person", "resources": "jcm_resources"},
                "output": "jcm_index"
                }
            }
 }

my_controller_configuration["workplace_choice_model_for_immigrant"] = copy.deepcopy(my_controller_configuration["workplace_choice_model_for_resident"])
my_controller_configuration["workplace_choice_model_for_immigrant"]["init"]["arguments"]["model_name"] = "'Non-home-based Work Choice Model for immigrants'"
my_controller_configuration["workplace_choice_model_for_immigrant"]["prepare_for_run"]["arguments"]["specification_table"] = "'workplace_choice_model_for_immigrant_specification'"
my_controller_configuration["workplace_choice_model_for_immigrant"]["prepare_for_run"]["arguments"]["coefficients_table"] = "'workplace_choice_model_for_immigrant_coefficients'"
my_controller_configuration["workplace_choice_model_for_immigrant"]["run"]["arguments"]["agents_filter"] = "'psrc.person.is_immigrant_worker_without_job'"
my_controller_configuration["household_location_choice_model"]["init"]["arguments"]["submodel_string"] = "'psrc.household.nonhome_based_workers_category'"

my_controller_configuration["home_based_workplace_choice_model"] = copy.deepcopy(my_controller_configuration["workplace_choice_model_for_resident"])
my_controller_configuration["home_based_workplace_choice_model"]["init"]["arguments"]["filter"] = "'psrc.job.is_untaken_home_based_job'"
my_controller_configuration["home_based_workplace_choice_model"]["init"]["arguments"]["model_name"] = "'Home-based Work Choice Model'"
my_controller_configuration["home_based_workplace_choice_model"]["init"]["arguments"]["short_name"] = "'HBWCM'"
my_controller_configuration["home_based_workplace_choice_model"]["prepare_for_run"]["arguments"]["specification_table"] = "'home_based_workplace_choice_model_specification'"
my_controller_configuration["home_based_workplace_choice_model"]["prepare_for_run"]["arguments"]["coefficients_table"] = "'home_based_workplace_choice_model_coefficients'"
my_controller_configuration["home_based_workplace_choice_model"]["run"]["arguments"]["agents_filter"] = "'psrc.person.is_home_based_worker_without_job'"
my_controller_configuration["home_based_workplace_choice_model"]["run"]["arguments"]["chunk_specification"] = "{'nchunks':1}"

for model in list(my_controller_configuration.keys()):
    if model not in list(run_configuration["models_configuration"].keys()):
        run_configuration["models_configuration"][model] = {}    
    run_configuration["models_configuration"][model]['controller'] = my_controller_configuration[model]

run_configuration['creating_baseyear_cache_configuration'].tables_to_cache += [
                                         "persons",
                                         "home_based_choice_model_coefficients",
                                         "home_based_choice_model_specification",
                                         "home_based_workplace_choice_model_coefficients",
                                         "home_based_workplace_choice_model_specification",
                                         "workplace_choice_model_for_resident_specification",
                                         "workplace_choice_model_for_resident_coefficients",
                                         "workplace_choice_model_for_immigrant_specification",
                                         "workplace_choice_model_for_immigrant_coefficients",                                         
                                         ]

run_configuration["datasets_to_preload"]['person'] = {'package_name':'psrc'}
run_configuration["models"] = [ 
                "prescheduled_events",
                "events_coordinator",
                "residential_land_share_model",
                'land_price_model',
                'development_project_transition_model',
                'residential_development_project_location_choice_model',
                'commercial_development_project_location_choice_model',
                'industrial_development_project_location_choice_model',
                "development_event_transition_model",
                "events_coordinator",
                "residential_land_share_model",
                "household_transition_model",
                "household_person_consistency_keeper",
                "home_based_choice_model",
                "home_based_workplace_choice_model",
                "job_change_model",
                "workplace_choice_model_for_immigrant",
                "employment_transition_model",
                "job_person_consistency_keeper",
                "household_relocation_model",
                "household_location_choice_model",
                "workplace_choice_model_for_resident",
                "employment_relocation_model", 
                {"employment_location_choice_model": {"group_members": "_all_"}},
                "distribute_unplaced_jobs_model"
                ]

