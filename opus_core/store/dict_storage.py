# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import copy

from numpy import array

from opus_core.store.storage import Storage

class dict_storage(Storage):
    def __init__(self):
        self._mystorage = {}
        
    def get_storage_location(self):
        return 'An in-memory dictionary'
        
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        result = {}
        
        try:
            available_column_names = self.get_column_names(table_name, lowercase)
            columns_to_load = self._select_columns(column_names, available_column_names) 
        except AttributeError, e:
            raise AttributeError("In table '%s': %s" % (table_name, e))
        
        if lowercase:
            col_map = dict([(col.lower(),col) 
                            for col in self.get_column_names(table_name, lowercase = False)])
        for column_name in columns_to_load:
            if lowercase:
                store_col_name = col_map[column_name]
            result[column_name] = copy.deepcopy(self._mystorage[table_name][store_col_name])

        return result
        
    def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
        if mode == Storage.APPEND:
            old_data = self.load_table(table_name = table_name)
            old_data.update(table_data)
            table_data = old_data
        self._get_column_size_and_names(table_data)
        self._mystorage[table_name] = copy.deepcopy(table_data)

    def get_column_names(self, table_name, lowercase=True):
        cols = self._mystorage[table_name].keys()
        if lowercase:
            cols = [col.lower() for col in cols]
        return cols
    
    def get_table_names(self):
        return self._mystorage.keys()
    
    
from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

from numpy import ma


class DictStorageTests(TestStorageInterface):
    def setUp(self):
        self.table_name = 'table'
        self.attr_name = 'attr'
        self.id_name = 'id'
        
        self.storage = dict_storage()
        
    def tearDown(self):
        del self.storage
        
    def test_write_table(self):
        data = {self.id_name:array([], dtype='int32')}
        expected_internal_storage = {self.table_name:data}
        
        self.storage.write_table(table_name=self.table_name, table_data=data)
        
        self.assert_(ma.allequal(self.storage._mystorage[self.table_name][self.id_name], 
            expected_internal_storage[self.table_name][self.id_name]))
        self.assertEqual(self.storage._mystorage[self.table_name].keys(), 
            expected_internal_storage[self.table_name].keys())
        self.assertEqual(self.storage._mystorage.keys(), expected_internal_storage.keys())
        
    def test_get_column_names(self):
        self.storage._mystorage = {self.table_name:{self.id_name:None, self.attr_name:None}}
        
        expected_field_names = self.storage._mystorage[self.table_name].keys()
        
        field_names = self.storage.get_column_names(table_name=self.table_name)
        
        self.assertEqual(field_names, expected_field_names)
        
    def test_load_table(self):
        expected_data = {
            'attribute1': array([1]),
            'attribute2': array([2]),
            }
        
        self.storage.write_table(table_name='table_name', table_data=expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name')
        self.assertDictsEqual(actual_data, expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name', column_names=Storage.ALL_COLUMNS)
        self.assertDictsEqual(actual_data, expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name', column_names=['attribute1', 'attribute2'])
        self.assertDictsEqual(actual_data, expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name', column_names=['attribute1'])
        expected_data = {
            'attribute1': array([1]),
            }
        self.assertDictsEqual(actual_data, expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name', column_names='attribute2')
        expected_data = {
            'attribute2': array([2]),
            }
        self.assertDictsEqual(actual_data, expected_data)
        
        actual_data = self.storage.load_table(table_name='table_name', column_names=[])
        expected_data = {}
        self.assertDictsEqual(actual_data, expected_data)
        
    def test_get_table_names_one_table(self):
        self.storage.write_table(table_name='table1', table_data={'a':array([1])})
        expected = ['table1']
        actual = self.storage.get_table_names()
        self.assertEquals(expected, actual)
        
    def test_get_table_names_two_tables(self):
        self.storage.write_table(table_name='table1', table_data={'a':array([1])})
        self.storage.write_table(table_name='table2', table_data={'a':array([1])})
        expected = ['table1', 'table2']
        expected.sort()
        actual = self.storage.get_table_names()
        actual.sort()
        self.assertEquals(expected, actual)
        
    def test_load_table_returns_copy(self):
        expected_data = {
            'attribute1': array([1]),
            }
            
        volatile_data = copy.deepcopy(expected_data)
        
        self.storage.write_table(table_name='table_name', table_data=volatile_data)
        
        actual_data1 = self.storage.load_table(table_name='table_name')
        actual_data1['attribute1'][0] = 2
        
        actual_data2 = self.storage.load_table(table_name='table_name')
        
        self.assertEqual(actual_data2['attribute1'][0], expected_data['attribute1'][0])
        self.assertNotEqual(actual_data2['attribute1'][0], actual_data1['attribute1'][0])
        
    def test_write_table_makes_copy(self):
        expected_data = {
            'attribute1': array([1]),
            }
            
        volatile_data = copy.deepcopy(expected_data)
        
        self.storage.write_table(table_name='table_name', table_data=volatile_data)

        volatile_data['attribute1'][0] = 2
        
        actual_data = self.storage.load_table(table_name='table_name')
        
        self.assertEqual(actual_data['attribute1'][0], expected_data['attribute1'][0])
        self.assertNotEqual(actual_data['attribute1'][0], volatile_data['attribute1'][0])
    

if __name__ == '__main__':
    opus_unittest.main()