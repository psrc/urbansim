# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

# This is a simple test variable for the interaction of gridcells and households.

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class hhnper2_nbnper2(Variable):
    """Test variable for the interaction of neighborhoods and households.  
    Computes household.poor * neighborhood.poor."""        
    
    def dependencies(self):
        return [attribute_label("neighborhood", "nper2_m"), 
                attribute_label("household", "nper2")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply("nper2", "nper2_m")


#if __name__=='__main__':
    #from opus_core.tests import opus_unittest
    #from urbansim.variable_test_toolbox import VariableTestToolbox
    #from numpy import array
    #from numpy import ma
    #class Tests(opus_unittest.OpusTestCase):
        #variable_name = "urbansim.household_x_neighborhood.hhrich_nbpoor"
        #def test_full_tree(self):
            #dept = array([10, 20, 30])
            #prev_dept = array([10, 4, 20, 30])
            
            #values = VariableTestToolbox().compute_variable(self.variable_name, 
                #{"neighborhood":{ 
                    #"dept":dept}, 
                #"household":{ 
                    #"prev_dept":prev_dept}}, 
                #dataset = "household_x_neighborhood")
            #should_be = array([[1,  0,  0], 
                               #[0,  0,  0], 
                               #[0,  1,  0], 
                               #[0,  0,  1]])

            #self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), 
                             #True, msg = "Error in " + self.variable_name)
    #opus_unittest.main()
