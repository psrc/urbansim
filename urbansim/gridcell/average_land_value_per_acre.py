    # Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import float32
from numpy import ma

class average_land_value_per_acre(Variable):
    """Average land value per acre, computed by dividing the gridcell's land value by its
    total number of acres"""

    land_value = "total_land_value"
    acres = "acres_of_land"

    def dependencies(self):
        return [my_attribute_label(self.land_value), 
                my_attribute_label(self.acres)]

    def compute(self, dataset_pool):
        acres = self.get_dataset().get_attribute("acres_of_land")
        return ma.filled(self.get_dataset().get_attribute("total_land_value")/ 
                                       ma.masked_where(acres == 0, acres.astype(float32)), 0.0)
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_land_value = array([0, 20050, 20050])
        acres_of_land = array([1995, 2005, 33])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{                     
                    "grid_id": array([1,2,3]),
                    "total_land_value":total_land_value, 
                    "acres_of_land":acres_of_land
                }
            }
        )
        
        should_be = array([0.0, 10.0, 607.5757576])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()