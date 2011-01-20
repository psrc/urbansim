# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import array

class utility_for_SOV(Variable):
    """The utility for SOV. """
    zone_id = "zone_id"

    def dependencies(self):
        return [my_attribute_label(self.zone_id), 
                attribute_label("zone", "zone_id"),
                attribute_label("zone", "utility_for_sov")]

    def compute(self, dataset_pool):
        zone_ids = self.get_dataset().get_attribute(self.zone_id)
        return dataset_pool.get_dataset('zone').get_attribute_by_id("utility_for_sov",zone_ids)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        utility_for_SOV = array([0.0, 0.250, 1])
        locations_in_zoneid = array([1, 1, 3, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "utility_for_sov":utility_for_SOV}, 
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