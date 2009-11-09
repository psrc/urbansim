# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.configs.baseline import Baseline
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration

class Highway(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'double-capacity highway with baseline travel model'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_baseyear'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_highway')
        self['travel_model_configuration'] = travel_model_configuration
