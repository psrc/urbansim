# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, ma, arange

class Tests(opus_unittest.OpusTestCase):

    def test_interaction_set_aggregate(self):
        # Test doing an aggregate on an interaction set component.  The interaction set is 
        # test_agent_x_test_location, and test_location will be aggregated from gridcell.  
        # (It would be nicer if test_location were called zone, but we wanted to use the existing 
        # test interactions set.)
        expr = "test_location.aggregate(gridcell.my_variable)"
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
        should_be = array([ [4.5, 9], [4.5, 9], [4.5, 9] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_aggregate")
     
    def test_interaction_set_aggregate2(self):
        # Similar to test_interaction_set_aggregate, except that it uses test_location_x_test_agent
        expr = "test_location.aggregate(gridcell.my_variable)"
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
        should_be = array([ [4.5, 4.5, 4.5], [9, 9, 9] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_aggregate2")
     
    def test_interaction_set_aggregate_and_multiply(self):
        # test doing an aggregate on an interaction set component and using the result in a multiply operation
        # this is the same as test_interaction_set_aggregate except that we multiply by test_agent.income
        expr = "test_agent.income * test_location.aggregate(gridcell.my_variable)"
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
        should_be = array([ [4.5, 9], [90, 180], [2250, 4500] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_aggregate_and_multiply")
     
    def test_interaction_set_aggregate_and_multiply2(self):
        # Similar to test_interaction_set_aggregate_and_multiply, except that it uses test_location_x_test_agent
        expr = "test_location.aggregate(gridcell.my_variable) * test_agent.income"
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
        should_be = array([ [4.5, 90, 2250], [9, 180, 4500] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_aggregate_and_multiply2")
     
    def test_interaction_set_disaggregate(self):
        # Test doing a disaggregate on an interaction set component.  The interaction set is 
        # test_agent_x_test_location, and test_location will be disaggregated from faz.  
        # (It would be nicer if test_location were called zone, but we wanted to use the existing 
        # test interactions set.)
        expr = "test_location.disaggregate(myfaz.my_variable)"
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
        should_be = array([ [4, 8, 4, 8], [4, 8, 4, 8], [4, 8, 4, 8] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate")
       
    def test_interaction_set_disaggregate2(self):
        # Similar to test_interaction_set_disaggregate, except that it uses test_location_x_test_agent
        expr = "test_location.disaggregate(myfaz.my_variable)"
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
        should_be = array([ [4, 4, 4], [8, 8, 8], [4, 4, 4], [8, 8, 8] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate2")
       
    def test_interaction_set_disaggregate_and_multiply(self):
        # test doing a disaggregate on an interaction set component and using the result in a multiply operation
        # this is the same as test_interaction_set_disaggregate except that we multiply by test_agent.income
        expr = "test_agent.income * test_location.disaggregate(myfaz.my_variable)"
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
        should_be = array([ [4, 8, 4, 8], [80, 160, 80, 160], [2000, 4000, 2000, 4000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate_and_multiply")

    def test_interaction_set_disaggregate_and_multiply2(self):
        # Similar to test_interaction_set_disaggregate_and_multiply, except that it uses test_location_x_test_agent
        expr = "test_location.disaggregate(myfaz.my_variable) * test_agent.income"
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
        should_be = array([ [4, 80, 2000], [8, 160, 4000], [4, 80, 2000], [8, 160, 4000] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in interaction_set_disaggregate_and_multiply2")
        
    def test_interaction_set_number_of_agents(self):
        # Test number_of_agents on an interaction set component.  The interaction set is 
        # test_agent_x_test_location, and we are finding the number of agents in each location
        expr = "test_location.number_of_agents(myjob)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id':array([1,2,3])}
            )
        storage.write_table(
            table_name='jobs', 
            table_data={'jid':arange(4)+1, 'id':array([2, 1, 3, 1]) }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        jobs = Dataset(in_storage=storage, in_table_name='jobs', id_name="jid", dataset_name="myjob")       
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myjob', jobs)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [2, 1, 1]
        should_be = array([ [2, 1, 1], [2, 1, 1], [2, 1, 1] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_number_of_agents")
       
    def test_interaction_set_number_of_agents2(self):
        # Similar to test_interaction_set_number_of_agents, except that it uses test_location_x_test_agent
        expr = "test_location.number_of_agents(myjob)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id':array([1,2,3])}
            )
        storage.write_table(
            table_name='jobs', 
            table_data={'jid':arange(4)+1, 'id':array([2, 1, 3, 1]) }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        jobs = Dataset(in_storage=storage, in_table_name='jobs', id_name="jid", dataset_name="myjob")       
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myjob', jobs)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [2, 1, 1]
        should_be = array([ [2, 2, 2], [1, 1, 1], [1, 1, 1] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_number_of_agents2")
        
    def test_interaction_set_number_of_agents_and_multiply(self):
        # Test number_of_agents on an interaction set component and using the result in a multiply operation
        # this is the same as test_interaction_set_number_of_agents except that we multiply by test_agent.income
        expr = "test_agent.income * test_location.number_of_agents(myjob)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id':array([1,2,3])}
            )
        storage.write_table(
            table_name='jobs', 
            table_data={'jid':arange(4)+1, 'id':array([2, 1, 3, 1]) }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        jobs = Dataset(in_storage=storage, in_table_name='jobs', id_name="jid", dataset_name="myjob")       
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myjob', jobs)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [2, 1, 1]
        should_be = array([ [2, 1, 1], [40, 20, 20], [1000, 500, 500] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_number_of_agents_and_multiply")
       
    def test_interaction_set_number_of_agents_and_multiply2(self):
        # Similar to test_interaction_set_number_of_agents_and_multiply, except that it uses test_location_x_test_agent
        expr = "test_agent.income * test_location.number_of_agents(myjob)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id':array([1,2,3])}
            )
        storage.write_table(
            table_name='jobs', 
            table_data={'jid':arange(4)+1, 'id':array([2, 1, 3, 1]) }
            )
        ds = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name="test_location")
        jobs = Dataset(in_storage=storage, in_table_name='jobs', id_name="jid", dataset_name="myjob")       
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        dataset_pool._add_dataset('test_location', ds)
        dataset_pool._add_dataset('myjob', jobs)
        test_agent_x_test_location = dataset_pool.get_dataset('test_location_x_test_agent')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        # result for just test_location would be [2, 1, 1]
        should_be = array([ [2, 40, 1000], [1, 20, 500], [1, 20, 500] ])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_interaction_set_number_of_agents_and_multiply2")

if __name__=='__main__':
    opus_unittest.main()
