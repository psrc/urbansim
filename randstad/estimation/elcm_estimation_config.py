# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.configs.elcm_estimation_config import elcm_configuration as config
from urbansim.estimation.estimator import update_controller_by_specification_from_module
from randstad.run_config.randstad_baseline import run_configuration as randstad_config

class elcm_configuration(config):
    def get_configuration(self, specification_module="ELCM_specification"):
        run_configuration = config.get_configuration(self)
        run_configuration.merge(randstad_config)
        run_configuration['models'] = [
            'housing_price_model',
            "employment_relocation_model",
            "divide_jobs_model",                                       
            {self.model_name:['estimate']}]
        return self.get_updated_configuration_from_module(run_configuration, specification_module)
