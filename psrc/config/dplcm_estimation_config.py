# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.dplcm_estimation_config import dplcm_configuration as config
from urbansim.estimation.estimator import update_controller_by_specification_from_module

class dplcm_configuration(config):
    def get_configuration(self, specification_module="psrc.estimation.estimation_DM_variables"):
        run_configuration = config.get_configuration(self)
        return self.get_updated_configuration_from_module(run_configuration, specification_module)