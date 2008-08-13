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

class total_land_value(Variable):
    """Sum of land values of locations."""

    residential_land_value = "residential_land_value"
    nonresidential_land_value = "nonresidential_land_value"

    def dependencies(self):
        return [my_attribute_label(self.residential_land_value), 
                my_attribute_label(self.nonresidential_land_value)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.residential_land_value) + \
               self.get_dataset().get_attribute(self.nonresidential_land_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        residential_land_value = array([100, 200, 300])
        nonresidential_land_value = array([1995, 2005, 2006])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "residential_land_value":residential_land_value, 
                    "nonresidential_land_value":nonresidential_land_value
                }
            }
        )
        
        should_be = array([2095, 2205, 2306])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()