# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import greater_equal, less_equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class di(Variable):
    """UrbanSim development type mixed-use, where(devtype==[20|21|22])"""
    development_type_id = 'devt'
    
    def dependencies(self):
        return [my_attribute_label(self.development_type_id)] 
            
    def compute(self, dataset_pool): 
        devt = self.get_dataset().get_attribute(name=self.development_type_id)
        return greater_equal(devt, 20) & less_equal(devt, 22)
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest

class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.di"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devt": array([15, 20, 21, 23, 22])}}, # di devt's are 20..22
            dataset = "land_cover")
        should_be = array([0, 1, 1, 0, 1])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["devt"])


if __name__=='__main__':
    opus_unittest.main()