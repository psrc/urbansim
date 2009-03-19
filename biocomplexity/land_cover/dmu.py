# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import greater_equal, less_equal
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class dmu(Variable):
    """Urbansim development type mixed-use, where(devtype==[9|10|11|12|13|14|15|16])"""
    development_type_id = 'devt'

    def dependencies(self):
        return [my_attribute_label(self.development_type_id)]
        
    def compute(self, dataset_pool): 
        devt = self.get_dataset().get_attribute(name=self.development_type_id)
        return greater_equal(devt, 9) & less_equal(devt, 16)
    


from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.dmu"
    
    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name,             
            {"land_cover":{
                "devt": array([1, 10, 21, 12, 16, 9, 8, 17, 15])}},                 
            dataset = "land_cover")
        should_be = array([0, 1, 0, 1, 1, 1, 0, 0, 1])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)            
  
    def test_tree(self):            
        values = VariableTestToolbox().compute_variable(self.variable_name,             
                {"land_cover":{
                "lct":array([1, 2, 3]),
                "devgrid_id":array([1, 1, 2])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "development_type_id": array([10, 5, 3])}},                    
             dataset = "land_cover")
        should_be = array([1, 1, 0])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":        
    opus_unittest.main()