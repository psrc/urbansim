# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.simulation_state import SimulationState


class abstract_absolute_SSS_difference_from_DDD(Variable):
    """An abstract class that makes it easy to provide this functionality
    for an arbitrary geography dataset.  Returns the
    difference of variable SSS (current year - baseyear)."""
    
    default_package_order = ["urbansim", "opus_core"]
    
    def __init__(self, variable_name, year, dataset_name=None, package_name=None):
        self._variable_name = variable_name
        self._year = year
        self._package_name = package_name
        self._dataset_name = dataset_name
        Variable.__init__(self)
    
    def dependencies(self):
        if self._package_name and self._dataset_name:
            return ["%s.%s.%s" % (self._package_name, self._dataset_name, self._variable_name)]
        else:
            return []

    def _compute_current_and_lag_values(self, dataset_pool):
        dataset = self.get_dataset()
        current_year = SimulationState().get_current_time()
        lag = current_year - self._year
        
        if not self._dataset_name:
            self._dataset_name = dataset.get_dataset_name()
        
        if self._package_name:
            lag_variable_name = '%s.%s.%s_lag%s' % (
                self._package_name,
                self._dataset_name,
                self._variable_name, 
                lag)
            
            current_values = dataset.compute_variables(self._variable_name) 
            lag_values = dataset.compute_variables(lag_variable_name, 
                                                   dataset_pool=dataset_pool)
        else:
            package_order = dataset_pool.get_package_order() or self.default_package_order
            current_values = dataset.compute_one_variable_with_unknown_package(self._variable_name, 
                                                                               dataset_pool=dataset_pool,
                                                                               package_order=package_order)
            lag_values = dataset.compute_one_variable_with_unknown_package( "%s_lag%s" % (self._variable_name, lag), 
                                                                            dataset_pool=dataset_pool,
                                                                            package_order=package_order)
        return (current_values, lag_values)        
    
    def compute(self, dataset_pool):
        current_values, lag_values = self._compute_current_and_lag_values(dataset_pool)
        
        results = current_values - lag_values
        return results


from opus_core.tests import opus_unittest
import os
import tempfile

from shutil import rmtree
from numpy import array
from numpy import ma

from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.store.dict_storage import dict_storage
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_pool import DatasetPool

class TestFactory(object):
    """If you are using this variable (above), you can test that it works for
    your geography dataset by generating a test class, as shown at the end of
    this file.  This avoids duplicating this code in each derived variable
    module."""
    def __init__(self, package_name='urbansim'):
        self.package_name = package_name
        
    def get_test_case_for_dataset(self, dataset_name, table_name, id_name):
        """Return a test case class customized for this dataset."""
        class __MyTests(opus_unittest.OpusTestCase):
            def setUp(self):
                self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            
            def tearDown(self):
                SimulationState().remove_singleton()
                if os.path.exists(self.temp_dir):
                    rmtree(self.temp_dir)
                    
            def _write_data_to_year(self, data, cache_dir, year):
                """Writes this data to this year of the cache.  Returns dataset.
                """
                # Import in unit test, so that circular dependency is avoided.
                from opus_core.datasets.dataset import Dataset
        
                SimulationState().set_cache_directory(cache_dir)
                
                storage = dict_storage()
                storage.write_table(
                        table_name=self._table_name,
                        table_data=data,
                    )
                
                ds = Dataset(id_name=self._id_name, in_storage=storage, in_table_name=self._table_name)
                ds.load_dataset()
                self._write_dataset_to_cache(ds, cache_dir, year)
                
            def _write_dataset_to_cache(self, dataset, cache_dir, year):
                # save to flt file with this year.
                SimulationState().set_current_time(year)
                year_dir = os.path.join(cache_dir, str(year))
                flt_storage = StorageFactory().get_storage('flt_storage', subdir='store', 
                    storage_location=year_dir)
                dataset.write_dataset(out_storage=flt_storage,
                                      out_table_name=self._table_name)
        
            def test(self):
                cache_dir = os.path.join(self.temp_dir, 'cache')
                data={
                    self._id_name:array([1,2,3]),
                    'population':array([10,20,30]),
                    }
                self._write_data_to_year(data, cache_dir, 2000)
                
                data={
                    self._id_name:array([1,2,3]),
                    'population':array([11,21,31]),
                    }
                self._write_data_to_year(data, cache_dir, 2001)
        
                data={
                    self._id_name:array([1,2,3]),
                    'population':array([12,23,34]),
                    }
                self._write_data_to_year(data, cache_dir, 2002)
        
                attribute_cache = AttributeCache(cache_directory=cache_dir)
                SimulationState(new_instance=True, 
                                base_cache_dir=self.temp_dir)
                SimulationState().set_cache_directory(cache_dir)
                SessionConfiguration(new_instance=True,
                                     in_storage=attribute_cache)
                
                SimulationState().set_current_time(2002)
                dataset_pool_2002 = DatasetPool(package_order=['urbansim'],
                                                storage=attribute_cache)
                dataset = dataset_pool_2002.get_dataset(self._dataset_name)
                variable_name = '%s.%s.absolute_population_difference_from_2000' % (self._package_name, self._dataset_name)
                dataset.compute_variables([variable_name],
                                          dataset_pool=dataset_pool_2002)
                pop_2002 = dataset.get_attribute(variable_name)
                self.assert_(ma.allequal(pop_2002, array([2,3,4])))
                
        
            def test_at_year_2000(self):
                cache_dir = os.path.join(self.temp_dir, 'cache')
                data={
                    self._id_name:array([1,2,3]),
                    'population':array([10,20,30]),
                    }
                self._write_data_to_year(data, cache_dir, 2000)
                
                attribute_cache = AttributeCache(cache_directory=cache_dir)
                SimulationState(new_instance=True, 
                                base_cache_dir=self.temp_dir)
                SimulationState().set_cache_directory(cache_dir)
                SessionConfiguration(new_instance=True,
                                     in_storage=attribute_cache)
                
                SimulationState().set_current_time(2000)
                dataset_pool_2000 = DatasetPool(package_order=['urbansim'],
                                                storage=attribute_cache)
                dataset = dataset_pool_2000.get_dataset(self._dataset_name)
                variable_name = '%s.%s.absolute_population_difference_from_2000' % (self._package_name, self._dataset_name)
                dataset.compute_variables([variable_name],
                                          dataset_pool=dataset_pool_2000)
                pop_2000 = dataset.get_attribute(variable_name)
                self.assert_(ma.allequal(pop_2000, array([0,0,0])))
        
        __MyTests._package_name = self.package_name
        __MyTests._dataset_name = dataset_name
        __MyTests._table_name = table_name
        __MyTests._id_name = id_name
        return __MyTests
            
# An example of how to use this test factory
# Need to assign to the same name as the class defined in TestFactory.
__MyTests = TestFactory().get_test_case_for_dataset('zone', 'zones', 'zone_id')

if __name__ == '__main__':
    opus_unittest.main()
