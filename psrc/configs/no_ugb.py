# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc.configs.baseline import Baseline

class NoUgb(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'no ugb with full travel model'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_scenario_A_no_ugb'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc')
        self['travel_model_configuration'] = travel_model_configuration
        