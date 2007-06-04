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

class has_population_within_walking_distance(Variable):
    """Boolean indicating whether the gridcell has any households within walking distance"""

    population = "number_of_households_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.population)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.population) > 0

    def post_check(self, values, dataset_pool):
        self.do_check("x == True or x == False", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1, 2, 3]),
                    "number_of_households_within_walking_distance":array([1, 0, 5])
                }
            } 
        )
        
        should_be = array([True, False, True])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()