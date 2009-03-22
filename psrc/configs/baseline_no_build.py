# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.configs.baseline import Baseline
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration

class BaselineNoBuild(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'baseline with no build travel model'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_no_build')
        self['travel_model_configuration'] = travel_model_configuration
        