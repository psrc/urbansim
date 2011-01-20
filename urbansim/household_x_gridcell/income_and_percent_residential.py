# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_percent_residential(Variable):
    """ income * percent_residential"""
    _return_type="float32"
    gc_percent_residential = "percent_residential"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_percent_residential),
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        self.gc_percent_residential)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import log
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.income_and_percent_residential"
    def test_full_tree(self):
        fraction_residential_land = array([1, 0, 0.35])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{ 
                 "fraction_residential_land":fraction_residential_land}, 
             "household":{
                 "income":income}},
            dataset = "household_x_gridcell")
        should_be = array([[100000, 0, 35000], [30000000, 0, 10500000], [5000000, 0, 1750000],
                          [0,0,0], [1055000, 0, 369250]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3),
                         True, msg = "Error in " + self.variable_name)

    def test_my_inputs(self):
        percent_residential = array([100, 0, 35])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{
                "percent_residential":percent_residential},
             "household":{
                 "income":income}},
            dataset = "household_x_gridcell")
        should_be = array([[100000, 0, 35000], [30000000, 0, 10500000], [5000000, 0, 1750000],
                          [0,0,0], [1055000, 0, 369250]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3),
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()