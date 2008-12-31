#
# Opus software. Copyright (C) 2005-2008 University of Washington
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
from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.variables.variable_factory import VariableFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, ma
from sets import Set


class Tests(opus_unittest.OpusTestCase):

    def test_constants(self):
        # test an expression involving two dataset names, one of which is *_constant
        expr = "test_agent.age<=urbansim_constant.young_age"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "age":array([30,20,60,80]),
                "id":array([1,3,4,10])
                }
            )
        # Test that the dataset name is correct for expr.  It should be test_agent -- urbansim_constant just holds constants, 
        # and is ignored as far as finding the dataset name for the expression.
        name = VariableName(expr)
        autogen = name.get_autogen_class()
        self.assertEqual(name.get_package_name(), None)
        self.assertEqual(name.get_dataset_name(), 'test_agent')
        # make an instance of the class and check the dependencies (it shouldn't depend on urbansim_constant)
        self.assertEqual(autogen().dependencies(), ['test_agent.age'])
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        # uncomment this once the test is rewritten to not use urbansim_constant
#        result = dataset.compute_variables([expr])
#        should_be = array( [True,True,False,False] )
#        self.assertEqual( ma.allclose( result, should_be, rtol=1e-7), True)

if __name__=='__main__':
    opus_unittest.main()
