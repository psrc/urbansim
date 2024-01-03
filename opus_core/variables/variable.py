# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import ma
from numpy import where, array
from opus_core.variables.variable_factory import VariableFactory
from opus_core.misc import has_this_method, DebugPrinter
from opus_core.resources import Resources
from opus_core.logger import logger
from opus_core.variables.variable_name import VariableName
from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_box import AttributeBox
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory

from numpy import longlong, int32


class Variable(object):
    """Abstract base class for variables. Each variable implementation must be 
    a subclass of this class, placed in a module that has the same name 
    as the variable class. Each variable class is expected to contain a method "compute" 
    that takes one argument "arguments". It is of type Resources and can contain 
    anything that the compute method might need. 
    The 'compute' method  returns a result of the computation which should be 
    an array of size self.get_dataset().size().
    
    Each variable class can contain a method "dependencies" which returns a list 
    of attributes/variables that this class is dependent on.  The dependencies list 
    is a list of fully (or dataset) qualified variable names, one for each 
    dependent variable. All dependent datasets must be included in 'arguments'.    
    
    Each variable may have a pre- and post-check that will perform checks on the
    variable's inputs and the variable's results.  This allows each variable's
    implementation to specify a contract about what it does.  
    
    The 'check_variables' entry of the 'arguments' defines what variables to check
    (see method 'should_check'). If a variable is required to be checked, the 
    'S' method for that variable is called before the variable's 'compute' 
    method, and the 'post_check' method for that variable is called after the 
    variable's 'compute' method.  Both 'pre_check' and 'post_check' take 2
    arguments: values (the results from the 'compute' method), and 'arguments'.
    
    In case of using 'compute_with_dependencies' the datasets for which variables 
    are computed, are expected to have a method 'compute_variables' that 
    takes at least three arguments: name of the variable, package name and 
    an object of class Resources. This dataset method should
    use the Variable method 'compute_with_dependencies' in order to work recursively 
    through dependency trees (see compute_variables and _compute_one_variable of 
    opus_core.Dataset).
    
    The return type of this variable is defined by it's _return_type property, which
    may have one of the following numpy types: "bool8", "int8", "uint8", "int16", 
    "uint16", "int32", "uint32", "int64", "uint64", "float32", "float64", "complex64",
    "complex128", "longlong".
    """
    _return_type = None
    
    def __new__(cls, *args, **kwargs):
        """Setup to automatically log the running time of the compute method."""
        
        an_instance = object.__new__(cls)
        compute_method = an_instance.compute_with_dependencies

        def logged_method (*req_args, **opt_args):
            with logger.block(name=an_instance.name(), verbose=False):
                results = compute_method(*req_args, **opt_args)
                an_instance._do_flush_dependent_variables_if_required()

            return results       
            
        an_instance.compute_with_dependencies = logged_method
        return an_instance        
    
    def __init__(self):
        self.dependencies_list = None
        self.dataset = None
        self.number_of_compute_runs = 0
        try:
            self.debug = SessionConfiguration().get('debuglevel', 0)
        except:
            self.debug = 0
        if isinstance(self.debug, int):
            self.debug = DebugPrinter(self.debug)
            
    def name(self):
        return self.__module__
            
    def _do_flush_dependent_variables_if_required(self):
        try:
            if not SimulationState().get_flush_datasets():
                return
        except:
            return
        from opus_core.datasets.interaction_dataset import InteractionDataset
        dataset = self.get_dataset()
        dependencies = self.get_current_dependencies()
        my_dataset_name = dataset.get_dataset_name()
        for iattr in range(len(dependencies)): # iterate over dependent variables
            dep_item = dependencies[iattr][0]
            if isinstance(dep_item, str):
                depvar_name = VariableName(dep_item)
            else:
                depvar_name = dep_item.get_variable_name() # dep_item should be an instance of AttributeBox
            dataset_name = depvar_name.get_dataset_name()
            if dataset_name == my_dataset_name:
                ds = dataset
            else:
                ds = SessionConfiguration().get_dataset_from_pool(dataset_name)
                #ds = dataset_pool.get_dataset('dataset_name')
            if not isinstance(ds, InteractionDataset):
                short_name = depvar_name.get_alias()
                if short_name not in ds.get_id_name():   
                    ds.flush_attribute(depvar_name)
        
    def compute(self, dataset_pool):
        """Returns the result of this variable.  Private use only."""
        raise NotImplementedError("compute() method not implemented for this variable.")
    
    def is_lag_variable(self):
        """Not a lag variable unless this function has been overridden to return True"""
        return False

    def _compute_and_check(self, dataset_pool):
        if has_this_method(self, "pre_check"):
            self.debug.print_debug("Running pre_check() for " + self.__class__.__module__,4)
            self.pre_check(dataset_pool)
        else:
            self.debug.print_debug("No pre_check() defined for " + self.__class__.__module__,4)
        values = self.compute(dataset_pool)
        if has_this_method(self, "post_check"):
            self.debug.print_debug("Running post_check() for " + self.__class__.__module__,4)
            self.post_check(values, dataset_pool)
        else:
            self.debug.print_debug("No post_check() defined for " + self.__class__.__module__,4)
        return values
        
    def compute_with_dependencies(self, dataset_pool, arguments={}):
        self._solve_dependencies(dataset_pool)
        if self.should_check(arguments):
            self.debug.print_debug("Computing and checking " + self.__class__.__module__,3)
            values = self._compute_and_check(dataset_pool)
        else:
            values = self.compute(dataset_pool)
        self.number_of_compute_runs += 1
        if self._return_type:
            return self._cast_values(values, arguments)
        return values

    if longlong == int32:
        __long_size = 2**31 - 1
    else:
        __long_size = 2**63 - 1
        
    _max_storable_value = {"bool8":1,
                            "int8":2**7 - 1,
                            "uint8":2**8 - 1,
                            "int16":2**15 - 1,
                            "uint16":2**16 - 1,
                            "int32":2**31 - 1,
                            "uint32":2**32 - 1,
                            "int64":2**63 - 1,
                            "uint64":2**64 - 1,
                            "float32":3.40282346638528860e+38,
                            "float64":1.79769313486231570e+308,
                            "complex64":3.40282346638528860e+38,
                            "complex128":1.79769313486231570e+308,
                            "longlong":__long_size,
                            }
        
    def _cast_values(self, values, arguments):
        """Change the return values to be of type self._return_type.
        If "should_check" is defined, first check for 
        values that are too large for the destination type or
        integer wrap-around."""
        type = values.dtype.str
        if self._return_type == type:
            return values
        if self.should_check(arguments):
            max_value = ma.maximum(values)
            if max_value > self._max_storable_value[self._return_type]:
                max_value_str = str(max_value)
                logger.log_error("Variable '%s' is being cast to type '%s', but contains a value (%s) too large to fit into that type."
                                 % (self.name(), self._return_type, max_value_str))
        return values.astype(self._return_type)

    def _solve_dependencies(self, dataset_pool):
        dataset = self.get_dataset()
        my_dataset_name = dataset.get_dataset_name()
        dependencies_list = self.get_current_dependencies()
        for i in range(len(dependencies_list)): # compute dependent variables
            dep_item = dependencies_list[i][0]
            if isinstance(dep_item, str):
                depvar_name = VariableName(dep_item)
            else:
                depvar_name = dep_item.get_variable_name() # dep_item should be an instance of AttributeBox
            dataset_name = depvar_name.get_dataset_name()
            version = dependencies_list[i][1]
            if dataset_name == my_dataset_name:
                ds = dataset
            else:
                ds = dataset_pool.get_dataset(dataset_name)
            (new_versions, value) = ds.compute_variables_return_versions_and_final_value([(depvar_name, version)], dataset_pool)
            self.dependencies_list[i] = (ds._get_attribute_box(depvar_name), new_versions[0])

        
    def get_all_dependencies(self):
        """Return all variables and attributes needed to compute this variable.  
        This is returned as a list of tuples where the first element is either AttributeBox or 
        VariableName of the dependent variable and the second element is the version for 
        which this variable was computed.
        """ 
        def create_fake_dataset(dataset_name):
            storage = StorageFactory().get_storage('dict_storage')
            
            storage.write_table(
                table_name='fake_dataset',
                table_data={
                    'id':array([], dtype='int32')
                    }
                )
            
            dataset = Dataset(in_storage=storage, in_table_name='fake_dataset', dataset_name=dataset_name, id_name="id")
            return dataset
        
        result_others = []
        dependencies_list = self.get_current_dependencies()
        for i in range(len(dependencies_list)):
            dep_item = dependencies_list[i][0]
            version = dependencies_list[i][1]
            isprimary = 0
            if isinstance(dep_item, str):
                depvar_name = VariableName(dep_item)
                dataset_name = depvar_name.get_dataset_name()
                var = VariableFactory().get_variable(depvar_name, create_fake_dataset(dataset_name), 
                                                               quiet=True)
                result_others = result_others + [(depvar_name, version)]                                              
            else: # dep_item should be an instance of AttributeBox
                var = dep_item.get_variable_instance()           
                result_others = result_others + [(dep_item, version)]
                isprimary = dep_item.is_primary()
                
            if (var != None) and (not isprimary):
                res = var.get_all_dependencies()
                result_others = result_others + res
        return result_others
        
    def get_dependencies(self):
        """Return variables and attributes needed to compute this variable.  
        This is returned as a list of tuples where the first element is the 
        name of the particular dataset and the second element is the variable 
        name. It does not work through the dependencies tree.
        """ 
        if has_this_method(self, "dependencies"):
            return self.dependencies()
        return []
    
    def add_dependencies(self, dep_list=[]):
        """Can be used within 'compute' method to add dependencies. It is performed only 
        when the compute method runs for the first time.
        dep_list can be either a list of character strings or a list of AttributeBoxes."""
        if self.number_of_compute_runs == 0:
            if isinstance(dep_list, str):
                dep_list = [dep_list]
            self.dependencies_list = self.dependencies_list + [(x, 0) for x in dep_list]
            
    def add_and_solve_dependencies(self, dep_list=[], dataset_pool=None):
        """Calls 'add_dependencies' and if it is run for the first time, it also calls the 
        '_solve_dependencies' method."""
        self.add_dependencies(dep_list)
        if self.number_of_compute_runs == 0:
            self._solve_dependencies(dataset_pool)
        
    def get_current_dependencies(self):
        if self.dependencies_list is None:
            self.dependencies_list = [(x, 0) for x in self.get_dependencies()]
        return self.dependencies_list
        
    def do_check(self, condition_str, values):
        def condition(x):
            return eval(condition_str)

        # This is a bit ugly, but the upgrade from Python 2.3.5 to
        # Python 2.4 broke backward compatability in regard to map and
        # numpy's rank-0 arrays. This attempts to detect a rank-0
        # array and convert it into something usable.
        try:
            try: len(values)
            except TypeError: values = array([values[()]])
        except: pass

        count = where(array([not(condition(x)) for x in values]) > 0)[0].size
        
        if (count > 0):
            logger.log_warning("Variable %s fails %d times on check %s" % 
                               (self.__class__.__module__, count, condition_str))
                
    def should_check(self, arguments=None):
        """Return True if this variable should be checked, otherwise False. The information of what
        variables to check is provided in the 'arguments' entry "check_variables". 
        If "check_variables" is missing or is None or is an empty list, do no checks. 
        If "check_variables" is '*', check all variables.
        If "check_variables" is a list containing this variable's name, check this variable. 
        """
        if not isinstance(arguments, Resources):
            return False
        check_variables = arguments.get("check_variables", None)
        if check_variables == None:
            return False
        if (check_variables == '*') or \
           (isinstance(check_variables, list) and (len(check_variables) > 0) and 
            (self.__class__.__name__ in check_variables)):
            return True
        return False
     
    def are_dependent_variables_up_to_date(self, version):
        result = []  
        all_dependencies_list = self.get_all_dependencies()
        for variable, version  in all_dependencies_list:
            if isinstance(variable, AttributeBox):
                result.append(variable.is_version(version))
            else: # of type VariableName (means variable wasn't used yet)
                result.append(False)
        return result
        
    def get_highest_version_of_dependencies(self):
        dependencies_list = self.get_current_dependencies()
        if len(dependencies_list) <= 0:
            return 0
        versions = array([x[1] for x in dependencies_list])
        return versions.max()
    
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    def get_dataset(self):
        return self.dataset

    def safely_divide_two_arrays(self, numerator, denominator, value_for_divide_by_zero=0.0):
        """Returns the result of numerator/denominator with the value_for_divide_by_zero 
        wherever denominator == 0.
        """
        return ma.filled(numerator / ma.masked_where(denominator == 0, denominator),
                      value_for_divide_by_zero)
    
    def safely_divide_two_attributes(self, numerator_name, denominator_name, value_for_divide_by_zero=0.0):
        """Returns the result of dividing the numerator_name attribute of this variable
        by the denominator_name attribute of this variable; return the value_for_divide_by_zero 
        wherever denominator == 0.
        """
        numerator = self.get_dataset().get_attribute(numerator_name)
        denominator = self.get_dataset().get_attribute(denominator_name)
        return self.safely_divide_two_arrays(numerator, denominator, value_for_divide_by_zero)
    
