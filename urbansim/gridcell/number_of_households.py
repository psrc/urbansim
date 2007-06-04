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

class number_of_households(Variable):
    """Number of households in a given gridcell"""

    _return_type="int32"
    
    def dependencies(self):
        return [attribute_label("household", "grid_id"), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, constant=1)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('household').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1, 2, 3, 4])
                    }, 
                "household":{ 
                    "household_id":array([1, 2, 3, 4, 5, 6]),
                    "grid_id":array([1, 2, 3, 4, 2, 2])
                }
            } 
        )
        
        should_be = array([1,3,1,1])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()