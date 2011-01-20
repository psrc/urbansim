# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configs.estimation_base_config import EstimationBaseConfig

class HLCMEstimationConfig(EstimationBaseConfig):
    def __init__(self, base_configuration=AbstractUrbansimConfiguration):
        EstimationBaseConfig.__init__(self, base_configuration)
        self.update_config()
        
    def update_config(self):
        self.merge(get_changes_for_hlcm_estimation(self))
        
def get_changes_for_hlcm_estimation(config=None):
    estimation_configuration = {}
    estimation_configuration["models"] = [                                
                  {"household_relocation_model": ["run"]},
                  {"household_location_choice_model": ["estimate"]}
              ]

    estimation_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'household':{}
        }
    return estimation_configuration

run_configuration = config.copy()

estimation_configuration = get_changes_for_hlcm_estimation()
run_configuration.merge(estimation_configuration)
