# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from randstad.run_config.randstad_baseline import run_configuration as config

run_configuration = config.copy()
run_configuration['models'] = [
    'housing_price_model',
    {'landuse_development_location_choice_model':['estimate']}]
