# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_land_value_from_buildings(Variable):
    """Sum of land values of locations computed from buildings."""

    vl_land_value = "total_value_vacant_land"
    nvl_land_value = "total_non_vacant_land_value_from_buildings"
    def dependencies(self):
        return [my_attribute_label(self.vl_land_value), my_attribute_label(self.nvl_land_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.nvl_land_value) + \
               self.get_dataset().get_attribute(self.vl_land_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        vl_land_value = array([40.5, 0.3, 100])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "building": {
                    "building_id":       array([1, 2, 3, 4, 5, 6]),
                    "land_value":        array([20, 40, 0, 100, 50, 99]),
                    "improvement_value": array([43, 1, 3, 0, 10, 3]),
                    "grid_id":           array([2, 3, 1, 1, 2, 2])
                    },
                "gridcell":{ 
                    "grid_id": array([1,2,3]),
                    "total_value_vacant_land": vl_land_value,
                }
            }
        )
        
        should_be = array([3+100+40.5, 20+43+50+10+99+3+0.3, 41+100])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()