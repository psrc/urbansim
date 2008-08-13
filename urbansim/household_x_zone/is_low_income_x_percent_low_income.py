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
from urbansim.functions import attribute_label

class is_low_income_x_percent_low_income(Variable):
    """Percent of households with high-income, given that the decision-making household is high-income.
    """    
    
    percent_low_income_households = "percent_low_income_households"
    hh_is_income = "is_low_income"
        
    def dependencies(self):
        return [attribute_label("zone", self.percent_low_income_households), 
                attribute_label("household", self.hh_is_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.percent_low_income_households,
                                            self.hh_is_income)

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_zone.is_low_income_x_percent_low_income"
        
    def test_my_inputs(self):
        percent_low_income_households = array([50, 10, 20])
        is_low_income = array([1, 0, 1, 0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                 "percent_low_income_households":percent_low_income_households}, 
             "household":{ 
                 "is_low_income":is_low_income}}, 
            dataset = "household_x_zone")
        should_be = array([[50, 10, 20], [0, 0, 0 ], [50, 10, 20], [0,0,0]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()