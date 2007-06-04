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

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_total_improvement_value(Variable):
    """Natural log of the total_improvement_value for this gridcell"""
    
    _return_type="float32"            
    total_improvement_value = "total_improvement_value"

    def dependencies(self):
        return [my_attribute_label(self.total_improvement_value)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.total_improvement_value))


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
                    "grid_id":array([1, 2, 3, 4, 5, 6]),
                    "total_improvement_value":array([50, 75, 0, 50, -20, 10000000000000000])
                }
            }
        )
        
        should_be = array([3.912023,  4.317488,  0.0, 3.912023, 0.0, 36.8413614])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()