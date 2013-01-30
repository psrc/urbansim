# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import h5py
import os
from numpy import array, dtype
from opus_core.misc import unique
from opus_core.logger import logger
from opus_core.store.hdf5_storage import hdf5_storage
from opus_core.store.storage import Storage
import re

class hdf5g_storage(hdf5_storage):
    """Like hdf5_storage, but it supports a grouped file structure where every table is a group and 
       its columns are stored on the second level of that group. 
       An object of this class is associated with a file name (passed to the init method with its full path), 
       since all datasets are stored in one file.
    """
      
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        """
        It is assumed that the table is stored as a group called table_name.
        """
        full_file_name = self._get_file_path()      
        f = h5py.File(full_file_name, 'r')
        if table_name not in f.keys():
            raise KeyError, 'Table %s not found in %s.' % (table_name, full_file_name)
        result = self._load_columns(f[table_name], column_names, lowercase) 
        f.close()
        return result

    def load_meta(self, table_name, column_name=None):
        file_name = self._get_file_path()   
        f = h5py.File(file_name, 'r')
        if table_name not in f.keys():
            raise KeyError, 'Table %s not found in %s.' % (table_name, file_name)
        meta = self._get_meta(f[table_name], column_name)
        f.close()
        return meta
    
    def write_table(self, table_name, table_data, mode = Storage.APPEND, table_meta={}, column_meta={}, driver=None, **kwargs):
        """
        table_data is a dictionary where keys are the column names and values 
            are value arrays of the corresponding columns.
        Each table is stored as a group called table_name. Each column is stored as an hdf5 dataset.
        By default, data are appended to an existing file. Set the argument mode to 'o' or 'w' to overwrite the file.
        Meta data for the whole table and/or for the columns can be passed as dictionaries table_meta and column_meta, respectively.
        Keys in column_meta have to correspond to column names. The values are again dictionaries with the meta data 
        which can be either strings, scalar or arrays (this is hdf5 restriction).    
        Argument driver is passed to the h5py.File. Other arguments can be passed to the h5py create_dataset function, 
        e.g. compression. 
        """
        
        file_name = self.get_storage_location()  
        dir = os.path.split(file_name)[0]     
        if len(dir) > 0 and not os.path.exists(dir):
            logger.log_status("%s doesn't exist and is created" % dir)
            os.makedirs(dir)
        unused_column_size, column_names = self._get_column_size_and_names(table_data)
        h5mode = self._get_hdf5mode(mode)
        f = h5py.File(file_name, h5mode, driver=driver)
        if h5mode == 'a' and table_name in f.keys():
            raise StandardError, 'File %s already contains table %s. Use mode="w" to overwrite the table.' % (file_name, table_name)
        group = f.create_group(table_name)
        self._write_columns(group, column_names, table_data, table_meta, column_meta, **kwargs)
        f.close()


    def get_column_names(self, table_name, lowercase=True):
        full_file_name = self._get_file_path()      
        f = h5py.File(full_file_name, 'r')
        if table_name not in f.keys():
            raise KeyError, 'Table %s not found in %s.' % (table_name, full_file_name)
        result = f[table_name].keys()
        if lowercase:
            result = [file.lower() for file in result]
        f.close()
        return result

    def get_table_names(self):
        """
        Returns a list of the names of the tables in storage. 
        """    
        f = h5py.File(self._get_file_path() , 'r')
        result = f.keys()
        f.close()
        return result
    
    def has_table(self, table_name):
        f = h5py.File(self._get_file_path() , 'r')
        res = table_name in f.keys()
        f.close()
        return res
    
from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface
from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

class TestHDF5Storage(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_hdf5g_storage')
        self.temp_file = os.path.join(self.temp_dir, 'xxx.hdf5')         
        self.storage = hdf5g_storage(storage_location=self.temp_file)
        
    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test_hdf5_storage_with_groups(self):
        data1 = {
            'bar': array([1,2,3]),
            'baz': array(['one', 'two', 'three']),
            }
        data2 = {
            'aaa': array([1,2,3,4,5]),
            'baz': array(['one', 'two', 'three', 'four', 'five']),
            }
        table_meta = {'mymeta': array([5,6])}
        col_meta = {'baz': {'description': 'this is a description of column baz'}}
        self.storage.write_table(table_name = 'foo1', table_data = data1, table_meta=table_meta) 
        self.storage.write_table(table_name = 'foo2', table_data = data2, column_meta=col_meta)          
              
        actual1 = self.storage.load_table(table_name = 'foo1', column_names = ['bar', 'baz'])           
        self.assertDictsEqual(data1, actual1)
        actual2 = self.storage.load_table(table_name = 'foo2')           
        self.assertDictsEqual(data2, actual2)
        self.assertEqual(self.storage.get_column_names('foo1'), ['bar', 'baz'])
        self.assertEqual(self.storage.get_table_names(), ['foo1', 'foo2'])
        self.assertEqual(self.storage.has_table('foo1'), True)
        self.assertEqual(self.storage.has_table('bar'), False)
        self.assertDictsEqual(self.storage.load_meta('foo1'), table_meta)
        self.assertDictsEqual(self.storage.load_meta('foo2', 'baz'), col_meta['baz'])
        self.assertDictsEqual(self.storage.load_meta('foo1', 'baz'), {})

if __name__ == '__main__':
    opus_unittest.main()   

