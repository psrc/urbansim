# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_parcel.configs.controller_config import config

run_configuration = config
run_configuration["models"] = [
    {"real_estate_price_model": ["run"]},                                       
#    {"household_relocation_model": ["run"]},
    {"household_location_choice_model": ["estimate"]}
]
