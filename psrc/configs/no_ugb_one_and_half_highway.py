# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from psrc.configs.baseline import Baseline
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration

class NoUgbOneAndHalfHighway(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'no ugb + 1.5 x baseline highway capacity'
        self['scenario_database_configuration'].database_name = 'PSRC_2000_scenario_A_no_ugb'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_highway_x_1.5')
        self['travel_model_configuration'] = travel_model_configuration
