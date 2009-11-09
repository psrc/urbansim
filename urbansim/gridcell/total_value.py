# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_value(Variable):
    """The total_residential_value + total_nonresidential_value."""
    
    total_residential_value = "total_residential_value"
    total_nonresidential_value = "total_nonresidential_value"
    
    def dependencies(self):
        return [my_attribute_label(self.total_residential_value), 
                my_attribute_label(self.total_nonresidential_value)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.total_residential_value) + \
               self.get_dataset().get_attribute(self.total_nonresidential_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        total_nonresidential_value = array([200, 500, 1000])
        total_residential_value = array([100, 400, 900])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "total_nonresidential_value":total_nonresidential_value, 
                    "total_residential_value":total_residential_value
                }
            }
        )
        
        should_be = array([300, 900, 1900])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)
        

if __name__=='__main__':
    opus_unittest.main()