# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_vacant_land(Variable):
    """Boolean indicating whether the gridcell has vacant land"""

    _return_type = "bool8"
    vacant_sqft = "vacant_land_sqft"

    def dependencies(self):
        return [my_attribute_label(self.vacant_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.vacant_sqft) > 0

    def post_check(self, values, dataset_pool):
        self.do_check("x == True or x == False", values)


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
                    "vacant_land_sqft":array([1, 0, 5])
                }
            } 
        )
        
        should_be = array([True, False, True])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()