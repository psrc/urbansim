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

class acres_per_gridcell(Variable):
    """total acres of land for a given gridcell (ignoring percent water).  This is also available in urbansim_constants; it is defined
    as a variable so that it can be used in an expression"""

    _return_type = "float32"

    def dependencies(self):
        return [my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        return 0*self.get_dataset().get_attribute("grid_id") + dataset_pool.get_dataset('urbansim_constant')["acres"]


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3]),
                },
                'urbansim_constant':{
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([105.0, 105.0, 105.0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
