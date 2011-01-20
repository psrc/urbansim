# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.estimation_base_config import run_configuration as config
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class dplcm_configuration:
    def __init__(self, type):
        self.type=type
        self.model_name = "%s_development_project_location_choice_model" % type
        
    def get_configuration(self):
        run_configuration = config.copy()
        dplcm_local_configuration = self.get_dplcm_configuration()
        run_configuration.merge(dplcm_local_configuration)
        run_configuration["models_configuration"]["%s_development_project_location_choice_model" % self.type]["controller"]["init"]["arguments"]["filter"] = \
            "'urbansim.gridcell.developable_%s_capacity_lag%s' %s (model_configuration['development_project_types']['%s']['units'], urbansim_constant['recent_years']+1)" % ("%s", "%s", "%", self.type)        
        return run_configuration

    def get_dplcm_configuration(self):
        run_configuration = {}
        run_configuration["models"] = [
            "land_price_model",
            {"%s_development_project_location_choice_model" % self.type: ["estimate"]}
         ]
        
        run_configuration["datasets_to_preload"] = {
                'gridcell':{}
                } 
        return run_configuration
    
    def get_updated_configuration_from_module(self, run_configuration, specification_module=None):
        run_configuration = update_controller_by_specification_from_module(
                            run_configuration, self.model_name, specification_module)
        run_configuration["models_configuration"][self.model_name]["controller"]["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec['%s']" % self.type
        return run_configuration  