# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dc(Variable):
    """UrbanSim development type commercial - if DEVT == 17,18,19 then 1 else 0"""
    development_type_id = 'devt'
    
    def dependencies(self):
        return [my_attribute_label(self.development_type_id)] 
                                         
    def compute(self, dataset_pool): 
        devt = self.get_dataset().get_attribute(name=self.development_type_id)
        return equal(devt, 17) | equal(devt, 18) | equal(devt, 19)
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dc"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devt": array([17, 9, 18, 3, 19])}}, # dc devt's are 17,18,19
            dataset = "land_cover")
        should_be = array([1, 0, 1, 0, 1])
        
        self.assertEqual(ma.allequal(values, should_be), 
                         True, msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["devt"])


if __name__=='__main__':
    opus_unittest.main()