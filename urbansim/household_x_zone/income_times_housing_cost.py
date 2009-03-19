# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class income_times_housing_cost(Variable):
    """ average_housing_cost * income""" 
    z_housing_cost = "average_housing_cost"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("zone", self.z_housing_cost), 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, self.z_housing_cost)
                

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.income_times_housing_cost"
    def test_my_inputs(self):
        housing_cost = array([333.0, 500.55, 1000.26, 459])
        income = array([1, 20, 500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "average_housing_cost":housing_cost}, 
            "household":{ 
                "income":income}}, 
            dataset = "household_x_zone")
        should_be = array([[333.0, 500.55, 1000.26, 459.0], [6660.0, 10011., 20005.2, 9180], 
                            [166500.,  250275.,  500130.,  229500.]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()