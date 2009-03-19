# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from dplcm_estimation_config import dplcm_configuration as dplcm_gridcell_config
from estimation_zone_config import run_configuration as config

class dplcm_configuration(dplcm_gridcell_config):
    def get_configuration(self):
        run_configuration = config.copy()
        dplcm_local_configuration = self.get_dplcm_configuration()
        run_configuration.merge(dplcm_local_configuration)
        return run_configuration
    
    def get_dplcm_configuration(self):
        run_configuration = dplcm_gridcell_config.get_dplcm_configuration(self)
        run_configuration.merge(self.get_local_dplcm_configuration())
        return run_configuration
        
    def get_local_dplcm_configuration(self):
        run_configuration = {}
        run_configuration["models"] = [
            {"%s_development_project_location_choice_model" % self.type: ["estimate"]}
         ]
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'job':{},
            'gridcell': {}
            }
        return run_configuration