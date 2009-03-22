# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class trip_weighted_travel_time_for_transit_walk(Variable):
    """ The trip_weighted_travel_time_for_transit_walk value."""

    zone_wtt_tw = "trip_weighted_travel_time_for_transit_walk"

    def dependencies(self):
        return [attribute_label("zone", self.zone_wtt_tw), 
                my_attribute_label("zone_id")]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.zone_wtt_tw)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        wtt_tw = array([0.0, 0.250, 1])
        locations_in_zoneid = array([1, 1, 3, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "trip_weighted_travel_time_for_transit_walk":wtt_tw
                    }, 
                "gridcell":{ 
                    "grid_id":array([1,2,3,4,5]),
                    "zone_id":locations_in_zoneid
                }
            }
        )
        
        should_be = array([0.0, 0.0, 1, .250, .250])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()