# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_ln_improvement_value_per_unit(Variable):
    """income * ln_residential_improvement_value_per_residential_unit"""
    _return_type="float32"
    gc_ln_residential_improvement_value_per_residential_unit = \
     "ln_residential_improvement_value_per_residential_unit"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_ln_residential_improvement_value_per_residential_unit),
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        self.gc_ln_residential_improvement_value_per_residential_unit)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import log
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.income_and_ln_improvement_value_per_unit"
    def test_full_tree(self):
        residential_improvement_value = array([100, 300, 800])
        residential_units = array([10, 3, 0])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{ 
                 "residential_improvement_value":residential_improvement_value,
                 "residential_units":residential_units},
             "household":{
                 "income":income}},
            dataset = "household_x_gridcell")
        should_be = array([[2302.585, 4605.170,0], [690775.5, 1381551.1,0 ], [115129.3, 230258.5,0],
                          [0,0,0], [24292.27, 48584.55, 0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3),
                         True, msg = "Error in " + self.variable_name)

    def test_my_inputs(self):
        ln_residential_improvement_value_per_residential_unit = array([log(10), log(100), 0])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{
                "ln_residential_improvement_value_per_residential_unit":ln_residential_improvement_value_per_residential_unit},
             "household":{ 
                 "income":income}}, 
            dataset = "household_x_gridcell")
        should_be = array([[2302.585, 4605.170,0], [690775.5, 1381551.1,0 ], [115129.3, 230258.5,0], 
                          [0,0,0], [24292.27, 48584.55, 0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), 
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()