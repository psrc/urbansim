# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class devtype_DDD(Variable):
    """Returns a boolean indicating whether this gridcell is of the specified devtype"""

    development_type_id = "development_type_id"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.development_type_id)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.development_type_id) == self.tnumber


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
                    "development_type_id":array([1, 2, 5])
                }
            }
        )
        
        should_be = array([True, False, False])
        instance_name = "urbansim.gridcell.devtype_1"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()