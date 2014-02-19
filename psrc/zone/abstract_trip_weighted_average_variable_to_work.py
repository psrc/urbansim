# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32, logical_and
from opus_core.ndimage import sum as ndimage_sum
from psrc.opus_package_info import package
from opus_core.logger import logger
from opus_core.misc import safe_array_divide
from opus_core.tests import opus_unittest

class Abstract_Trip_Weighted_Average_Variable_To_Work(Variable):
    """
    Do the trip-weighted averaging used by several of our variables.
    """
    _return_type = "float32"
    missing_value = 999 
    
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
        non_missing_idx = where(logical_and(time <> self.missing_value, trips <> self.missing_value))
        numerator = array(ndimage_sum(time[non_missing_idx] * trips[non_missing_idx],
                                       labels = to_zone_id[non_missing_idx], index=zone_ids))
        denominator = array(ndimage_sum(trips[non_missing_idx],
                                       labels = to_zone_id[non_missing_idx], index=zone_ids), dtype=float32)
        
        # if there is a divide by zero then substitute the values from the zone one below that one
        # if there are contiguous places of zero division the values should propagate upon iteration
        no_trips_to_here = where(denominator == 0)[0]
        while no_trips_to_here.size != 0:
            if no_trips_to_here.size == denominator.size:
                logger.log_warning("%s attribute of travel_data is all zeros; %s returns all zeros" % (self.trips_attribute_name, 
                                                                                                       self.name()
                                                                                                       ))
                break
            
            substitute_locations = no_trips_to_here - 1    # a mapping, what zone the new data will come from
            if substitute_locations[0] < 0: substitute_locations[0] = 1
            numerator[no_trips_to_here] = numerator[substitute_locations]
            denominator[no_trips_to_here] = denominator[substitute_locations] 
            no_trips_to_here = where(denominator == 0)[0]
            
        return safe_array_divide(numerator, denominator)