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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import array, bool8

class is_not_minority(Variable):
    """Is the head of household not a minority, i.e., white. """
    
    def dependencies(self):
        return [my_attribute_label("is_minority")]
            
    def compute(self, dataset_pool):
        return 1 - self.get_dataset().get_attribute("is_minority")


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_not_minority"

    def test_my_inputs( self ):
        race_id = array([2, 2, 3, 5])
        minority = array([0,1,1,1,0])
        
        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"household":{ 
                "race_id":race_id},
             "race":{"minority":minority}}, 
            dataset = "household" )
        should_be = array([0, 0, 0, 1])
        
        self.assertEqual( ma.allequal( values, should_be), True, msg = "Error in " + self.variable_name )

    
if __name__=='__main__':
    opus_unittest.main()