# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_land_value(Variable):
    """Sum of land values of location."""

    residential_land_value = "residential_land_value"
    nonresidential_land_value = "nonresidential_land_value"

    def dependencies(self):
        return [my_attribute_label(self.residential_land_value), 
                my_attribute_label(self.nonresidential_land_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.residential_land_value) + \
               self.get_dataset().get_attribute(self.nonresidential_land_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.total_land_value"

    def test_my_inputs(self):
        residential_land_value = array([100, 200, 300])
        nonresidential_land_value = array([1995, 2005, 2006])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "residential_land_value":residential_land_value, 
                "nonresidential_land_value":nonresidential_land_value} }, 
            dataset = "zone")
        should_be = array([2095, 2205, 2306])

        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()