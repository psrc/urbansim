# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import copy
from psrc.config.workplace_zone_choice_model_config import run_configuration
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class rwzcm_configuration:
    def __init__(self, dummy=None):
        self.model_name = "workplace_choice_model_for_resident"
    
    def get_configuration(self, specification_module="psrc.estimation.estimation_RWZCM_variables"):
        config = copy.deepcopy(run_configuration)
        config["models"] = [
            #"land_price_model",
            {"workplace_choice_model_for_resident": ["estimate"]}
         ]
        
        config["datasets_to_preload"] = {
            'gridcell':{},
            'person':{'package_name':'psrc'},
            'zone':{}                
        } 

        config = update_controller_by_specification_from_module(config, self.model_name, specification_module)

        return config