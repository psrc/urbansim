# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, ma, int32, float64


class Tests(opus_unittest.OpusTestCase):

    def test_casts_fully_qualified_variable(self):
        expr1 = "opus_core.test_agent.income_times_10.astype(int32)"
        expr2 = "opus_core.test_agent.income_times_10.astype(int32)**2"
        expr3 = "(2*opus_core.test_agent.income_times_10).astype(int32)"
        error_msg = "Error in test_casts_fully_qualified_variable"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "income":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result1 = dataset.compute_variables([expr1])
        self.assertEqual( type(result1[0]), int32, error_msg)
        self.assert_(ma.allclose(result1, array([10, 50, 100]), rtol=1e-6), error_msg)
        result2 = dataset.compute_variables([expr2])
        self.assertEqual( type(result2[0]), int32, error_msg)
        self.assert_(ma.allclose(result2, array([100, 2500, 10000]), rtol=1e-6), error_msg)
        result3 = dataset.compute_variables([expr3])
        self.assertEqual( type(result3[0]), int32, error_msg)
        self.assert_(ma.allclose(result3, array([20, 100, 200]), rtol=1e-6), error_msg)
         
    def test_casts_dataset_qualified_attribute(self):
        expr1 = "tests.persons.astype(float64)"
        expr2 = "tests.persons.astype(float64)**2"
        expr3 = "(2*tests.persons).astype(float64)"
        error_msg = "Error in test_casts_dataset_qualified_attribute"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result1 = dataset.compute_variables([expr1])
        self.assertEqual( type(result1[0]), float64, error_msg)
        self.assert_(ma.allclose(result1, array([1, 5, 10]), rtol=1e-6), error_msg)
        result2 = dataset.compute_variables([expr2])
        self.assertEqual( type(result2[0]), float64, error_msg)
        self.assert_(ma.allclose(result2, array([1, 25, 100]), rtol=1e-6), error_msg)
        result3 = dataset.compute_variables([expr3])
        self.assertEqual( type(result3[0]), float64, error_msg)
        self.assert_(ma.allclose(result3, array([2, 10, 20]), rtol=1e-6), error_msg)
        
    def test_casts_attribute(self):
        expr1 = "persons.astype(float64)"
        expr2 = "persons.astype(float64)**2"
        expr3 = "(2*persons).astype(float64)"
        error_msg = "Error in test_casts_attribute"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result1 = dataset.compute_variables([expr1])
        self.assertEqual( type(result1[0]), float64, error_msg)
        self.assert_(ma.allclose(result1, array([1, 5, 10]), rtol=1e-6), error_msg)
        result2 = dataset.compute_variables([expr2])
        self.assertEqual( type(result2[0]), float64, error_msg)
        self.assert_(ma.allclose(result2, array([1, 25, 100]), rtol=1e-6), error_msg)
        result3 = dataset.compute_variables([expr3])
        self.assertEqual( type(result3[0]), float64, error_msg)
        self.assert_(ma.allclose(result3, array([2, 10, 20]), rtol=1e-6), error_msg)

if __name__=='__main__':
    opus_unittest.main()
