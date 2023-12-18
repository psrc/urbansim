# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import array, bool8

class is_minority(Variable):
    """Is the head of household a minority. """
    
    race_id = "race_id"
    minority = "minority"
    
    def dependencies(self):
        return [my_attribute_label(self.race_id), attribute_label("race", self.minority)]
            
    def compute(self, dataset_pool):
        races = dataset_pool.get_dataset('race')
        race_idx = races.get_attribute_by_id(self.minority, self.get_dataset().get_attribute(self.race_id))
        return races.get_attribute_by_index("minority", race_idx).astype(bool8)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_minority"

    def test_my_inputs( self ):
        race_id = array([2, 2, 3, 5])
        minority = array([0,1,1,1,0])
        
        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"household":{ 
                "race_id":race_id},
             "race":{"minority":minority}}, 
            dataset = "household" )
        should_be = array([1, 1, 1, 0])
        
        self.assertEqual( ma.allequal( values, should_be), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()