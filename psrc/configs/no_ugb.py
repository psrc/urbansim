#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

class NoUgb(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'no ugb with full travel model'
        self['input_configuration'].database_name = 'PSRC_2000_scenario_A_no_ugb'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc')
        self['travel_model_configuration'] = travel_model_configuration
        