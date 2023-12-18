# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class total_non_vacant_land_value_from_buildings(Variable):
    """Sum of land values of locations computed from buildings (excluded vacant_land)."""

    def dependencies(self):
        return [attribute_label("building", "land_value"),
                attribute_label("building", "improvement_value"),
                attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        return self.get_dataset().sum_dataset_over_ids(buildings, "land_value") + \
               self.get_dataset().sum_dataset_over_ids(buildings, "improvement_value")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.total_non_vacant_land_value_from_buildings"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"building": {
                 "land_value":         array([20, 40, 0, 100, 50, 99]),
                  "improvement_value": array([43, 1, 3, 0, 10, 3]),
                   "grid_id":          array([2,  3, 1, 1,  2, 2])
                          },
             "gridcell":{ 
                "grid_id": array([1,2,3]),
        } }, 
            dataset = "gridcell")
        should_be = array([3+100, 20+43+50+10+99+3, 41])

        self.assertEqual(ma.allclose(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()