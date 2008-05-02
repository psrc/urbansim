#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from urbansim.configs.estimation_base_config import run_configuration as config
from opus_core.resources import merge_resources_if_not_None
run_configuration = config.copy()
run_configuration['models_configuration'].merge({
                          "estimation":"opus_core.bhhh_mnl_estimation", 
                          })            
    
my_controller_configuration = {
 'auto_ownership_choice_model': {
    "import": {"opus_core.choice_model":"ChoiceModel",
               "washtenaw.aocm.aocm_specification":"specification as spec_dict",
               "opus_core.model":"get_specification_for_estimation",
               },
    "init": { 
        "name": "ChoiceModel",
        "arguments": {
                      "choice_set":[0, 1, 2, 3],
                      "choice_attribute_name":"'cars'",
#                      "run_config":"models_configuration",
#                      "estimate_config":"models_configuration"
             }},
#    "prepare_for_estimate": {
#        "name": "prepare_for_estimate",
#        "arguments": {
#                      "agent_set":'household'
#                        },
#        "output": "(specification, index)"
#        },
    "estimate": {
        "arguments": {          
                      "specification": "get_specification_for_estimation(spec_dict)",
                      "agent_set": "household",
#                     "agents_index": "index",
                      "procedure":"'opus_core.bhhh_mnl_estimation'",
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
    {"auto_ownership_choice_model": ["estimate"]}
]

run_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'household':{},
        'zone':{}
        }
