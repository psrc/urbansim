# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config
from opus_core.resources import merge_resources_if_not_None
run_configuration = config.copy()
run_configuration['models_configuration']['worker1_work_place_location_choice_model']= {}
run_configuration['models_configuration']['worker1_work_place_location_choice_model']["estimation"]="opus_core.bhhh_mnl_estimation"
#run_configuration['models_configuration']['worker1_work_place_location_choice_model']["sampler"]=None #"opus_core.samplers.weighted_sampler"
run_configuration['models_configuration']['worker1_work_place_location_choice_model']["sample_size_locations"]=None
#run_configuration['models_configuration']['worker1_work_place_location_choice_model']["weights_for_estimation_string"]="urbansim.zone.number_of_non_home_based_jobs"

run_configuration['models_configuration']['worker1_work_place_location_choice_model']["export_estimation_data"]=True
run_configuration['models_configuration']['worker1_work_place_location_choice_model']["estimation_data_file_name"]="/tmp/W1WPLCM_estimate_data.csv"
    
my_controller_configuration = {
 'worker1_work_place_location_choice_model': {
    "import": {"urbansim.models.agent_location_choice_model":
                                        "AgentLocationChoiceModel"},
    "init": { 
        "name": "AgentLocationChoiceModel",
        "arguments": {
                      "location_set":"zone",
                      "model_name":"'Worker1 Work Place Location Choice Model'",
                      "short_name":"'W1WPLCM'",
                      "submodel_string":"None",
                      "sampler":'None', #"opus_core.samplers.weighted_sampler",#
                      "location_id_string":"'psrc.household.worker1_work_place_zone_id'",
                      "run_config":"models_configuration['worker1_work_place_location_choice_model']",
                      "estimate_config":"models_configuration['worker1_work_place_location_choice_model']"
             }},
    "prepare_for_estimate": {
        "name": "prepare_for_estimate",
        "arguments": {
                      "agent_set":"household",
                      "join_datasets": "False",
                      "agents_for_estimation_storage": "base_cache_storage",
                      "agents_for_estimation_table": "'households_for_estimation'",                      
                      "filter":"'psrc.household.has_1_nonhome_based_workers_and_valid_worker1_work_place_zone_id'",
                      "data_objects": "datasets"
                        },
        "output": "(specification, index)"
        },
                                           
    "estimate": {
        "arguments": {          
                      "specification": "specification",
                      "agent_set": "household",
                     "agents_index": "index",
                      "data_objects": "datasets",
                      "debuglevel": run_configuration['debuglevel']},
        "output": "(coefficients, dummy)"
        },  
   }}

for model in list(my_controller_configuration.keys()):
    if model not in list(run_configuration["models_configuration"].keys()):
        run_configuration["models_configuration"][model] = {}    
    run_configuration["models_configuration"][model]['controller'] = my_controller_configuration[model]

run_configuration["models"] = [
    {"worker1_work_place_location_choice_model": ["estimate"]}
]

run_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'parcel':{'package_name':'psrc'},                                            
        'person':{'package_name':'psrc'},
        'zone':{},
        'household':{},
        }
