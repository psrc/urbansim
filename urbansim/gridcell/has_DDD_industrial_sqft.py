# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_DDD_industrial_sqft(Variable):
    """Boolean indicating whether or not the gridcell has DDD industrial_sqft"""

    industrial_sqft = "industrial_sqft"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.industrial_sqft) == self.tnumber

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
                    "grid_id":array([1, 2, 3]),
                    "industrial_sqft":array([1, 2, 5])
                }
            }
        )
    
        should_be = array([False, True, False])
        instance_name = "urbansim.gridcell.has_2_industrial_sqft"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()