#Functions    
def ln_bounded(v):
    return ma.filled(ma.log(ma.masked_where(v<1,v)),0.0)
    
def ln(v):
    return ma.filled(ma.log(ma.masked_where(v==0,v)),0.0)
    
def ln_shifted(v, shift=1):
    """'v' is shifted by 'shift' before doing log."""
    return ma.log(v + shift)
    
def ln_shifted_auto(v):
    """If 'v' has values <= 0, it is shifted in a way that min(v)=1 before doing log. 
    Otherwise the log is done on the original 'v'."""
    vmin = ma.minimum(v)
    if vmin <= 0:
        values = v - vmin + 1
    else:
        values = v
    return ma.log(values)

def get_variable_dependencies(name, quiet=False):
    """Return a tuple where the first element is a list of variables of the given 'dataset' that the 
    variable given by 'name' is directly as well as indirectly dependent on.
    The second elemet is a list of dependent variables that belong to other datasets. It consists of tuples where the 
    first element is the fully qualified name and the second element is the version. """
    dep = VariableFactory().get_variable(name, None, quiet=quiet).get_all_dependencies()
    return dep
    
def get_dependency_datasets(variables, dataset, quiet=False):
    """Return a list of datasets that are required by the compute methods of the given variables."""    
    if not isinstance(variables, list):
        variables = [variables]
    datasetslist = []
    for var in variables:
        dep = get_variable_dependencies(var, quiet)
        for name, version in dep:
            object = name.get_dataset_name()
            if not (object in datasetslist) and (object != dataset):
                datasetslist = datasetslist + [object]
    return datasetslist

