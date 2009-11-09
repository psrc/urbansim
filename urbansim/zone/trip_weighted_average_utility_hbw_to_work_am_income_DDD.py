# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, where, float32
from scipy.ndimage import sum as ndimage_sum

class trip_weighted_average_utility_hbw_to_work_am_income_DDD(Variable):
    """ SUM(trips(I self) * logsum_DDD(I, self), for I=all_zones) / SUM(trips(J, self), J=all_zones)
    """
    
    def __init__(self, number):
        self.tnumber = number
        self.logsum_hbw_am_income = "logsum_hbw_am_income_" + str(int(self.tnumber))
        self.trips_hbw_am_income = "trips_hbw_am_income_" + str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.logsum_hbw_am_income), 
                attribute_label("travel_data", self.trips_hbw_am_income)]
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        logsum_hbw_am_income = travel_data.get_attribute(self.logsum_hbw_am_income)
        trips_hbw_am_income = travel_data.get_attribute(self.trips_hbw_am_income)
        to_zone_id = travel_data.get_attribute('to_zone_id')
        zone_ids = zone_set.get_attribute('zone_id')
        
        numerator = array(ndimage_sum(travel_data.get_attribute(self.trips_hbw_am_income) *
                                 travel_data.get_attribute(self.logsum_hbw_am_income),
                                    labels = to_zone_id, index=zone_ids))
        denominator = array(ndimage_sum(travel_data.get_attribute(self.trips_hbw_am_income),
                                    labels = to_zone_id, index=zone_ids), dtype=float32)
        
        # if there is a divide by zero then subsititute the values from the zone one below that one
        # if there are contigious places of zero division the values should propigate upon iteration
        no_trips_from_here = where(denominator == 0)[0]
        while no_trips_from_here.size != 0:
            substitute_locations = no_trips_from_here - 1    # a mapping, what zone the new data will come from
            if substitute_locations[0] < 0: substitute_locations[0] = 1
            numerator[no_trips_from_here] = numerator[substitute_locations]
            denominator[no_trips_from_here] = denominator[substitute_locations] 
            no_trips_from_here = where(denominator == 0)[0]
            
        return numerator / denominator
        
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    # check the case num_autos = 2
    variable_name = "urbansim.zone.trip_weighted_average_utility_hbw_to_work_am_income_2"
 
    def test_my_inputs(self):
        # the zone table includes two zones (1 and 2)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2])}, 
             "travel_data":{ 
                 "from_zone_id":array([1,1,2,2]), 
                 "to_zone_id":array([1,2,1,2]), 
                 "logsum_hbw_am_income_1":array([-4.8,-2.222,-3.1,-4]), 
                 "logsum_hbw_am_income_2":array([-3,-2,-1,-3.5]), 
                 "trips_hbw_am_income_1":array([1.1,2.1,3.1,4.1]), 
                 "trips_hbw_am_income_2":array([0,3.1,0,1.1])}}, 
            dataset = "zone")
        should_be = array([(3.1 * -2+1.1*-3.5)/(3.1+1.1),  
                           (3.1 * -2+1.1*-3.5)/(3.1+1.1)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()