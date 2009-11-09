# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from randstad.run_config.randstad_baseline import run_configuration as config

run_configuration = config.copy()
run_configuration['models'] = [
    {'housing_price_model':['estimate']} ]
