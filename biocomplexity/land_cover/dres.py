# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import greater_equal, less_equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dres(Variable):
    """UrbanSim development type residential - if 1 <= DEVT <= 8 then 1 else 0 """
    development_type_id = 'devt'
    
    def dependencies(self):
        return [my_attribute_label(self.development_type_id)] 
                                         
    def compute(self, dataset_pool): 
        devt = self.get_dataset().get_attribute(name=self.development_type_id)
        return greater_equal(devt, 1) & less_equal(devt, 8)
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dres"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devt": array([1, 9, 8, 3, 91])}}, # dres devt's are 1, 2...8
            dataset = "land_cover")
        should_be = array([1, 0, 1, 1, 0])
        
        self.assertEqual(ma.allequal(values, should_be), 
                         True, msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["devt"])


if __name__=='__main__':        
    opus_unittest.main()