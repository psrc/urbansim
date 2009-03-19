# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim_parcel.configs.controller_config import config

run_configuration = config
run_configuration["models"] = [
#    {"land_price_model": ["run"]},                                      
    {"business_relocation_model": ["run"]},
    {"business_location_choice_model": ["estimate"]}
]
