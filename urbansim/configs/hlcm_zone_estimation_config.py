# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from hlcm_estimation_config import estimation_configuration
from estimation_zone_config import run_configuration as config

run_configuration = config.copy()
run_configuration.merge(estimation_configuration)
#residential_price_model = {"real_estate_price_model": {"group_members": ["residential"]}}
#run_configuration["models"] = [residential_price_model] + \
#                               run_configuration["models"]
run_configuration["datasets_to_preload"] = {
        'gridcell': {},
        'job': {},
        'zone':{},
        'household':{},
        'building': {},
        'faz':{},
        }


#run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["sample_size_locations"] = 50