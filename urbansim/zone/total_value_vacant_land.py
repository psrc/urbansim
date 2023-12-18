# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class total_value_vacant_land(Variable):
    """Total value of vacant land."""

    def dependencies(self):
        return [my_attribute_label("avg_val_per_unit_vacant_land"), 
                my_attribute_label("vacant_land_sqft")]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("avg_val_per_unit_vacant_land") * \
               self.get_dataset().get_attribute("vacant_land_sqft")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.total_value_vacant_land"

    def test_my_inputs(self):
        val = array([10, 20, 30])
        space = array([1995, 2005, 2006])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "avg_val_per_unit_vacant_land":val, 
                "vacant_land_sqft":space} }, 
            dataset = "zone")
        should_be = array([19950, 40100, 60180])

        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()