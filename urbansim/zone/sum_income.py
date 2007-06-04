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
from variable_functions import my_attribute_label

class sum_income(Variable):
    """Sum of all income in a zone, by summing the incomes of each household in the zone"""

    _return_type="int64"
    hh_income = "income"

    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("household", self.hh_income), 
                attribute_label("household", "zone_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.hh_income)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.sum_income"
 
    def test_my_inputs(self):
        income = array([2100,2200,2700,4200, 0]) 
        zone_ids = array([1,2,1,3,2]) 
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"zone":{
                "zone_id":array([1,2, 3])}, 
            "household":{ 
                "income":income,
                "zone_id":zone_ids}}, 
            dataset = "zone")
        should_be = array([4800, 2200, 4200])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=0), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()