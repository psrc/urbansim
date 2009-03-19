# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from numpy import array, ma


class Tests(opus_unittest.OpusTestCase):

    def test_alias_attribute(self):
        # this tests an expression consisting of an alias for a primary attribute
        expr = "p = persons"
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
        self.assertEqual(ma.allclose(result, [1,5,10], rtol=1e-7), True, msg="error in test_alias_attribute")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        self.assertEqual(name.get_package_name(), None, msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), None, msg="bad value for dataset")
        self.assert_(name.get_short_name().startswith('autogen'), msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'p', msg="bad value for alias")
        self.assertNotEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        
    def test_alias_attribute_same_name(self):
        # this tests an expression consisting of an alias for a primary attribute that is the same name as the primary attribute
        expr = "persons = persons"
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
        self.assertEqual(ma.allclose(result, [1,5,10], rtol=1e-7), True, msg="error in test_alias_attribute")
        name = VariableName(expr)
        self.assertEqual(name.get_short_name(), 'persons', msg="bad value for shortname")
        self.assertEqual(name.get_alias(), 'persons', msg="bad value for alias")
        self.assertEqual(name.get_autogen_class(), None, msg="bad value for autogen_class")
        
    def test_alias_attribute_with_modification(self):
        # this tests an expression consisting of an alias for a primary attribute that is modified
        expr = "p = persons"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "persons":array([1,5,10]),
                "id":array([1,3,4])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        # modify the primary attribute 'persons'
        new_values = array([3, 0, 100])
        dataset.modify_attribute('persons', new_values)
        # result should have the new values
        result = dataset.compute_variables([expr])
        self.assertEqual(ma.allclose(result, new_values, rtol=1e-7), True, msg="error in test_alias_attribute_with_modification")
        
    def test_alias_complex_expression(self):
        # aliasing a complex expression
        expr = "x = 2*sqrt(var1+var2)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "var2": array([3,3,7,7]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([ 5.29150262, 0.0,  5.47722558,  5.65685425])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_alias_complex_expression")
        # check that the new var has x as an alias
        v = VariableName(expr)
        self.assertEqual(v.get_alias(), 'x', msg="bad value for alias")
        # check that the alias gives the correct value
        result2 = dataset.compute_variables(['x'])
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_variable")
     
    def test_alias_fully_qualified_variable(self):
        expr = "x = opus_core.tests.a_test_variable"
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
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_alias_fully_qualified_variable")
        # check that the new var has x as an alias
        v = VariableName(expr)
        self.assertEqual(v.get_package_name(), None, msg="bad value for package_name")
        self.assertEqual(v.get_dataset_name(), 'tests', msg="bad value for dataset_name")
        self.assert_(v.get_short_name().startswith('autogen'), msg="bad value for shortname")
        self.assertEqual(v.get_alias(), 'x', msg="bad value for alias")
        self.assertNotEqual(v.get_autogen_class(), None, msg="bad value for autogen_class")
        # check that the alias has the correct value
        result2 = dataset.compute_variables(['x'])
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_variable")

    def test_alias_fully_qualified_variable_same_name(self):
        expr = "a_test_variable = opus_core.tests.a_test_variable"
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
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_alias_fully_qualified_variable")
        result2 = dataset.compute_variables(['a_test_variable'])
        self.assert_(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_variable")
        v = VariableName(expr)
        # check that no autogen class was generated
        self.assertEqual(v.get_autogen_class(), None, msg="bad value for autogen_class")        
        # check that the alias is correct
        self.assertEqual(v.get_alias(), 'a_test_variable', msg="bad value for alias")

    def test_alias_with_delete_computed_attributes(self):
        # Make an alias for an expression, then delete all computed attributes, then use the same alias
        # for a different expression.  This tests that the dictionary of aliases that have been defined
        # is cleared when you delete attributes.
        expr1 = "x = 2*sqrt(var1+var2)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "var2": array([3,3,7,7]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr1])
        should_be = array([ 5.29150262, 0.0,  5.47722558,  5.65685425])
        self.assert_(ma.allclose(result, should_be, rtol=1e-6), "Error in test_alias_with_delete_computed_attributes")
        dataset.delete_computed_attributes()
        # now alias x to a different expression
        expr2 = "x = var1+10"
        # check that the new var has x as an alias
        result2 = dataset.compute_variables([expr2])
        should_be2 = array([14, 2, 10.5, 11])
        self.assert_(ma.allclose(result2, should_be2, rtol=1e-6), "Error in test_alias_with_delete_computed_attributes")
         
if __name__=='__main__':
    opus_unittest.main()
