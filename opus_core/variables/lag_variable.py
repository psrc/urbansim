# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from numpy import array, take, zeros, arange

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.variables.variable import Variable
from opus_core.misc import has_this_method
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.variables.attribute_type import AttributeType
from opus_core.variables.lag_variable_parser import LagVariableParser
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.session_configuration import SessionConfiguration

class LagVariable(Variable):
    """An abstract class containing common code for lag variables.
    See opus_core.VVV_lagLLL for unit tests for this code.
    """

    def __init__(self, package_name, attribute_name, lag_offset, dataset_name, index_name):
        self.package_name = package_name
        self.attribute_name = attribute_name
        self.simulation_state = SimulationState()
        self.attribute_cache = AttributeCache()
        self.lag_offset = lag_offset
        self.dataset_name = dataset_name
        self.index_name = index_name
        self.lag_index_name = "%s_lag%d" % (index_name, lag_offset)
        Variable.__init__(self)

    def lag_time(self):
        return self.simulation_state.get_current_time() - self.lag_offset

    def get_dependencies(self):
        """Return variables and attributes needed to compute this variable.
        This is returned as a list of tuples where the first element is the
        name of the particular dataset and the second element is the variable
        name. It does not work through the dependencies tree.
        """
        dependencies = []
        if has_this_method(self, "dependencies"):
            dependencies = self.dependencies()

            parser = LagVariableParser()
            for i in range(len(dependencies)):
                variable_name = dependencies[i]
                dependencies[i] = parser.add_this_lag_offset_to_this_short_name(variable_name, self.lag_offset)

        return dependencies

    def compute(self, dataset_pool, arguments=None):
        attribute_name = self.attribute_name
        index_name = self.index_name
        dataset = self.get_dataset()

        # Get data from prior year
        lag_time = self.lag_time()

        if self.package_name is None:
            attr_full_name = '.'.join([self.dataset_name, self.attribute_name])
        else:
            attr_full_name = '.'.join([self.package_name, self.dataset_name, self.attribute_name])
        lag_data = self._compute_variable_for_prior_year(dataset, attr_full_name, lag_time, arguments)

        # Also need the index data from prior year.
        # The index must be a primary attribute.
        index_full_name = dataset.create_and_check_qualified_variable_name(index_name).get_expression()
        lag_index = self._compute_variable_for_prior_year(dataset, index_full_name, lag_time, arguments)

        # Get data for current year
        dataset.compute_variables([attr_full_name], dataset_pool, arguments)
        current_data = dataset.get_attribute(attr_full_name)
        dataset.compute_variables([index_full_name], dataset_pool, arguments)
        current_index = dataset.get_attribute(index_full_name)

        # Determine where indices differ in prior and current year, and fix accordingly.
        fixed_lag_index, fixed_lag_data =  self.match_lag_and_current_indices(lag_index, lag_data, current_index, current_data)

        # Save the fixed data as the lag attribute's values.
        self.get_dataset().add_attribute(data=fixed_lag_index,
                             name = self.lag_index_name, metadata = AttributeType.LAG)

        return fixed_lag_data

    def is_lag_variable(self):
        return True

    def _compute_variable_for_prior_year(self, dataset, full_name, time, resources=None):
        """Create a new dataset for this variable, compute the variable, and then return
        the values for this variable."""
        calling_dataset_pool = SessionConfiguration().get_dataset_pool()
        calling_time = SimulationState().get_current_time()
        SimulationState().set_current_time(time)
        try:
            # Get an empty dataset pool with same search paths.
            my_dataset_pool = DatasetPool(
                package_order=calling_dataset_pool.get_package_order(),
                storage=AttributeCache())

            ds = dataset.empty_dataset_like_me(in_storage=AttributeCache())

            # Don't pass any datasets via resources, since they may be from a different time.
            my_resources = Resources(resources)
            for key in my_resources:
                if isinstance(key, Dataset):
                    del my_resources[key]

            ds.compute_variables(full_name, my_dataset_pool, resources=my_resources)
            values = ds.get_attribute(full_name)
            return values
        finally:
            SimulationState().set_current_time(calling_time)

    def _add_remove_datasets(self, lag_index_array, lag_var_array, current_index_array, current_var_array):
        unremoved_items = []
        added_items = []
        lag_index = 0
        lag_size = lag_index_array.size
        current_index = 0
        final_index = 0
        current_size = current_index_array.size
        final_index_array = zeros((current_size,), dtype=lag_index_array.dtype.type)
        final_var_array = zeros((current_size,), dtype=lag_var_array.dtype.type)
        while lag_index < lag_size and current_index < current_size:
            if lag_index_array[lag_index] == current_index_array[current_index]:
                final_index_array[final_index] = lag_index_array[lag_index]
                final_var_array[final_index] = lag_var_array[lag_index]
                lag_index += 1
                current_index += 1
                final_index += 1
            elif lag_index_array[lag_index] < current_index_array[current_index]:
                lag_index += 1
            elif lag_index_array[lag_index] > current_index_array[current_index]:
                final_index_array[final_index] = current_index_array[current_index]
                final_var_array[final_index] = current_var_array[current_index]
                current_index += 1
                final_index += 1

        if lag_index >= lag_size:
            final_index_array.put(indices=arange(current_index,current_size),
                                  values=take(current_index_array, range(current_index,current_size)))
            final_var_array.put(indices=arange(current_index,current_size),
                                values=take(current_var_array, range(current_index,current_size)))

        return (final_index_array, final_var_array)

    def _invert_arg_sort(self, sorted_indices):
        inversed_indices = zeros((sorted_indices.size,), dtype="int32")
        for index in range(sorted_indices.size):
            inversed_indices[sorted_indices[index]] = index
        return inversed_indices

    def match_lag_and_current_indices(self, lag_index_array, lag_var_array, index_array, var_array):
        sorted_indices = index_array.argsort()
        lag_sorted_indices = lag_index_array.argsort()
        sorted_index_array = take(index_array,sorted_indices)
        sorted_var_array = take(var_array,sorted_indices)
        sorted_lag_index_array = take(lag_index_array,lag_sorted_indices)
        sorted_lag_var_array = take(lag_var_array,lag_sorted_indices)
        sorted_lag_index_array, sorted_lag_var_array = self._add_remove_datasets(sorted_lag_index_array,
                                                                                sorted_lag_var_array,
                                                                                sorted_index_array,
                                                                                sorted_var_array)
        inversed_indices = self._invert_arg_sort(sorted_indices)
        lag_index_array = take(sorted_lag_index_array, inversed_indices)
        lag_var_array = take(sorted_lag_var_array, inversed_indices)
        return (lag_index_array, lag_var_array)


