# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class household_size_times_population_per_acre(Variable):
    """ population_per_acre * household_size""" 
    z_popden = "population_per_acre"
    hh_size = "persons"
    
    def dependencies(self):
        return [attribute_label("zone", self.z_popden), 
                attribute_label("household", self.hh_size)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_size, self.z_popden)
                

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.household_size_times_population_per_acre"
    def test_my_inputs(self):
        population_per_acre = array([100, 200, 400, 200])
        persons = array([1, 4, 2])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "population_per_acre":population_per_acre}, 
            "household":{ 
                "persons":persons}}, 
            dataset = "household_x_zone")
        should_be = array([[100, 200, 400, 200], [400, 800, 1600, 800], 
                            [200, 400, 800, 400]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3),
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()