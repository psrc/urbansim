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

class is_DDD_persons_x_percent_size_DDD_persons(Variable):
    """Percent of households with DDD persons, given that the decision-making household has DDD persons.
    """    
        
    def __init__(self, number1, number2):
        Variable.__init__(self)
        self.has_persons = "has_%s_persons" % number1
        self.percent_persons = "percent_%s_persons_households" % number2

    def dependencies(self):
        return [attribute_label("zone", self.percent_persons), 
                attribute_label("household", self.has_persons)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.percent_persons,
                                            self.has_persons)

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.is_1_persons_x_percent_size_1_persons"
        
    def test_my_inputs(self):
        percent_high_income_households = array([50, 10, 20])
        has_persons = array([1, 0, 1, 0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                 "percent_1_persons_households":percent_high_income_households}, 
             "household":{ 
                 "has_1_persons":has_persons}}, 
            dataset = "household_x_zone")
        should_be = array([[50, 10, 20], [0, 0, 0 ], [50, 10, 20], [0,0,0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()