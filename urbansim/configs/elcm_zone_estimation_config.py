# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .elcm_estimation_config import elcm_configuration as elcm_gridcell_config
from .estimation_zone_config import run_configuration as config

class elcm_configuration(elcm_gridcell_config):
    def get_configuration(self):
        run_configuration = config.copy()
        elcm_local_configuration = self.get_local_configuration()
        run_configuration.merge(elcm_local_configuration)
        return run_configuration
    
    def get_local_configuration(self):
        run_configuration = elcm_gridcell_config.get_local_configuration(self)
        run_configuration.merge(self.get_local_elcm_configuration())
        #residential_price_model = {"real_estate_price_model": {"group_members": ["residential"]}}
        #if self.type == "home_based":
        #    run_configuration["models"] = [residential_price_model] + \
        #        run_configuration["models"]
        #else:
        #    run_configuration["models"] = [{"real_estate_price_model": {"group_members": [self.type]}}] + \
        #                                  run_configuration["models"] 
        return run_configuration
    
    def get_local_elcm_configuration(self):
        run_configuration = {}
        run_configuration["datasets_to_preload"] = {
            'zone':{},
            'job':{},
            'gridcell': {},
            'household':{},
            'job_building_type':{},
            'building':{},
            'faz': {},
            }
        return run_configuration