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

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_employment_within_DDD_minutes_travel_time_hbw_am_transit_walk(Variable):
    """Natural log of employment_within_DDD_minutes_travel_time_hbw_am_transit_walk"""
    
    _return_type="float32"    

    def __init__(self, number):
        self.variable_name = 'employment_within_%s_minutes_travel_time_hbw_am_transit_walk' % number
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label(self.variable_name)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.variable_name))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft