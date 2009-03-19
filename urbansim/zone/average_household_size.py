# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import safe_array_divide

class average_household_size(Variable):
    """Computed by dividing population in the given zone by
        the total number of housholds in the zone"""

    population = "population"
    number_of_households = "number_of_households"

    def dependencies(self):
        return [my_attribute_label(self.number_of_households),
                my_attribute_label(self.population)]

    def compute(self, dataset_pool):
        nh = self.get_dataset().get_attribute(self.number_of_households)
        return safe_array_divide(self.get_dataset().get_attribute(self.population), nh)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.average_household_size"

    def test_my_inputs(self):
        population = array([1000, 10000, 100000]) #specify population for each of three locations
        number_of_households = array([300, 20, 500]) #specify the total number of households for each of three locations

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "population":population, 
                "number_of_households":number_of_households}}, 
            dataset = "zone")

        should_be = array([3.33333, 500.0, 200.0]) 
        self.assertEqual(ma.allclose(values, should_be), True, msg = "Error in " + self.variable_name)

    def test_for_err(self):
        population = array([1000, 10000, 100000])
        number_of_households = array([1, 0, 500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "population":population, 
                "number_of_households":number_of_households}}, 
            dataset = "zone")
        should_be = array([1000.0, 0, 200.0])
        self.assertEqual(ma.allclose(values, should_be, rtol=0), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()