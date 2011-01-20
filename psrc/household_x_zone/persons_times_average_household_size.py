# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class persons_times_average_household_size(Variable):
    """ average_housing_cost * income""" 
    z_household_size = "average_household_size"
    hh_size = "persons"
    
    def dependencies(self):
        return [attribute_label("zone", self.z_household_size), 
                attribute_label("household", self.hh_size)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_size, self.z_household_size)
                


#FIX THIS: I started to change this but it looks wrong -- why is the should_be a 2D array??
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_zone.persons_times_average_household_size"
    def test_my_inputs(self):
        average_household_size = array([3.1, 5.0, 1.2, 4.1])
        persons = array([1, 2, 5])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"zone":{ \
                "average_household_size":average_household_size}, \
            "household":{ \
                "persons":persons}}, \
            dataset = "household_x_zone")
        should_be = array([[3.1, 5.0, 1.2, 4.1], [6.2, 10.0, 2.4, 8.2], 
                            [15.5,  25,  6.0,  20.5]])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()