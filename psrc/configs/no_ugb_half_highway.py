# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.configs.baseline import Baseline
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration

class NoUgbHalfHighway(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'no ugb + double-capacity highway'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_scenario_A_no_ugb'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_highway_x_half')
        self['travel_model_configuration'] = travel_model_configuration
