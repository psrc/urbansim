# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config
from opus_core.resources import merge_resources_if_not_None
run_configuration = config.copy()
run_configuration['models_configuration']['work_place_location_choice_model']= {}
run_configuration['models_configuration']['work_place_location_choice_model']["estimation"]="opus_core.bhhh_mnl_estimation"
#run_configuration['models_configuration']['work_place_location_choice_model']["sampler"]=None #"opus_core.samplers.weighted_sampler"
run_configuration['models_configuration']['work_place_location_choice_model']["sample_size_locations"]=None #None 
run_configuration['models_configuration']['work_place_location_choice_model']["weights_for_estimation_string"]="urbansim.zone.number_of_non_home_based_jobs"

run_configuration['models_configuration']['work_place_location_choice_model']["export_estimation_data"]=True
run_configuration['models_configuration']['work_place_location_choice_model']["estimation_data_file_name"]="/tmp/WPLCM_estimate_data.csv"
    
my_controller_configuration = {
 'work_place_location_choice_model': {
    "import": {"urbansim.models.agent_location_choice_model":
                                        "AgentLocationChoiceModel"},
    "init": { 
        "name": "AgentLocationChoiceModel",
        "arguments": {
                      "location_set":"zone",
                      "model_name":"'Work Place Location Choice Model'",
                      "short_name":"'WPLCM'",
                      "submodel_string":"None",
                      "sampler":"None",
                      "location_id_string":"'psrc.person.work_place_zone_id'",
                      "run_config":"models_configuration['work_place_location_choice_model']",
                      "estimate_config":"models_configuration['work_place_location_choice_model']"
             }},
    "prepare_for_estimate": {
        "name": "prepare_for_estimate",
        "arguments": {
                      "agent_set":"person",
                      "join_datasets": "False",
                      "agents_for_estimation_storage": "base_cache_storage",
                      "agents_for_estimation_table": "'persons'",                      
                      "filter":"'psrc.person.is_worker1_in_single_nonhome_based_worker_household'",
                      "data_objects": "datasets"
                        },
        "output": "(specification, index)"
        },
                                           
    "estimate": {
        "arguments": {          
                      "specification": "specification",
                      "agent_set": "person",
                     "agents_index": "index",
                      "data_objects": "datasets",
                      "debuglevel": run_configuration['debuglevel']},
        "output": "(coefficients, dummy)"
        },  
   }}

for model in my_controller_configuration.keys():
    if model not in run_configuration["models_configuration"].keys():
        run_configuration["models_configuration"][model] = {}    
    run_configuration["models_configuration"][model]['controller'] = my_controller_configuration[model]

run_configuration["models"] = [
    {"work_place_location_choice_model": ["estimate"]}
]

run_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'parcel':{'package_name':'psrc'},                                            
        'person':{'package_name':'psrc'},
        'zone':{}
        }
