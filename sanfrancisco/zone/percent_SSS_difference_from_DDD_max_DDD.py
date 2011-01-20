# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import isnan
from urbansim.abstract_variables.abstract_percent_SSS_difference_from_DDD_max_DDD \
    import abstract_percent_SSS_difference_from_DDD_max_DDD

class percent_SSS_difference_from_DDD_max_DDD(abstract_percent_SSS_difference_from_DDD_max_DDD):
    """percent difference of variable SSS (current year - baseyear)"""
    ## no code needed, but we do need the class present in the dataset directory
    pass


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
from opus_core.simulation_state import SimulationState


class TestFactory(object):
    """If you are using this variable (above), you can test that it works for
    your geography dataset by generating a test class, as shown at the end of
    this file.  This avoids duplicating this code in each derived variable
    module."""    
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
                '''Test dataset with following situations:
                [normal, normal, normal, divide-by-zero, cap-very-large-values]'''
                cache_dir = os.path.join(self.temp_dir, 'cache')
                data={
                    self._id_name:array([1,2,3,4,5]),
                    'population':array([10,20,30,0,1]),
                    }
                self._write_data_to_year(data, cache_dir, 2000)
                
                data={
                    self._id_name:array([1,2,3,4,5]),
                    'population':array([11,21,31,0,1]),
                    }
                self._write_data_to_year(data, cache_dir, 2001)
        
                data={
                    self._id_name:array([1,2,3,4,5]),
                    'population':array([20,30,30,40,10000]),
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
                variable_name = 'sanfrancisco.%s.percent_population_difference_from_2000_max_9999' % self._dataset_name
                dataset.compute_variables([variable_name],
                                          dataset_pool=dataset_pool_2002)
                pop_2002 = dataset.get_attribute(variable_name)
                print pop_2002
                self.assert_(ma.allclose(pop_2002, array([100,50,0,9999,9999])))
                
        
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
                variable_name = 'sanfrancisco.%s.percent_population_difference_from_2000_max_9999' % self._dataset_name
                dataset.compute_variables([variable_name],
                                          dataset_pool=dataset_pool_2000)
                pop_2000 = dataset.get_attribute(variable_name)
                self.assert_(ma.allequal(pop_2000, array([0,0,0])))
                
        __MyTests._dataset_name = dataset_name
        __MyTests._table_name = table_name
        __MyTests._id_name = id_name
        return __MyTests
            
# An example of how to use this test factory
# Need to assign to the same name as the class defined in TestFactory.
__MyTests = TestFactory().get_test_case_for_dataset('zone', 'zones', 'zone_id')
        

if __name__ == '__main__':
    opus_unittest.main()