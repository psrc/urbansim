# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dos(Variable):
    """UrbanSim development type open space  if DEVT == 24, 26, 29 then 1 else 0"""
    development_type_id = 'devt'
    
    def dependencies(self):
        return [my_attribute_label(self.development_type_id)] 
                                         
    def compute(self, dataset_pool): 
        dev_types = self.get_dataset().get_attribute(name=self.development_type_id)
        return equal(dev_types, 24) | equal(dev_types, 26) | equal(dev_types, 29)
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dos"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devt": array([15, 24, 29])}}, # dos devt's are 24, 26 and 29
            dataset = "land_cover")
        should_be = array([0, 1, 1])
        
        self.assertEqual(ma.allequal(values, should_be), 
                         True, msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["devt"])


if __name__=='__main__':
    opus_unittest.main()