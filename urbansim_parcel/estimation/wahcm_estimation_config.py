# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_parcel.configs.controller_config import config

run_configuration = config
run_configuration["models"] = [
#    {"land_price_model": ["run"]},                                      
    {"work_at_home_choice_model": ["estimate"]}
]
