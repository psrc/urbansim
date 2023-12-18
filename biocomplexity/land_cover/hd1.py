# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import equal
from opus_core.variables.variable import Variable, ln
from biocomplexity.land_cover.variable_functions import my_attribute_label

class hd1(Variable):
    """housing_density_per_acre:
         ln ( residential, condo, and apartment number of units in current year / number of acres + 1) / 10
         or ln(HOUSE_DEN + 1) / 10"""
    house_den = 'house_den'
    
    def dependencies(self):
        return [my_attribute_label(self.house_den)] 
    
    def compute(self, dataset_pool): 
        return ln(self.get_dataset().get_attribute(self.house_den) + 1) / 10
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.hd1"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "house_den": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([0.06931471, 0.17917594, 0.13862943])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["house_den"])
        

if __name__=='__main__':
    opus_unittest.main()