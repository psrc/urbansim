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

class acres_of_open_space(Variable):
    """Acres of open space for a given gridcell, based on the
    water percentage for that given gridcell"""
    
    _return_type = "float32"
    percent_open_space = "percent_open_space"

    def dependencies(self):
        return [my_attribute_label(self.percent_open_space)]

    def compute(self, dataset_pool):
        return (1.0-(self.get_dataset().get_attribute(self.percent_open_space)/100.0)) * \
                dataset_pool.get_dataset('urbansim_constant')["acres"]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([33, 5, 20]),
                    'percent_open_space': array([33, 5, 20]),
                },
                'urbansim_constant':{
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([(1.0 - (33/100.0))*105.0, 
                           (1.0 - (5/100.0))*105.0, 
                           (1.0 - (20/100.0))*105.0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
