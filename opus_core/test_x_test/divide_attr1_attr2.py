# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class divide_attr1_attr2(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def compute(self, dataset_pool):
        values = self.get_dataset().divide('attr1', 'attr2')
        return values
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "opus_core.test_x_test.divide_attr1_attr2"
    
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
        test_x_test.compute_variables(self.variable_name, 
                                            dataset_pool=dataset_pool)
        values = test_x_test.get_attribute(self.variable_name)
        
        should_be = array([[1./10, 2./10], [1./100, 2./100]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-20),
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()