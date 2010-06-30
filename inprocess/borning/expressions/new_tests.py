# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.variables.variable_factory import VariableFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, ma

class Tests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        VariableName.use_inprocess_compiler = True
        
    def tearDown(self):
        VariableName.use_inprocess_compiler = False


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
        self.assertEqual(ma.allclose(result, should_be, rtol=1e-5), True, msg="error in test_unary_functions_fully_qualified_name")
        # check that the access methods for the variable all return the correct values
        name = VariableName(expr)
        autogen = name.get_autogen_class()
        self.assert_(issubclass(autogen, Variable), msg="autogen'd class isn't a Variable")
        self.assertEqual(name.get_package_name(), None, msg="bad value for package")
        self.assertEqual(name.get_dataset_name(), 'tests', msg="bad value for dataset")
        self.assertEqual(name.get_short_name(), autogen.__name__, msg="bad value for shortname")
        self.assertEqual(name.get_alias(), autogen.__name__, msg="bad value for alias")
        # make an instance of the class and check the dependencies (since the dependent variables
        # all have fully-qualified names we don't need to associate a dataset with the variable
        # for this test)
        self.assertEqual(autogen().dependencies(), ['opus_core.tests.a_test_variable'], 
                         msg="dependencies are incorrect")
 
if __name__=='__main__':
    opus_unittest.main()
