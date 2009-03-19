# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, ma

class Tests(opus_unittest.OpusTestCase):

    def test_fully_qualified_variable(self):
        # this tests an expression consisting of a fully-qualified variable
        expr = "opus_core.test_agent.income_times_2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "income":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result = dataset.compute_variables([expr])
        should_be = array([2, 10, 20])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_fully_qualified_variable")
        # check that expr is in the cache of known expressions
        # (normally we shouldn't be accessing this private field, but just this once ...)
        cache = VariableName._cache
        self.assert_(expr in cache, msg="did not find expr in cache")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        self.assertEqual(name.get_package_name(), 'opus_core', msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), 'test_agent', msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), 'income_times_2', msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'income_times_2', msg="bad value for alias")
        self.assertEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        # test that the variable can now also be accessed using its short name in an expression
        result2 = dataset.compute_variables(['income_times_2'])
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_variable")
        # check that the cache uses the variable name with whitespace removed
        oldsize = len(cache)
        expr_with_spaces = "opus_core . test_agent. income_times_2  "
        name2 = VariableName(expr_with_spaces)
        newsize = len(cache)
        self.assertEqual(oldsize, newsize, msg="caching error")
        self.assert_(expr_with_spaces not in cache, msg="caching error")
        self.assertEqual(expr_with_spaces, name2.get_expression(), msg="caching error")
        self.assertEqual(name2.get_short_name(), 'income_times_2', msg="bad value for shortname")
       
    def test_fully_qualified_DDD_SSS_variable(self):
        # this should use the test variable a_test_SSS_variable_DDD_SSS
        expr = "opus_core.tests.a_test_squid_variable_42_clam"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result = dataset.compute_variables([expr])
        should_be = array([10,50,100])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_fully_qualified_DDD_SSS_variable")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        self.assertEqual(name.get_package_name(), 'opus_core', msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), 'tests', msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), 'a_test_squid_variable_42_clam', msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'a_test_squid_variable_42_clam', msg="bad value for alias")
        self.assertEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        # test that the variable can now also be accessed using its short name in an expression
        result2 = dataset.compute_variables(['a_test_squid_variable_42_clam'])
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_squid_variable_42_clam")

    
    def test_attribute(self):
        # this tests an expression consisting of just a primary attribute
        expr = "persons"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result = dataset.compute_variables([expr])
        self.assertEqual(ma.allclose(result, [1,5,10], rtol=1e-7), True, msg="error in test_attribute")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        self.assertEqual(name.get_package_name(), None, msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), None, msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), 'persons', msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'persons', msg="bad value for alias")
        self.assertEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        
    def test_dataset_qualified_attribute(self):
        expr = "tests.persons"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result = dataset.compute_variables([expr])
        self.assertEqual(ma.allclose(result, [1,5,10], rtol=1e-7), True, msg="error in test_attribute")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        self.assertEqual(name.get_package_name(), None, msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), 'tests', msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), 'persons', msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'persons', msg="bad value for alias")
        self.assertEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        
if __name__=='__main__':
    opus_unittest.main()
