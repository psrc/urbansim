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

class HalfHighway(Baseline):
    def __init__(self):
        Baseline.__init__(self)
        self['description'] = 'double-capacity highway with baseline travel model'
        self['input_configuration'].database_name = 'PSRC_2000_baseyear'

        travel_model_configuration = create_travel_model_configuration('baseline_travel_model_psrc_highway_x_half')
        self['travel_model_configuration'] = travel_model_configuration
