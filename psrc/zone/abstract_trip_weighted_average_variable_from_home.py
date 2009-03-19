# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32
from scipy.ndimage import sum as ndimage_sum
from psrc.opus_package_info import package
from opus_core.logger import logger
from opus_core.misc import safe_array_divide
from opus_core.tests import opus_unittest

class Abstract_Trip_Weighted_Average_Variable_From_Home(Variable):
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
        from_zone_id = travel_data.get_attribute('from_zone_id')
        zone_ids = zone_set.get_attribute('zone_id')
        time = travel_data.get_attribute(self.time_attribute_name)
        trips = travel_data.get_attribute(self.trips_attribute_name)
        
        numerator = array(ndimage_sum(time * trips,
                                       labels = from_zone_id, index=zone_ids))
        denominator = array(ndimage_sum(trips,
                                         labels = from_zone_id, index=zone_ids), dtype=float32)
        
        # if there is a divide by zero then subsititute the values from the zone one below that one
        # if there are contigious places of zero division the values should propigate upon iteration
        no_trips_from_here = where(denominator == 0)[0]
        while no_trips_from_here.size != 0:
            if no_trips_from_here.size == denominator.size:
                logger.log_warning("%s attribute of travel_data is all zeros; %s returns all zeros" % (self.trips_attribute_name, 
                                                                                                       self.name()
                                                                                                       ))
                break
                 
            substitute_locations = no_trips_from_here - 1    # a mapping, what zone the new data will come from
            if substitute_locations[0] < 0: substitute_locations[0] = 1
            numerator[no_trips_from_here] = numerator[substitute_locations]
            denominator[no_trips_from_here] = denominator[substitute_locations] 
            no_trips_from_here = where(denominator == 0)[0]
            
        return safe_array_divide(numerator, denominator)

    ##TODO: this test class is not run or used by any other module
    class Abstract_Trip_Weighted_Average_Variable_From_Home_Tests(opus_unittest.OpusTestCase):
        def __init__(self, variable_name, time_attribute_name, trips_attribute_name):
            self.variable_name = variable_name
            self.time_attribute_name = time_attribute_name
            self.trips_attribute_name = trips_attribute_name
            opus_unittest.OpusTestCase.__init__(self)
        
        def test_my_inputs(self):
            values = VariableTestToolbox().compute_variable(self.variable_name,
                {"zone":{
                    "zone_id":array([1,2])},
                 "travel_data":{
                     "from_zone_id":array([1,1,2,2]),
                     "to_zone_id":array([1,2,1,2]),
                     self.time_attribute_name:array([1.1, 2.2, 3.3, 4.4]),
                     self.trips_attribute_name:array([1.0, 2.0, 3.0, 4.0])}},
                dataset = "zone", package=package())
            should_be = array([(1.1*1.0 +2.2*2.0)/(3.0), 
                               (3.3*3.0 + 4.4*4.0)/(7.0)])
            self.assert_(ma.allclose(values, should_be, rtol=1e-4), "Error in " + self.variable_name)
    
        def test_with_zero_denominator(self):
            values = VariableTestToolbox().compute_variable(self.variable_name,
                {"zone":{
                    "zone_id":array([1,2,3,4])},
                 "travel_data":{
                     "from_zone_id":array([1,2,2,3,4]),
                     "to_zone_id":array([1,2,1,2,2]),
                     self.time_attribute_name:array([1.1, 2.2, 3.3, 4.4, 5.5]),
                     self.trips_attribute_name:array([10.1, 20.0, 30.0, 0.0, 0.0])}},
                dataset = "zone", package=package())
            should_be = array([(1.1*10.1)/(10.1), 
                               (2.2*20.0 + 3.3*30)/(20.0+30.0), 
                               (2.2*20.0 + 3.3*30)/(20.0+30.0),# when denominator = 0, use prior good value
                               (2.2*20.0 + 3.3*30)/(20.0+30.0)])# when denominator = 0, use prior good value
            self.assert_(ma.allclose(values, should_be, rtol=1e-4), "Error in " + self.variable_name)
    