# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree


from opus_core.resources import Resources
from opus_core.variables.attribute_type import AttributeType
from opus_core.opus_package_info import package
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

from numpy import array

class TestWithAttributeData(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_cache_path = tempfile.mkdtemp(prefix='opus_tmp')    
        self.temp_cache_path2 = tempfile.mkdtemp(prefix='opus_tmp')
      
        self.attribute_vals = array([5,6,7,8])
        self.attribute_vals2 = array([50,60,70,80])
        self.id_vals = array([1,2,3,4])
        
        self.years = [1980, 1981, 1982]
        for year in self.years:
            self.add_attributes(year, self.attribute_vals,
                                self.attribute_vals2)

        self.attribute_vals_diff = array([10,12,14,16])
        self.attribute_vals2_diff = array([100,120,140,160])
        
        self.add_attributes(1983, self.attribute_vals_diff,
                            self.attribute_vals2_diff)     
        
        self.dataset_state = {
            'year':None,
            'dataset_name':None,
            'cache_directory':None
        }

        self.dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            )
        
    def _set_cache_directory(self, cache_directory):
        if cache_directory != SimulationState().get_cache_directory():
            SimulationState().set_cache_directory(cache_directory) 
            SessionConfiguration(
                new_instance = True,
                package_order = self.dataset_pool_configuration.package_order,
                in_storage = AttributeCache()) 
            
    def _get_dataset(self, dataset_name, cache_directory = None, year = None):
        
        if year == None: 
            year = SimulationState().get_current_time()
        if cache_directory == None:
            cache_directory = self.dataset_state['cache_directory']
                
        fetch_dataset = (self.dataset_state['year'] != year or
                         self.dataset_state['cache_directory'] != cache_directory or
                         self.dataset_state['dataset_name'] != dataset_name)

        #only get dataset if its necessary                 
        if fetch_dataset: 
            self._set_cache_directory(cache_directory)
            SimulationState().set_current_time(year)
            SessionConfiguration().get_dataset_pool().remove_all_datasets()
        
            self.dataset_state['year'] = SimulationState().get_current_time()
            self.dataset_state['dataset_name'] = dataset_name
            self.dataset_state['cache_directory'] = cache_directory
                
        return SessionConfiguration().get_dataset_from_pool(dataset_name)
        
    def add_attributes(self, year, attribute_vals, attribute_vals2):
        dir = os.path.join(self.temp_cache_path, repr(year))
        storage = StorageFactory().get_storage('flt_storage', storage_location=dir)
        
        storage.write_table(table_name = 'tests',
            table_data = {'id': self.id_vals,
                'attribute': attribute_vals,
                'attribute2': attribute_vals2,}
        )

        copytree(dir, os.path.join(self.temp_cache_path2, repr(year)))
                
    def tearDown(self):
        rmtree(self.temp_cache_path)
        rmtree(self.temp_cache_path2)