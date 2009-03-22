# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class commercial_and_industrial_sqft(Variable):
    """Sum of commercial, industrial sqft for this gridcell."""
    
    commercial_sqft = "commercial_sqft"
    industrial_sqft = "industrial_sqft"
    #governmental_sqft = "governmental_sqft"

    def dependencies(self):
        return [my_attribute_label(self.commercial_sqft), 
                my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.commercial_sqft) + \
               self.get_dataset().get_attribute(self.industrial_sqft)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs1(self):
        commercial_sqft = array([100, 200, 300])
        governmental_sqft = array([1000, 400, 0])
        industrial_sqft = array([0, 100, 500])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "commercial_sqft":commercial_sqft, 
                    "governmental_sqft":governmental_sqft, 
                    "industrial_sqft":industrial_sqft
                }
            }
        )
        
        should_be = array([100, 300, 800])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()