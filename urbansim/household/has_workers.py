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
from numpy import logical_not

class has_workers(Variable):
    """Has one or more workers """
    
    _return_type="bool8"
    workers = "workers"
    
    def dependencies(self):
        return [my_attribute_label(self.workers)]
            
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.workers) > 0


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.has_workers"

    def test_my_inputs( self ):
        w = array([2, 1, 0, 0])
        
        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"household":{ 
                "workers":w},
             }, 
            dataset = "household" )
        should_be = array([1, 1, 0, 0])
        
        self.assertEqual( ma.allequal( values, should_be), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()