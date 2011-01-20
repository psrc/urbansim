# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.interaction_dataset import InteractionDataset

class TestXTestDataset(InteractionDataset):
    """Dataset used by InteractionDataset unit tests.
    """
    pass

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test(self):

        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                'id': array([1, 2]),
                'attr1': array([1, 2]),
                'attr2': array([10, 100]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['opus_core'],
                                   storage=storage)
        test_x_test = dataset_pool.get_dataset('test_x_test')
        test_x_test.compute_variables('opus_core.test_x_test.divide_attr1_attr2', 
                                      dataset_pool=dataset_pool)
        values = test_x_test.get_attribute('divide_attr1_attr2')
        
        should_be = array([[1./10, 2./10], [1./100, 2./100]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-20),
                     msg = "Error in test_x_test_dataset")
    
if __name__ == '__main__':
    opus_unittest.main()