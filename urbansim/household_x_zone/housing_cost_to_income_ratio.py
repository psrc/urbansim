# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class housing_cost_to_income_ratio(Variable):
    """ average_housing_cost / income""" 
    z_housing_cost = "average_housing_cost"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("zone", self.z_housing_cost), 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().divide(self.z_housing_cost, self.hh_income)
                

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.housing_cost_to_income_ratio"
    def test_my_inputs(self):
        housing_cost = array([333.0, 500.55, 1000.26, 459])
        income = array([1, 20, 500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "average_housing_cost":housing_cost}, 
            "household":{ 
                "income":income}}, 
            dataset = "household_x_zone")
        should_be = array([[333.0, 500.55, 1000.26, 459.0], [16.65, 25.0275, 50.013, 22.95], 
                            [.666,  1.0011,  2.00052, .918]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), 
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()