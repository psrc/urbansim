# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import equal
from opus_core.variables.variable import Variable, ln
from biocomplexity.land_cover.variable_functions import my_attribute_label

class cd1(Variable):
    """Commercial density: ln(COMM_DEN+1)/10"""
    comm_den = 'comm_den'
    
    def dependencies(self):
        return [my_attribute_label(self.comm_den)] 
    
    def compute(self, dataset_pool): 
        return ln(self.get_dataset().get_attribute(self.comm_den)+1) / 10
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.cd1"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "comm_den": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([0.06931471, 0.17917594, 0.13862943])
        
        self.assert_(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)    
                     
    def test_on_expected_data(self):
        self.do_test_on_expected_data(["comm_den"])


if __name__=='__main__':
    opus_unittest.main()