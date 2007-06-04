#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

# This is a simple test variable for the interaction of gridcells and households.

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class hhnper3_nbnper3(Variable):
    """Test variable for the interaction of neighborhoods and households.  
    Computes household.poor * neighborhood.poor."""        
    
    def dependencies(self):
        return [attribute_label("neighborhood", "nper3_m"), 
                attribute_label("household", "nper3")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply("nper3", "nper3_m")


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
