# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_value_vacant_land(Variable):
    """avg_val_per_unit_vacant_land * number of vacant_land_sqft"""

    _return_type = "float32"
    
    average_value_per_unit = "avg_val_per_unit_vacant_land"
    number_of_sqft = "vacant_land_sqft"

    def dependencies(self):
        return [my_attribute_label(self.average_value_per_unit), my_attribute_label(self.number_of_sqft)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.average_value_per_unit) * \
                self.get_dataset().get_attribute(self.number_of_sqft)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


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
                    "grid_id":array([1, 2, 3, 4]),             
                    "avg_val_per_unit_vacant_land":array([5, 17, 5, 0]), 
                    "vacant_land_sqft":array([2, 1, 0, 10])        
                }
            }
        )
        
        should_be = array([10, 17, 0, 0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
