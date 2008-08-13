#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from opus_core.misc import safe_array_divide
from variable_functions import my_attribute_label


class population_per_acre(Variable):
    """The population of the zone / land acres in the zone. """
    _return_type = "int32"
    population = "population"
    acres_of_land = "acres_of_land"
    
    def dependencies(self):
        return [my_attribute_label(self.population), 
                my_attribute_label(self.acres_of_land)]
    
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return safe_array_divide(ds.get_attribute(self.population), 
                                 ds.get_attribute(self.acres_of_land))

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import int32
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.population_per_acre"
 
    def test_my_inputs(self):
        
        values = VariableTestToolbox().compute_variable(self.variable_name, {
            "zone":{ 
                "population":array([4,2,4,5,0]),
                "acres_of_land": array([210, 52.5, 105, 0, 0])}
            }, 
            dataset = "zone")

        should_be = array([4/210.0, 2/52.5, 4/105.0, 0.0, 0.0], dtype=int32)
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), 
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()