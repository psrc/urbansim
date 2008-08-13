#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from psrc.configs.baseline import Baseline
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration

class NoUgbOneAndHalfHighway(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'no ugb + 1.5 x baseline highway capacity'
        self['input_configuration'].database_name = 'PSRC_2000_scenario_A_no_ugb'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_highway_x_1.5')
        self['travel_model_configuration'] = travel_model_configuration
