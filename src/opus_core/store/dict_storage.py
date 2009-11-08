#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import copy

from numpy import array

from opus_core.store.storage import Storage
from opus_core.store.old.dict_storage import dict_storage as dict_storage_old

class dict_storage(Storage, dict_storage_old):
    def __init__(self):
        self._mystorage = {}
        
    def get_storage_location(self):
        return 'An in-memory dictionary'
        
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True,
            id_name=None # Not used for this storage, but required for SQL-based storages
            ):
        ### TODO: Use lowercase
        result = {}
        
        try:
            columns_to_load = self._select_columns(column_names, self._mystorage[table_name])
        except AttributeError, e:
            raise AttributeError("In table '%s': %s" % (table_name, e))
        
        for column_name in columns_to_load:
            result[column_name] = copy.deepcopy(self._mystorage[table_name][column_name])

        return result
        
    def write_table(self, table_name, table_data):
        self._get_column_size_and_names(table_data)
        self._mystorage[table_name] = copy.deepcopy(table_data)

    def get_column_names(self, table_name, lowercase=True):
        ### TODO: Use lowercase
        return self._mystorage[table_name].keys()
    
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