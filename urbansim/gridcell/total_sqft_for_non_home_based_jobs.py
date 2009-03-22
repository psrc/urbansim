# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_sqft_for_non_home_based_jobs(Variable):
    """Sum of sqft for jobs that aren't home-based (governmental, commmercial, and industrial)"""

    governmental_sqft = "governmental_sqft"
    commercial_sqft = "commercial_sqft"
    industrial_sqft = "industrial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.governmental_sqft), 
                my_attribute_label(self.commercial_sqft), 
                my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.governmental_sqft) + \
               self.get_dataset().get_attribute(self.commercial_sqft) + \
               self.get_dataset().get_attribute(self.industrial_sqft)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        governmental_sqft = array([1000, 3000, 0])
        commercial_sqft = array([500, 900, 250])
        industrial_sqft = array([200, 0, 1000])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "governmental_sqft":governmental_sqft, 
                    "commercial_sqft":commercial_sqft, 
                    "industrial_sqft":industrial_sqft 
                }
            }
        )
        
        should_be = array([1700, 3900, 1250])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()