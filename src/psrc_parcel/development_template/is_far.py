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

class is_far(Variable):
    """
    Logical. Return True if the template is in far units otherwise False.
    """
    _return_type = "bool8"
    
    def dependencies(self):
        return ["development_template.density_type"]

    def compute(self, dataset_pool):
        dp = self.get_dataset()
        return dp.get_attribute("density_type") == 'far'

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x == 1", values)

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim'],
            test_data={            
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'density_type': array(['units_per_acre', 'far', 'units_per_acre', 'far']),
            },

            }
        )
        
        should_be = array([False, True, False, True])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    