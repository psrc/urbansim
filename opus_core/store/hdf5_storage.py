# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import h5py
import os
from glob import glob
from numpy import array, dtype
from opus_core.misc import unique
from opus_core.logger import logger
from opus_core.store.storage import Storage
import re

class hdf5_storage(Storage):
    """Storage class for hdf5 I/O. It supports a structure where every table attribute is 
            its own hdf5 'dataset'. For a structure using groups, see hdf5g_storage.
        """
    def __init__(self,  storage_location):
        self._base_directory = storage_location
        
    def get_storage_location(self):
        return self._base_directory
      
    def _get_file_path(self, file_name=None):
        dataset_path = self.get_storage_location()
        if not os.path.exists(dataset_path):
            raise StandardError("Path '%s' does not exist!" % dataset_path)
        if file_name is None:
            return dataset_path
        return os.path.join(dataset_path, file_name)
    
    def _get_file_path_for_table(self, table_name):
        return self._get_file_path('%s.hdf5' % table_name)
    
    def _load_columns(self, f, column_names, lowercase=True):
        result = {}
        for column_name in f.keys():
            if lowercase:
                column_name = column_name.lower()
            if column_names == Storage.ALL_COLUMNS or column_name in column_names:
                result[column_name] = f[column_name][...]
        return result
    
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        """
        The table is loaded from a file called {table_name}.hdf5 assuming to have a 'flat' structure
        (i.e. each table column is a hdf5 dataset on the most upper level).
        """        
        full_file_name = self._get_file_path_for_table(table_name)   
        f = h5py.File(full_file_name, 'r')
        result = self._load_columns(f, column_names, lowercase)               
        f.close()
        return result

    def _get_hdf5mode(self, mode):
        h5mode = mode
        if mode == Storage.APPEND:
            h5mode = 'a'
        elif mode == Storage.OVERWRITE:
            h5mode = 'w'
        return h5mode
    
    def _get_meta(self, f, column_name):
        if column_name is None:
            meta = dict(f.attrs.items())
        else:
            meta = dict(f[column_name].attrs.items())
        return meta
    
    def load_meta(self, table_name, column_name=None):
        file_name = self._get_file_path_for_table(table_name)   
        f = h5py.File(file_name, 'r')
        meta = self._get_meta(f, column_name)
        f.close()
        return meta
    
    def _write_columns(self, f, column_names, table_data, table_meta={}, column_meta={}, **kwargs):
        for mkey, mvalue in table_meta.iteritems():
            f.attrs[mkey] = mvalue
        for column_name in column_names:                    
            column_ds = f.create_dataset(column_name, data=table_data[column_name], **kwargs)
            ds_meta = column_meta.get(column_name, {})
            for mkey, mvalue in ds_meta.iteritems():
                column_ds.attrs[mkey] = mvalue
            
    def write_table(self, table_name, table_data, mode = Storage.OVERWRITE, table_meta={}, column_meta={}, driver=None, **kwargs):
        """
        Argument table_name specifies the file name in the base storage directory (without the suffix '.hdf5'). 
        table_data is a dictionary where keys are the column names and values 
            are value arrays of the corresponding columns.
        Each column is stored as an hdf5 dataset.
        Meta data for the whole table and/or for the columns can be passed as dictionaries table_meta and column_meta, respectively.
        Keys in column_meta have to correspond to column names. The values are again dictionaries with the meta data 
        which can be either strings, scalar or arrays (this is hdf5 restriction).
        Argument driver is passed to the h5py.File. kwargs are passed to the h5py create_dataset function, 
        e.g. compression. 
        """
        dir = self.get_storage_location()        
        if not os.path.exists(dir):
            logger.log_status("%s doesn't exist and is created" % dir)
            os.makedirs(dir)
        unused_column_size, column_names = self._get_column_size_and_names(table_data)
        f = h5py.File(os.path.join(dir, '%s.hdf5' % table_name), self._get_hdf5mode(mode), driver=driver)
        self._write_columns(f, column_names, table_data, table_meta, column_meta, **kwargs)
        f.close()

    def get_column_names(self, table_name, lowercase=True):
        full_file_name = self._get_file_path_for_table(table_name) 
        f = h5py.File(full_file_name, 'r')
        result = f.keys()
        if lowercase:
            result = self._lower_case(result)
        f.close()
        return result

    def get_table_names(self):
        file_names = glob(os.path.join(self.get_storage_location(), '*.hdf5'))
        return [os.path.splitext(os.path.basename(file_name))[0] for file_name in file_names]
    
    def has_table(self, table_name):
        return os.path.exists(self._get_file_path_for_table(table_name))
    

    
from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface
from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

class TestHDF5Storage(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_hdf5_storage')            
        self.storage = hdf5_storage(storage_location=self.temp_dir)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test_hdf5_storage(self):
        data = {
            'bar': array([1,2,3]),
            'baz': array(['one', 'two', 'three']),
            }
        table_meta = {'mymeta': array([5,6])}
        col_meta = {'bar': {'description': 'this is a description of column bar'}}
        
        self.storage.write_table(
            table_name = 'foo',
            table_data = data,
            table_meta = table_meta,
            column_meta = col_meta
            )          
        filename = os.path.join(self.temp_dir, 'foo.hdf5')
        self.assert_(os.path.exists(filename))
              
        actual = self.storage.load_table(
            table_name = 'foo', 
            column_names = ['bar', 'baz']
            )           
        self.assertDictsEqual(data, actual)
        self.assertEqual(self.storage.get_column_names('foo'), ['bar', 'baz'])
        self.assertEqual(self.storage.get_table_names(), ['foo'])
        self.assertEqual(self.storage.has_table('foo'), True)
        self.assertEqual(self.storage.has_table('bar'), False)
        self.assertDictsEqual(self.storage.load_meta('foo'), table_meta)
        self.assertDictsEqual(self.storage.load_meta('foo', 'bar'), col_meta['bar'])
        self.assertDictsEqual(self.storage.load_meta('foo', 'baz'), {})
        
if __name__ == '__main__':
    opus_unittest.main()   

