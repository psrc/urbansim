# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import greater_equal, less_equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dt(Variable):
    """UrbanSim development type mixed-use, where(devtype==24)
    
    Problem - UrbanSim Development Type Typology HAS NO Transportation class
    Work around for King County LCCM is to either remove from MNL equations     
    development_type_id = 'devt'
    (meaning restimating them) or to use the DT.flt file in the INVARIANTS directory  """
    
    development_type_id = 'devt'
    
    def dependencies(self):
        return [my_attribute_label(self.development_type_id)] 
            
    def compute(self, dataset_pool): 
        return self.get_dataset().get_attribute(name=self.development_type_id) == 24
        

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dt"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devt": array([15, 24, 21, 23, 22])}}, # dt devt's is 24
            dataset = "land_cover")
        should_be = array([0, 1, 0, 0, 0])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)

    def test_on_expected_data(self):
        self.do_test_on_expected_data(["devt"])


if __name__=='__main__':
    opus_unittest.main()