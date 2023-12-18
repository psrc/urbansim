# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, ma


class Tests(opus_unittest.OpusTestCase):

    def test_alias_file(self):
        # this tests aliases in the file 'aliases.py'
        # expr1 and expr2 are aliases, while expr3 is an ordinary variable, 
        # just to make sure that aliases and ordinary variables interoperate correctly
        expr1 = "opus_core.test_agent.income_times_10"
        expr2 = "opus_core.test_agent.income_times_5"
        expr3 = "opus_core.test_agent.income_times_2"
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
        self.assertTrue(ma.allclose(result1, array([10, 50, 100]), rtol=1e-6), "Error in test_alias_file")
        result2 = dataset.compute_variables([expr2])
        self.assertTrue(ma.allclose(result2, array([5, 25, 50]), rtol=1e-6), "Error in test_alias_file")
        result3 = dataset.compute_variables([expr3])
        self.assertTrue(ma.allclose(result3, array([2, 10, 20]), rtol=1e-6), "Error in test_alias_file")
         
if __name__=='__main__':
    opus_unittest.main()
