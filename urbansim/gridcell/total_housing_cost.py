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
from variable_functions import my_attribute_label

class total_housing_cost(Variable):
    """housing_cost x number of residential units"""
            
    housing_cost = "housing_cost"
    residential_units = "residential_units"

    def dependencies(self):
        return [my_attribute_label(self.housing_cost),
                my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        units = self.get_dataset().get_attribute(self.residential_units)
        return units * self.get_dataset().get_attribute(self.housing_cost)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        housing_cost = array([50, 75, 0, 5, 20.5, 1000])
        residential_units = array([1, 1, 0, 0, 2, 100])
        property_value_to_annual_cost_ratio = 10.3
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3,4,5,6]),
                    "housing_cost": housing_cost,
                    "residential_units":residential_units
                }
            }
        )
        should_be = array([50, 75, 0, 0, 41, 100000])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()