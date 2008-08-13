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

class combine_2_datasets(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def dependencies(self):
        return ["opus_core.test.attr1_times_2", "opus_core.test2.attr1_times_4"]
        
    def compute(self, dataset_pool):
        values = self.get_dataset().get_attribute('attr1_times_2') / \
                    dataset_pool.get_dataset("test2").get_attribute("attr1_times_4")
        return values
        

from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
            __file__,
            package_order=['opus_core'],
            test_data={
                'test':{
                    'id': array([1, 2]),
                    'attr1': array([1, 2])},
                'test2': {
                     'id': array([1,2]),
                     'attr1': array([20, 15])}
                },
        )
        should_be = array([(1*2)/(20*4.0), (2*2)/(15*4.0)])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()