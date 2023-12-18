# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class is_fully_in_water(Variable):
    """Returns a boolean indicating if the gridcell is 100% in water"""

    percent_water = "percent_water"

    def dependencies(self):
        return [my_attribute_label(self.percent_water)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.percent_water) >= 100

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "percent_water":array([100, 50, 0])
                }
            }
        )
        
        should_be = array([True, False, False])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()