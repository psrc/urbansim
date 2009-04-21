# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.storage_factory import StorageFactory
from numpy import array, ma

class Tests(opus_unittest.OpusTestCase):
    
    # Tests involving aggregation/disaggregation for InteractionSets are in interaction_aggregate_disaggregate
   
    def test_multiply(self):
        expr = 'test_agent.income*test_location.cost'
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id': array([1,2]), 'cost': array([1000, 2000])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        should_be = array([[1000, 2000], 
                           [20000, 40000], 
                           [500000, 1000000]])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), msg = "Error in " + expr)
        name = VariableName(expr)
        # since the expression involves both test_agent and test_location, the dataset name should be None
        # and the interaction set names should be (test_agent, test_location) or (test_location, test_agent)
        self.assertEqual(name.get_dataset_name(), None)
        names = name.get_interaction_set_names()
        self.assertEqual(len(names),2)
        self.assert_('test_agent' in names)
        self.assert_('test_location' in names)

    def test_divide(self):
        expr = 'test_location.cost/test_agent.income'
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id': array([1,2]), 'cost': array([1000, 2000])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        should_be = array([[1000, 2000], 
                           [50, 100], 
                           [2, 4]])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), msg = "Error in " + expr)
        
    def test_interaction_set_component(self):
        # test a fully-qualified variable that applies to a component of an interaction set
        expr = "opus_core.test_agent.income_times_2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id': array([1,2]), 'cost': array([1000, 2000])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        should_be = array([[2, 2], [40, 40], [1000, 1000]])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), msg = "Error in " + expr)
        # test that the interaction set now has this as an attribute
        result2 = test_agent_x_test_location.get_attribute('income_times_2')
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), msg = "Error in " + expr)
        # test that the variable can now also be accessed using its short name
        result3 = test_agent_x_test_location.compute_variables(['income_times_2'])
        self.assert_(ma.allclose(result3, should_be, rtol=1e-6), msg = "Error in " + expr)
        # even though we're using this with an interaction set, the dataset name for expr
        # should be the name of the component set (since that's the only one mentioned in expr)
        name = VariableName(expr)
        self.assertEqual(name.get_dataset_name(), 'test_agent', msg="bad value for dataset")

    def test_interaction_set_component_expression(self):
        # test an expression involving a fully-qualified variable that applies to a component of an interaction set
        expr = "3+opus_core.test_agent.income_times_2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id': array([1,2]), 'cost': array([1000, 2000])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        should_be = array([[5, 5], [43, 43], [1003, 1003]])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), msg = "Error in " + expr)
        
    def test_interaction_set_component_expression_alias(self):
        expr = "squid = 3+opus_core.test_agent.income_times_2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents', 
            table_data={'id': array([1, 2, 3]), 'income': array([1, 20, 500])}
            )
        storage.write_table(
            table_name='test_locations', 
            table_data={'id': array([1,2]), 'cost': array([1000, 2000])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_agent_x_test_location = dataset_pool.get_dataset('test_agent_x_test_location')
        result = test_agent_x_test_location.compute_variables(expr, dataset_pool=dataset_pool)
        should_be = array([[5, 5], [43, 43], [1003, 1003]])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), msg = "Error in " + expr)
        # test that the interaction set now has this as an attribute
        result2 = test_agent_x_test_location.get_attribute('squid')
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), msg = "Error in " + expr)
        # test that the value can now also be accessed using the alias
        result3 = test_agent_x_test_location.compute_variables(['squid'])
        self.assert_(ma.allclose(result3, should_be, rtol=1e-6), msg = "Error in " + expr)

    def test_agent_times_choice(self):
        expression = 'agent_x_choice.agent_times_choice(attr)'
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='agents', 
            table_data={'id': array([1, 2, 3, 4, 5]), 'attr_2': array([3,   2,   4,   10, 20]), 
                                                      'attr_3': array([10, 100, 1000, 500, 0]),
                                                      'attr_4': array([100, 500, 0, 20, -30])
                        }
            )
        storage.write_table(table_name='choices', 
            table_data={'id': array([1, 2, 3, 4])}
            )
        agents = Dataset(in_storage=storage, in_table_name='agents', dataset_name='agent', id_name='id')
        choices = Dataset(in_storage=storage, in_table_name='choices', dataset_name='choice', id_name='id')
        ids = InteractionDataset(dataset1=agents, dataset2=choices, index1=array([0,1,3,4]), index2=array([1,2,3])) 
        result = ids.compute_variables(expression)
        should_be = array([[3, 10, 100], [2,100,500], [10,500, 20], [20, 0, -30]])
        self.assertEqual(ma.allequal(result, should_be), True)
        
        agents.touch_attribute('attr_2') # in order to recompute the expression
        choices.add_primary_attribute(name='name', data=array(['bus', 'car', 'tran', 'walk']))
        agents.add_primary_attribute(name='attr_tran', data=array([100, 1000, 10000, 5000,10]))
        result = ids.compute_variables(expression)
        should_be = array([[3, 100, 100], [2,1000,500], [10,5000, 20], [20, 10, -30]])
        self.assertEqual(ma.allequal(result, should_be), True)
        
if __name__=='__main__':
    opus_unittest.main()
