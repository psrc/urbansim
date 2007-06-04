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

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32
from scipy.ndimage import sum as ndimage_sum
from psrc.opus_package_info import package

from opus_core.tests import opus_unittest

class Abstract_Trip_Weighted_Average_Variable_To_Work(Variable):
    """
    Do the trip-weighted averaging used by several of our variables.
    """
    _return_type = "float32"
    def __init__(self, time_attribute_name, trips_attribute_name):
        self.time_attribute_name = time_attribute_name
        self.trips_attribute_name = trips_attribute_name
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("travel_data", self.time_attribute_name), 
                attribute_label("travel_data", self.trips_attribute_name)]
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        to_zone_id = travel_data.get_attribute('to_zone_id')
        zone_ids = zone_set.get_attribute('zone_id')
        time = travel_data.get_attribute(self.time_attribute_name)
        trips = travel_data.get_attribute(self.trips_attribute_name)
        
        numerator = array(ndimage_sum(time * trips,
                                       labels = to_zone_id, index=zone_ids))
        denominator = array(ndimage_sum(trips,
                                         labels = to_zone_id, index=zone_ids), dtype=float32)
        
        # if there is a divide by zero then subsititute the values from the zone one below that one
        # if there are contigious places of zero division the values should propigate upon iteration
        no_trips_to_here = where(denominator == 0)[0]
        while no_trips_to_here.size != 0:
            substitute_locations = no_trips_to_here - 1    # a mapping, what zone the new data will come from
            if substitute_locations[0] < 0: substitute_locations[0] = 1
            numerator[no_trips_to_here] = numerator[substitute_locations]
            denominator[no_trips_to_here] = denominator[substitute_locations] 
            no_trips_to_here = where(denominator == 0)[0]
            
        return numerator / denominator
