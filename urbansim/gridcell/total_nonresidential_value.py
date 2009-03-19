# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_nonresidential_value(Variable):
    """Sum of the nonresidential improvement value and the nonresidential land value"""

    nonresidential_improvement_value = "nonresidential_improvement_value"
    nonresidential_land_value = "nonresidential_land_value"

    def dependencies(self):
        return [my_attribute_label(self.nonresidential_improvement_value), 
                my_attribute_label(self.nonresidential_land_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.nonresidential_improvement_value) + \
               self.get_dataset().get_attribute(self.nonresidential_land_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        nonresidential_improvement_value = array([200.5, 5, 200])
        nonresidential_land_value = array([199, 205, 6])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "nonresidential_improvement_value":nonresidential_improvement_value, 
                    "nonresidential_land_value":nonresidential_land_value
                }
            } 
        )
        
        should_be = array([399.5, 210, 206])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()