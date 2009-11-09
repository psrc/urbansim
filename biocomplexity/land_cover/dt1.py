# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dt1(Variable):
    """Developed in time 1.
       ie where land cover types are 1, 2 or 3"""
    land_cover_types = 'lct'
    
    def dependencies(self):
        return [my_attribute_label(self.land_cover_types)] 
                                         
    def compute(self, dataset_pool): 
        lct = self.get_dataset().get_attribute(name=self.land_cover_types)
        return equal(lct, 1) | equal(lct, 2) | equal(lct, 3)
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dt1"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([1, 0, 1])
        
        self.assertEqual(ma.allequal(values, should_be), 
                         True, msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["lct"])                             

if __name__=='__main__':
    opus_unittest.main()