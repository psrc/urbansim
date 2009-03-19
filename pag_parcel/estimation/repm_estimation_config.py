# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from pag_parcel.configs.controller_config import config

run_configuration = config
run_configuration['models'] = [
    {'real_estate_price_model':['estimate']} ]
