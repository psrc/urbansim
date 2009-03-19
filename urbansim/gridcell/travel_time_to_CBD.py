# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class travel_time_to_CBD(Variable):
    """AM peak hour travel time by single-occupancy vehicle from the cell's TAZ to the CBD's TAZ (or a representative TAZ for the CBD).
    [cell.travel_time_to_CBD - based on the TAZ-to-TAZ AM peak hour travel time."""

    zone_travel_time_to_CBD = "travel_time_to_cbd"

    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("zone", self.zone_travel_time_to_CBD)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.zone_travel_time_to_CBD)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        travel_time_to_cbd = array([0.0, 30.0, 60.0])
        locations_in_zoneid = array([1, 1, 3, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "travel_time_to_cbd":travel_time_to_cbd
                    }, 
                "gridcell":{ 
                    "grid_id":array([1,2,3,4,5]),
                    "zone_id":locations_in_zoneid
                }
            }
        )
        
        should_be = array([0.0, 0.0, 60.0, 30.0, 30.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()