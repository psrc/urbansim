# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.variables.variable_factory import VariableFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, ma

class Tests(opus_unittest.OpusTestCase):

    def test_unary_functions_fully_qualified_name(self):
        # this tests expressions with unary functions applied to a fully qualified name
        expr = "sqrt(opus_core.tests.a_test_variable)"
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
        should_be = array([3.16227766, 7.0710678, 10])
        self.assertEqual(ma.allclose(result, should_be, rtol=1e-3), True, msg="error in test_unary_functions_fully_qualified_name")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        autogen = name.get_autogen_class()
        self.assertTrue(issubclass(autogen, Variable), msg="autogen'd class isn't a Variable")
        self.assertEqual(name.get_package_name(), None, msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), 'tests', msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), autogen.__name__, msg="bad value for shortname")
        self.assertEqual(name.get_alias(), autogen.__name__, msg="bad value for alias")
        # make an instance of the class and check the dependencies (since the dependent variables
        # all have fully-qualifed names we don't need to associate a dataset with the variable
        # for this test)
        self.assertEqual(autogen().dependencies(), ['opus_core.tests.a_test_variable'], 
                         msg="dependencies are incorrect")
        
    def skip_test_dataset_qualified_name(self):
        # this tests expressions with a dataset-qualified name
        expr = "sqrt(tests.a_test_variable)"
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
        should_be = array([3.16227766, 7.0710678, 10])
        self.assertEqual(ma.allclose(result, should_be, rtol=1e-5), True)
        
    def test_attr_power(self):
        # Attributes and fully-qualified names to a power require separate parse tree patterns,
        # which are tested in the following two tests.
        # test attribute to a power
        expr = "var1**3"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([64, -512, 0.125, 1])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_attr_power")
        # check the dependencies (trickier for ** because we need a separate attribute tree pattern)
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        self.assertEqual(var.dependencies(), ['mydataset.var1'], msg="dependencies are incorrect")

    def test_fully_qualified_name_power(self):
        # test fully qualified name to a power
        expr = "opus_core.tests.a_test_variable**2"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,0]),
                "id":array([1,3])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        result = dataset.compute_variables([expr])
        should_be = array([100,0])
        self.assertEqual(ma.allclose(result, should_be, rtol=1e-5), True, msg="error in test_fully_qualified_name_power")
        # check the dependencies
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        self.assertEqual(var.dependencies(), ['opus_core.tests.a_test_variable'], msg="dependencies are incorrect")
        
    def test_expression(self):
        # test an expression.  Also make sure that the generated variable can be accessued 
        # using its short name and that dependencies are correct.
        expr = "2*sqrt(my_variable+10)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"my_variable": array([4,-8,0.5,1]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([ 7.48331477,  2.82842712,  6.4807407 ,  6.63324958])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_expression")
        # check the name
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        self.assertEqual(var.name(), expr, msg="name is incorrect")
        # check the dependencies
        self.assertEqual(var.dependencies(), ['mydataset.my_variable'], msg="dependencies are incorrect")
        # test that the variable can now also be accessed using its short name in an expression
        result2 = dataset.compute_variables([v.get_short_name()])
        self.assertTrue(ma.allclose(result2, should_be, rtol=1e-6), "Error in accessing a_test_variable")

    def test_two_expressions(self):
        # test having two different expressions (to make sure having two autogen'd classes at once is working)
        expr1 = "2*sqrt(my_variable+10)"
        expr2 = "3*sqrt(my_variable+10)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"my_variable": array([4,-8,0.5,1]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result1 = dataset.compute_variables([expr1])
        should_be1 = array([ 7.48331477, 2.82842712, 6.4807407, 6.63324958])
        self.assertTrue(ma.allclose(result1, should_be1, rtol=1e-6), "Error in test_two_expressions")
        result2 = dataset.compute_variables([expr2])
        should_be2 = array([11.22497216, 4.24264068, 9.72111105,  9.94987437])
        self.assertTrue(ma.allclose(result2, should_be2, rtol=1e-6), "Error in test_two_expressions")

    def test_expression_2vars(self):
        # test an expression with 2 variables
        expr = "2*sqrt(var1+var2)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,-8,0.5,1]), "var2": array([3,3,7,7]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([ 5.29150262, 0.0,  5.47722558,  5.65685425])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_expression_2vars")
        # check the dependencies (will depend on two different other variables)
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        # use sets for the equality test, since we don't know in what order the dependencies will be returned
        self.assertEqual(set(var.dependencies()), set(['mydataset.var1', 'mydataset.var2']), 
                         msg="dependencies are incorrect")

    def test_expression_1var_2times(self):
        # test an expression with two occurences of the same variable 
        # (the var should just occur once in dependencies)
        expr = "var1+sqrt(var1)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={"var1": array([4,25,0,1]), "id": array([1,2,3,4])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([ 6, 30, 0, 2])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_expression_2vars")
        # check the dependencies
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        self.assertEqual(var.dependencies(), ['mydataset.var1'], msg="dependencies are incorrect")

    def test_sqrt_constant(self):
        # test an expression that is constant -- should have no dependencies
        expr = "sqrt(25)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset', 
            table_data={"id": array([1,2])}
            )
        # we don't actually use anything in the dataset
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        self.assertTrue(4.99<result and result<5.01, "Error in test_sqrt_constant")
        # check the dependencies
        v = VariableName(expr)
        var = VariableFactory().get_variable(v, dataset)
        self.assertEqual(var.dependencies(), [], msg="dependencies are incorrect")

    def test_numpy_arange_constant(self):
        # test another constant - syntactically this looks like a method call, so it exercises that part of the code
        expr = "numpy.arange(5)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset', 
            table_data={"id": array([1,2])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([0, 1, 2, 3, 4])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_numpy_arange_constant")

    def test_numpy_arange_constant2(self):
        # same as test_numpy_arange_constant, except provide 2 arguments
        expr = "numpy.arange(2,5)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset', 
            table_data={"id": array([1,2])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        should_be = array([2, 3, 4])
        self.assertTrue(ma.allclose(result, should_be, rtol=1e-6), "Error in test_numpy_arange_constant2")

    def test_rand(self):
        # test numpy.random.rand (this exercises 0-argument functions)
        expr = "numpy.random.rand()"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset', 
            table_data={"id": array([1,2])}
            )
        dataset = Dataset(in_storage=storage, in_table_name='dataset', id_name="id", dataset_name="mydataset")
        result = dataset.compute_variables([expr])
        self.assertTrue(result>=0 and result<1, "Error in test_rand")

    def test_condition(self):
        # test using a condition to return an array of True and False values
        expr = "opus_core.test_agent.income>4"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "income":array([1,5,10,3]),
                "id":array([1,3,4,10])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result = dataset.compute_variables([expr])
        should_be = array( [False,True,True,False] )
        self.assertEqual( ma.allclose( result, should_be, rtol=1e-7), True, msg = "Error in test_condition")

    def test_where(self):
        # test using the numpy where function
        expr = "where(opus_core.test_agent.income>4, 100, 200)"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "income":array([1,5,10,3]),
                "id":array([1,3,4,10])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result = dataset.compute_variables([expr])
        should_be = array( [200, 100, 100, 200] )
        self.assertEqual( ma.allclose( result, should_be, rtol=1e-7), True, msg = "Error in test_where")

    def test_true_false(self):
        # make sure True and False can be used in an expression
        expr = "array([True, False, False])"
        # we're not actually using this dataset in the expression, but expressions are computed
        # with respect to a dataset ...
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='test_agents',
            table_data={
                "income":array([10]),
                "id":array([1])
                }
            )
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        result = dataset.compute_variables([expr])
        should_be = array( [True, False, False] )
        self.assertEqual( ma.allclose( result, should_be, rtol=1e-7), True, msg = "Error in test_true_false")

if __name__=='__main__':
    opus_unittest.main()
