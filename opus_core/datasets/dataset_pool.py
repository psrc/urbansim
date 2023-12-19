# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from copy import deepcopy

from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.misc import create_import_for_camel_case_class


class DatasetPool(object):
    """
    Maintains a 'pool' of datasets.  
    """
    
    def __init__(self, package_order=[], package_order_exceptions={}, storage=None, datasets_dict={}):
        """Keeps a set of datasets by name & knows where to look for dataset modules."""
        self._package_order = package_order
        if len(package_order_exceptions)>0:
            raise ValueError("parameter package_order_exceptions is deprecated and shouldn't be used -- tried to pass in a non-empty dictionary to package_order_exceptions")        
        self._storage = storage
        self._loaded_datasets = {}
        self.add_datasets_if_not_included(datasets_dict)
        
    def get_copy(self):
        """Return a copy of this dataset pool, without copying the datasets."""
        pool = DatasetPool(package_order=self._package_order, storage=self._storage)
        for dataset_name, dataset in self._loaded_datasets.items():
            pool._add_dataset(dataset_name, dataset)
        return pool
        
    def get_package_order(self):
        return self._package_order
    
    def get_storage(self):
        return self._storage
    
    def get_dataset(self, dataset_name, dataset_arguments={}):
        """Return object for this dataset.
        
        If it is in the pool already, return that.
        Otherwise, create a new one and put it in the pool before returning it.
        """
        if dataset_name not in self._loaded_datasets: # Lazy load
            self._load_new_dataset(dataset_name, dataset_arguments)
            
        return self._loaded_datasets[dataset_name]
    
    def _add_dataset(self, dataset_name, dataset):
        """If this dataset is not already in pool, add it.  Else, fail."""
        if dataset_name in self._loaded_datasets:
            raise Exception("Dataset '%s' already in dataset pool; cannot add it again." % 
                            dataset_name) 
        self._loaded_datasets[dataset_name] = dataset
        
    def add_datasets_if_not_included(self, datasets_dict):
        """Add datasets from the dictionary 'datasets_dict' (that are not already in the pool) into the pool."""
        for name, dataset in datasets_dict.items():
            if name not in self._loaded_datasets:
                self._add_dataset(name, dataset)
                
    def replace_dataset(self, dataset_name, dataset):
        """Add dataset into pool. If a dataset of that name already exists in the pool, it is replaced by this one.
        """
        if dataset_name in self._loaded_datasets:
            self._remove_dataset(dataset_name)
        self._add_dataset(dataset_name, dataset)
        
    def has_dataset(self, dataset_name):
        return dataset_name in self._loaded_datasets
    
    def datasets_in_pool(self):
        """Returns set of datasets in this pool."""
        return self._loaded_datasets
    
    def remove_all_datasets(self):
        """Empty this pool."""
        for dataset_name in list(self._loaded_datasets.keys()):
            self._remove_dataset(dataset_name)
            
    def flush_loaded_datasets(self):
        for dataset in list(self.datasets_in_pool().values()):
            dataset.flush_dataset()
        
    def _remove_dataset(self, dataset_name):
        """Remove this dataset from this pool."""
        del self._loaded_datasets[dataset_name]
    
    def _load_new_dataset(self, dataset_name, dataset_arguments):
        """Create a new dataset object and put it in the pool.
        Use first class found in the 'datasets' directory
        for the packages in package_order."""
        
        arguments = deepcopy(dataset_arguments)
        # Augment arguments as needed.
        if '_x_' in dataset_name:
            dataset_names = dataset_name.split('_x_')
            for i in range(len(dataset_names)):
                key = 'dataset%s' % (i+1)
                arguments[key] = self.get_dataset(dataset_names[i])
        else:
            arguments['in_storage'] = self._storage
        if len(dataset_arguments.get('id_name', ['dummy'])) == 0:
            dataset = DatasetFactory().search_for_dataset_with_hidden_id(dataset_name, self._package_order, subdir='datasets', arguments=arguments)
        else:
            dataset = DatasetFactory().search_for_dataset(dataset_name, self._package_order, subdir='datasets', arguments=arguments)        
        self._add_dataset(dataset_name, dataset)
    
    def _create_dataset(self, module_path, dataset_arguments):
        import_stmt = create_import_for_camel_case_class(module_path, 'ImportedDataset')
        exec(import_stmt, globals())
        dataset = ImportedDataset(in_storage=self._storage, **dataset_arguments)

        return dataset

    def info_itemsize_in_memory(self):
        """Prints out itemsize of attributes in memory of loaded datasets."""
        print("In-memory itemsize of datasets:")
        for name, dataset in self._loaded_datasets.items():
            try:
                print("%s: %s" % (name, dataset.itemsize_in_memory()))
            except:
                print("unknown size of %s" % name) 

    ### some helper methods and shorthands
    def __getitem__(self, dataset_name):
        """ enables dataset_pool[dataset_name]
        """
        return self.get_dataset(dataset_name)

import os
from opus_core.tests import opus_unittest
import tempfile
import sys

from shutil import rmtree, copyfile

from opus_core.opus_package_info import package
from opus_core.opus_package import create_package
from opus_core.misc import replace_string_in_files


