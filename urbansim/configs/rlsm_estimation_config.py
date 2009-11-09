# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.configs.estimation_base_config import run_configuration as config

run_configuration = config.copy()
run_configuration["models"] = [
    {
    "residential_land_share_model": ["estimate"]
    }
]

run_configuration["datasets_to_preload"] = {
        'gridcell':{}
        }

