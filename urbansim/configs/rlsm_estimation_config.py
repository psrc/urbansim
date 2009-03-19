# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

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

