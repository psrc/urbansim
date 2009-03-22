# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_improvement_value(Variable):
    """Sum of all improvement values for this gridcell."""
    
    nonresidential_improvement_value = "nonresidential_improvement_value"
    residential_improvement_value = "residential_improvement_value"

    def dependencies(self):
        return [my_attribute_label(self.nonresidential_improvement_value), 
                my_attribute_label(self.residential_improvement_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.nonresidential_improvement_value) + \
               self.get_dataset().get_attribute(self.residential_improvement_value)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        nonresidential_improvement_value = array([100, 200, 300])
        residential_improvement_value = array([1000, 400, 0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3]),
                    "nonresidential_improvement_value":nonresidential_improvement_value, 
                    "residential_improvement_value":residential_improvement_value
                }
            }
        )
        
        should_be = array([1100, 600, 300])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()