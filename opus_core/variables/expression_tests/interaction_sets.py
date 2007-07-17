#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
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
        # the VariableName for this expression should not have dataset_name set, since there are
        # two different dataset names in expr
        name = VariableName(expr)
        self.assertEqual(name.get_dataset_name(), None, msg="bad value for dataset")

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

if __name__=='__main__':
    opus_unittest.main()
