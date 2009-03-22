# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import array, ma


class Tests(opus_unittest.OpusTestCase):

    def test_constants(self):
        # test an expression involving two dataset names, one of which is *_constant
        expr = "test_agent.age<=opus_constant.young_age"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "age":array([30,20,60,80]),
                "id":array([1,3,4,10])
                }
            )
        storage.write_table(
            table_name='opus_constants',
            table_data={
                "young_age":array([35]),
                "opus_constant_id":array([1])
                }
            )
        dataset_pool = DatasetPool(storage=storage)
        # Test that the dataset name is correct for expr.  It should be test_agent -- opus_constant just holds constants, 
        # and is ignored as far as finding the dataset name for the expression.
        name = VariableName(expr)
        autogen = name.get_autogen_class()
        self.assertEqual(name.get_package_name(), None)
        self.assertEqual(name.get_dataset_name(), 'test_agent')
        # make an instance of the class and check the dependencies (it shouldn't depend on urbansim_constant)
        self.assertEqual(autogen().dependencies(), ['test_agent.age'])
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result = dataset.compute_variables([expr], dataset_pool=dataset_pool)
        should_be = array( [True,True,False,False] )
        self.assertEqual( ma.allequal( result, should_be), True)

if __name__=='__main__':
    opus_unittest.main()
