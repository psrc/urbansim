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

class simple_agent_alternative_interaction(Variable):
    """Test variable for the interaction of gridcells and households.  Multiplies 
    the G2 attribute of grid cells with the A2 attribute of households."""        
    
    def dependencies(self):
        return [attribute_label("gridcell", "g2"), 
                attribute_label("household", "a2")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply("a2", "g2")



from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.simple_agent_alternative_interaction"
    def test_full_tree(self):
        G2 = array([10, 20, 30])
        A2 = array([0, 4, 2, 100])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{ 
                "g2":G2}, 
            "household":{ 
                "a2":A2}}, 
            dataset = "household_x_gridcell")
        should_be = array([[0,   0,   0], 
                           [40,  80,  120], 
                           [20,  40,  60], 
                           [1000,2000,3000]])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()