# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configuration import Configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration

class EstimationBaseConfig(Configuration):
    def __init__(self, base_configuration=AbstractUrbansimConfiguration):
        config = base_configuration()
        config.merge(get_changes_for_estimation(config))
        self.merge(config)
                
def get_changes_for_estimation(config):
    estimation_configuration = {}
    if "base_year" in config:
        estimation_configuration["years"] = range(config["base_year"], config["base_year"])
    estimation_configuration["sample_size_locations"] = 30
    estimation_configuration["seed"] = 1,#(1,1)
    return estimation_configuration

run_configuration = AbstractUrbansimConfiguration()

estimation_configuration = get_changes_for_estimation(run_configuration)
run_configuration.merge(estimation_configuration)