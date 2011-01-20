# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_residential_value(Variable):
    """Sum of residential improvement value and residential land value"""

    residential_improvement_value = "residential_improvement_value"
    residential_land_value = "residential_land_value"

    def dependencies(self):
        return [my_attribute_label(self.residential_improvement_value), 
                my_attribute_label(self.residential_land_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.residential_improvement_value) + \
               self.get_dataset().get_attribute(self.residential_land_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        residential_improvement_value = array([200.5, 5, 200])
        residential_land_value = array([199, 205, 6])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "residential_improvement_value":residential_improvement_value, 
                    "residential_land_value":residential_land_value
                }
            }
        )
        
        should_be = array([399.5, 210, 206])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()