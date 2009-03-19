# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_not

class is_developed(Variable):
    """Returns a boolean indicating whether this gridcell is industrially, commercially, governmentally 
    or residentially developed"""

    has_0_industrial_sqft = "has_0_industrial_sqft"
    has_0_commercial_sqft = "has_0_commercial_sqft"
    has_0_governmental_sqft = "has_0_governmental_sqft"
    has_0_residential_units = "has_0_units"

    def dependencies(self):
        return [my_attribute_label(self.has_0_industrial_sqft),
                my_attribute_label(self.has_0_commercial_sqft), 
                my_attribute_label(self.has_0_governmental_sqft), 
                my_attribute_label(self.has_0_residential_units)]

    def compute(self, dataset_pool):
        return (logical_not(self.get_dataset().get_attribute(self.has_0_industrial_sqft)) + 
                logical_not(self.get_dataset().get_attribute(self.has_0_commercial_sqft)) +  
                logical_not(self.get_dataset().get_attribute(self.has_0_governmental_sqft)) +  
                logical_not(self.get_dataset().get_attribute(self.has_0_residential_units))) > 0

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        has_0_industrial_sqft =   array([1,1,0,0])
        has_0_commercial_sqft =   array([1,0,1,0])
        has_0_governmental_sqft = array([1,0,1,0])
        has_0_residential_units = array([1,0,0,0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "has_0_industrial_sqft":has_0_industrial_sqft, 
                    "has_0_commercial_sqft":has_0_commercial_sqft, 
                    "has_0_governmental_sqft":has_0_governmental_sqft, 
                    "has_0_units":has_0_residential_units
                }
            }
        )
        
        should_be = array([False,True,True,True])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()