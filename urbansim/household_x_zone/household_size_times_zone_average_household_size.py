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
from urbansim.functions import attribute_label
from numpy import float32

class household_size_times_zone_average_household_size(Variable):
    """ average_household_size * household_size""" 
    z_average_household_size = "average_household_size"
    hh_size = "persons"
    
    def dependencies(self):
        return [attribute_label("zone", self.z_average_household_size), 
                attribute_label("household", self.hh_size)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_size, self.z_average_household_size)
                

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.household_size_times_zone_average_household_size"
    def test_my_inputs(self):
        average_household_size = array([333.0, 500.55, 1000.26, 459])
        household_size = array([1, 20, 500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "average_household_size":average_household_size}, 
            "household":{ 
                "persons":household_size}}, 
            dataset = "household_x_zone")
        should_be = array([[333.0, 500.55, 1000.26, 459.0], [6660.0, 10011., 20005.2, 9180], 
                            [166500.,  250275.,  500130.,  229500.]])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-3), True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()