# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_without_children(Variable):
    """Does this household not have children."""
    
    children = "children"
    
    def dependencies(self):
        return [my_attribute_label(self.children)]
    
    def compute(self, dataset_pool):    
        return self.get_dataset().get_attribute(self.children) == 0


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_without_children"

    def test_my_inputs( self ):
        children = array([0, 1, 2, 1])

        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"household":{ 
                "children":children}}, 
            dataset = "household" )
        should_be = array( [1,0,0,0] )
        
        self.assertEqual( ma.allclose( values, should_be, rtol=1e-7 ), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()