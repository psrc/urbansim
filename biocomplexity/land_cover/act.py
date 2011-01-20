# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


from opus_core.variables.variable import Variable
from numpy import ones
from numpy import float32

class act(Variable):
    """Alternative-specific constant
    This "variable" is always equal to one, making the ACT "coefficient" 
    in the equations table a constant value that is added to the the 
    logit equation."""
    
    def compute(self, dataset_pool): 
        return ones(shape=(self.get_dataset().size()), dtype=float32)
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "biocomplexity.land_cover.act"
    
    def test_my_inputs(self):
        land_cover_types = array([-9999, 5, 3, 1])
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct": land_cover_types}}, 
            dataset = "land_cover")
        should_be = array([1, 1, 1, 1])
        
        self.assertEqual(ma.allequal(values, should_be), 
                         True, msg = "Error in " + self.variable_name)            
    

if __name__ == "__main__":
    opus_unittest.main()