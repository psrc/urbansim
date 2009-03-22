# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_developed_with_buildings(Variable):
    """Returns a boolean indicating whether this gridcell is developed with buildings."""

    _return_type = "bool8"

    def dependencies(self):
        return [my_attribute_label("number_of_buildings")]
                
    def compute(self, dataset_pool):
        nob = self.get_dataset().get_attribute("number_of_buildings")
        return nob > 0

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        nob =     array([1,1,0,0])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "number_of_buildings": nob, 
                }
            }
        )
        
        should_be = array([True, True, False, False])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()