class TestDatasetPool(opus_unittest.OpusTestCase):
    def get_dataset_pool(self, package_order):
        opus_core_path = package().get_opus_core_path()
        cache_dir = os.path.join(opus_core_path, 'data', 'test_cache', '1980')
        
        # These imports are here to prevent cycles in the imports.
        from opus_core.resources import Resources
        from opus_core.store.flt_storage import flt_storage

        storage = flt_storage(Resources({'storage_location':cache_dir}))
        return DatasetPool(package_order, storage=storage)
    
    def test_get_copy(self):
        pool = self.get_dataset_pool(package_order=['a','b'])
        pool_2 = pool.get_copy()
        self.assertEqual(pool._package_order, pool_2._package_order)
    
    def test_no_paths(self):
        dataset_pool = DatasetPool()
        self.assertRaises(Exception, dataset_pool.get_dataset, 'gridcell')
        
    def test_change_package_order(self):
        """Does it find the correct dataset when there are multiple packages?"""
        opus_path = package().get_package_parent_path()
        old_sys_path = sys.path
        try:
            temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            
            # Create a temporary Opus package with a variant of the alldata dataset.
            temp_package_name = '__test_change_package_order__'
            create_package(package_parent_dir=temp_dir, package_name=temp_package_name)
            
            # Make sure Python can find this temporary package.
            sys.path = [temp_dir] + sys.path
            
            # Add the datasets directory.
            temp_package_path = os.path.join(temp_dir, temp_package_name)
            os.mkdir(os.path.join(temp_package_path, 'datasets'))
            opus_core_dataset_path = os.path.join(opus_path, 'opus_core', 'datasets')
            temp_package_dataset_path = os.path.join(temp_package_path, 'datasets')
            
            # Create a 'newdata' dataset.
            copyfile(os.path.join(opus_core_dataset_path, '__init__.py'),
                     os.path.join(temp_package_dataset_path, '__init__.py'))
            copyfile(os.path.join(opus_core_dataset_path, 'alldata_dataset.py'),
                     os.path.join(temp_package_dataset_path, 'newdata_dataset.py'))
            replace_string_in_files(temp_package_dataset_path, 'alldata', 'newdata')
            replace_string_in_files(temp_package_dataset_path, 'Alldata', 'Newdata')
            
            package_order = [temp_package_name, 'opus_core']
            dataset_pool = self.get_dataset_pool(package_order)
            temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            
            # Create a temporary Opus package with a variant of the alldata dataset.
            temp_package_name = '__test_change_package_order__'
            create_package(package_parent_dir=temp_dir, package_name=temp_package_name)
            
            # Make sure Python can find this temporary package.
            sys.path = [temp_dir] + sys.path
            
            # Add the datasets directory.
            temp_package_path = os.path.join(temp_dir, temp_package_name)
            os.mkdir(os.path.join(temp_package_path, 'datasets'))
            opus_core_dataset_path = os.path.join(opus_path, 'opus_core', 'datasets')
            temp_package_dataset_path = os.path.join(temp_package_path, 'datasets')
            
            # Create a 'newdata' dataset.
            copyfile(os.path.join(opus_core_dataset_path, '__init__.py'),
                     os.path.join(temp_package_dataset_path, '__init__.py'))
            copyfile(os.path.join(opus_core_dataset_path, 'alldata_dataset.py'),
                     os.path.join(temp_package_dataset_path, 'newdata_dataset.py'))
            replace_string_in_files(temp_package_dataset_path, 'alldata', 'newdata')
            replace_string_in_files(temp_package_dataset_path, 'Alldata', 'Newdata')
            
            package_order = [temp_package_name, 'opus_core']
            dataset_pool = self.get_dataset_pool(package_order)
            
            # Make sure it works as expected for 'alldata'.
            self.do_test_get_dataset(dataset_pool)
            
            # Try it for 'newdata'.
            newdata = dataset_pool.get_dataset('newdata')
            self.assertTrue(newdata is not None, "Could not get 'newdata' dataset")
            
        finally:
            sys.path = old_sys_path
            rmtree(temp_dir)
        
    def test_cannot_get_dataset_when_no_packages_in_path(self):
        package_order = []
        dataset_pool = self.get_dataset_pool(package_order)
        self.assertRaises(Exception, dataset_pool.get_dataset, 'alldata')
        
    def test_get_dataset(self):
        package_order = ['opus_core']
        dataset_pool = self.get_dataset_pool(package_order)
        self.do_test_get_dataset(dataset_pool)
        
    def do_test_get_dataset(self, dataset_pool):
        test_dataset_name = 'alldata'
        dataset1 = dataset_pool.get_dataset(test_dataset_name)
        
        self.assertTrue(dataset1 is not None, "Could not get 'alldata' dataset")
        
        try:
            dataset1.get_primary_attribute_names()
        except:
            self.fail('Expected dataset from get_dataset! Received a %s '
                'instead.' % type(dataset1))
        
        dataset2 = dataset_pool.get_dataset(test_dataset_name)
        
        self.assertTrue(dataset2 is dataset1, 'Different datasets received from '
            'calls of get_dataset on the same dataset name! Expected %s; '
            'received %s.' % (dataset1, dataset2))
        
if __name__ == '__main__':
    opus_unittest.main()