from opus_core.tests import opus_unittest
import platform
from numpy import int8, int64

class VariableTests(opus_unittest.OpusTestCase):
    def test_safely_divide_two_arrays(self):
        result = Variable().safely_divide_two_arrays(array([10,20,30,0]).astype(int8), array([2,0,2,0]).astype(int8))
        self.assertTrue(ma.allclose(array([5,0,15,0]), result))
        # Types are done correctly
        self.assertEqual(result.dtype.name, "float64")
        
        result = Variable().safely_divide_two_arrays(array([1,2,3,0]), array([2.,0.,2.,0.]))
        self.assertTrue(ma.allclose(array([.5, 0, 1.5, 0]), result))
        
        result = Variable().safely_divide_two_arrays(array([1,2,3,0]), array([2.,0.,2.,0.]), value_for_divide_by_zero=-1.)
        self.assertTrue(ma.allclose(array([.5, -1., 1.5, -1.]), result))
        
    def test_safely_divide_two_attributes(self):
        from opus_core.datasets.dataset_pool import DatasetPool
        
        storage = StorageFactory().get_storage('dict_storage')        
        storage.write_table(
            table_name='tests',
            table_data={
                'id': array([1,2,3,4]),
                'numerator': array([1,2,3,0]),
                'denominator': array([2.,0.,2.,0.]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['opus_core'],
                                   storage=storage)
        test = dataset_pool.get_dataset('test')
        variable = Variable()
        variable.set_dataset(test)

        result = variable.safely_divide_two_attributes('opus_core.test.numerator',
                                                       'opus_core.test.denominator')
        self.assertTrue(ma.allclose(array([.5, 0, 1.5, 0]), result))
        
        result = variable.safely_divide_two_attributes('opus_core.test.numerator',
                                                       'opus_core.test.denominator', 
                                                        value_for_divide_by_zero=-1.0)
        self.assertTrue(ma.allclose(array([.5, -1., 1.5, -1.]), result))
    
    def test_compute_unloads_from_memory(self):
        
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                'a_dependent_variable':array([1,5,10]),
                'id':array([1,3,4])
                }
            )
        
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name='id', dataset_name='tests')
        
        SimulationState().set_flush_datasets(True)
        dataset.get_attribute("a_dependent_variable")
        self.assertTrue("a_dependent_variable" in dataset.get_attributes_in_memory())
        dataset.compute_variables("opus_core.tests.a_test_variable")
        self.assertTrue("a_dependent_variable" not in dataset.get_attributes_in_memory())
        self.assertTrue("a_test_variable" in dataset.get_attributes_in_memory())
        SimulationState().remove_singleton(delete_cache=True)

    def test_compute_does_not_unload_from_memory(self):        
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,5,1000]),
                "id":array([1,3,4])
                }
            )
        
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")
        
        values = dataset.get_attribute("a_dependent_variable")
        self.assertTrue("a_dependent_variable" in dataset.get_attributes_in_memory())
        dataset.compute_variables("opus_core.tests.a_test_variable")
        self.assertTrue("a_dependent_variable" in dataset.get_attributes_in_memory())
        self.assertTrue("a_test_variable" in dataset.get_attributes_in_memory())
        # The type of values will be int32 on a 32-bit machine, and int64 on a 64 bit machine
        if platform.architecture()[0]=='64bit':
            self.assertEqual(values.dtype.type, int64)
        else:
            self.assertEqual(values.dtype.type, int32)
        
    def test_casting(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='tests',
            table_data={
                "a_dependent_variable":array([1,5,1000]),
                "id":array([1,3,4])
                }
            )
        
        dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name="tests")

        logger.enable_hidden_error_and_warning_words()
        # Next line should cause a 'WARNING' to be logged.
        dataset.compute_variables("opus_core.tests.a_test_variable",
                                  resources=Resources({"check_variables":"*"}))
        logger.disable_hidden_error_and_warning_words()
        
        values = dataset.get_attribute("a_test_variable")
        self.assertEqual(values.dtype.type, int8)
        
        
if __name__ == "__main__":
    opus_unittest.main()        