from opus_core.tests import opus_unittest

from shutil import rmtree
from tempfile import mkdtemp

from numpy import ma

from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache


class TestLagVariables(opus_unittest.OpusTestCase):
    def setUp(self):
        self._temp_dir = mkdtemp(prefix='opus_tmp_test_lag_variables')
        
    def tearDown(self):
        if os.path.exists(self._temp_dir):
            rmtree(self._temp_dir)
    
    def test_simple_lag_variable(self):
        test_data = {
            1000:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([10,20,30]),
                    },
                },
            1001:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([111,222,333]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self._temp_dir, test_data)
        
        SimulationState().set_current_time(1001)
        
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['opus_core'],
                             in_storage=attribute_cache)
        
        ds = Dataset(in_storage = attribute_cache, 
                     in_table_name = 'tests', 
                     id_name = ['id'], 
                     dataset_name = 'tests')
        
        ds.compute_variables(['opus_core.tests.attr1'])
        self.assert_(ma.allequal(ds.get_attribute('attr1'), array([111,222,333])))
        
        ds.compute_variables(['opus_core.tests.attr1_lag1'])
        self.assert_(ma.allequal(ds.get_attribute('attr1_lag1'), array([10,20,30])))
    
        
    
if __name__ == '__main__':
    opus_unittest.main()
