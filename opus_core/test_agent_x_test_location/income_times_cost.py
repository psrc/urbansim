# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable

class income_times_cost(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def compute(self, dataset_pool):
        values = self.get_dataset().multiply('income', 'cost')
        return values
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "opus_core.test_agent_x_test_location.income_times_cost"
    
    def test(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='test_agents',
            table_data={
                'id': array([1, 2, 3]),
                'income': array([1, 20, 500]),
            }
        )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'id': array([1,2]),
                'cost': array([1000, 2000]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['opus_core'],
                                   storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        values = test_agent_x_test_location.compute_variables(self.variable_name, 
                                            dataset_pool=dataset_pool)
        
        should_be = array([[1000, 2000], 
                           [20000, 40000], 
                           [500000, 1000000]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-20),
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()