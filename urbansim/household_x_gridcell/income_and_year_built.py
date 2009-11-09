# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_year_built(Variable):
    """income * year_built"""
    _return_type="float32"
    gc_year_built = "year_built"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_year_built),
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        self.gc_year_built)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import log
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.income_and_year_built"
    def test_full_tree(self):
        year_built = array([1980, 2000, 1910])
        income = array([1000, 300000, 50000, 0, 10550])
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{
                 "year_built":year_built},
             "household":{
                 "income":income}},
            dataset = "household_x_gridcell")
        should_be = array([[1980000, 2000000, 1910000], [594000000, 600000000, 573000000], [99000000, 100000000, 95500000],
                          [0,0,0], [20889000, 21100000, 20150500]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3),
                         True, msg = "Error in " + self.variable_name)

    # test_my_inputs not needed -- all inputs are primary attributes

if __name__=='__main__':
    opus_unittest.main()