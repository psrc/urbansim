# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, ma, arange

class Tests(opus_unittest.OpusTestCase):
    # like Interaction_aggregate_disaggregate.py, except that the thing being aggregated is an expression
    # omits tests involving number_of_agents
    
    def test_interaction_set_aggregate(self):
        # Test doing an aggregate on an interaction set component.  The interaction set is 
        # test_agent_x_test_location, and test_location will be aggregated from gridcell.  
        # (It would be nicer if test_location were called zone, but we wanted to use the existing 
        # test interactions set.)
        expr = "test_location.aggregate(10.0*gridcell.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'location_id':array([1,2])
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'location_id':array([1,2,1,2]),
                }
            )
        location_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="location_id", dataset_name="test_location")
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', location_dataset)
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4.5, 9]
        should_be = array([ [45, 90], [45, 90], [45, 90] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_aggregate")
     
    def test_interaction_set_aggregate2(self):
        # Similar to test_interaction_set_aggregate, except that it uses test_location_x_test_agent
        expr = "test_location.aggregate(10.0*gridcell.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'location_id':array([1,2])
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'location_id':array([1,2,1,2]),
                }
            )
        location_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="location_id", dataset_name="test_location")
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', location_dataset)
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4.5, 9]
        should_be = array([ [45, 45, 45], [90, 90, 90] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_aggregate2")
     
    def test_interaction_set_aggregate_and_multiply(self):
        # test doing an aggregate on an interaction set component and using the result in a multiply operation
        # this is the same as test_interaction_set_aggregate except that we multiply by test_agent.income
        expr = "test_agent.income * test_location.aggregate(10.0*gridcell.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'location_id':array([1,2])
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'location_id':array([1,2,1,2]),
                }
            )
        location_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="location_id", dataset_name="test_location")
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', location_dataset)
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4.5, 9]
        should_be = array([ [45, 90], [900, 1800], [22500, 45000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_aggregate_and_multiply")
     
    def test_interaction_set_aggregate_and_multiply2(self):
        # Similar to test_interaction_set_aggregate_and_multiply, except that it uses test_location_x_test_agent
        expr = "test_location.aggregate(10.0*gridcell.my_variable) * test_agent.income"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'location_id':array([1,2])
                }
            )
        storage.write_table(
            table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'location_id':array([1,2,1,2]),
                }
            )
        location_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="location_id", dataset_name="test_location")
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', location_dataset)
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4.5, 9]
        should_be = array([ [45, 900, 22500], [90, 1800, 45000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_aggregate_and_multiply2")
     
    def test_interaction_set_aggregate_and_multiply_same_expr(self):
        # Test doing an aggregate on an interaction set component and using the result in a multiply operation
        # with the same expression.
        expr = "(test_agent.income+1)*test_location.aggregate(test_agent.income+1)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'location_id':array([1,2,2]), 'income': array([1, 20, 50])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'location_id':array([1,2])
                }
            )
        location_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="location_id", dataset_name="test_location")
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', location_dataset)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # test_agent.income+1 is [2, 21, 51]
        # test_location.aggregate(test_agent.income+1) is [2, 72]
        should_be = array([ [2*2, 2*72], [21*2, 21*72], [51*2, 51*72] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6))

    def test_interaction_set_disaggregate(self):
        # Test doing a disaggregate on an interaction set component.  The interaction set is 
        # test_agent_x_test_location, and test_location will be disaggregated from faz.  
        # (It would be nicer if test_location were called zone, but we wanted to use the existing 
        # test interactions set.)
        expr = "test_location.disaggregate(10.0*myfaz.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(
            table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4, 8, 4, 8]
        should_be = array([ [40, 80, 40, 80], [40, 80, 40, 80], [40, 80, 40, 80] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate")
       
    def test_interaction_set_disaggregate2(self):
        # Similar to test_interaction_set_disaggregate, except that it uses test_location_x_test_agent
        expr = "test_location.disaggregate(10.*myfaz.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(
            table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4, 8, 4, 8]
        should_be = array([ [40, 40, 40], [80, 80, 80], [40, 40, 40], [80, 80, 80] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate2")
       
    def test_interaction_set_disaggregate_and_multiply(self):
        # test doing a disaggregate on an interaction set component and using the result in a multiply operation
        # this is the same as test_interaction_set_disaggregate except that we multiply by test_agent.income
        expr = "test_agent.income * test_location.disaggregate(10.0*myfaz.my_variable)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(
            table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4, 8, 4, 8]
        should_be = array([ [40, 80, 40, 80], [800, 1600, 800, 1600], [20000, 40000, 20000, 40000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate_and_multiply")

    def test_interaction_set_disaggregate_and_multiply2(self):
        # Similar to test_interaction_set_disaggregate_and_multiply, except that it uses test_location_x_test_agent
        expr = "test_location.disaggregate(10.0*myfaz.my_variable) * test_agent.income"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(
            table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [4, 8, 4, 8]
        should_be = array([ [40, 800, 20000], [80, 1600, 40000], [40, 800, 20000], [80, 1600, 40000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate_and_multiply2")

if __name__=='__main__':
    opus_unittest.main()
