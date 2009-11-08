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

from opus_core.store.old.storage import Storage


class dict_storage(Storage):
    def __init__(self):
        self._mystorage = {}
        
    def _write_dataset(self, out_table_name, values):
        self._mystorage[out_table_name] = copy.deepcopy(values)

    def _determine_field_names(self, in_table_name):
        return self._mystorage[in_table_name].keys()
    
        
    def determine_field_names(self, load_resources, attributes='*'):
        in_table_name = load_resources['in_table_name']
        return self._determine_field_names(in_table_name=in_table_name)

    def write_dataset(self, write_resources):
        out_table_name = write_resources['out_table_name']
        values = write_resources['values']
        
        self._write_dataset(out_table_name=out_table_name, values=values)
        
from opus_core.tests import opus_unittest

from numpy import ma

class DictStorageTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.table_name = 'table'
        self.attr_name = 'attr'
        self.id_name = 'id'
        
        self.storage = dict_storage()
        
    def tearDown(self):
        del self.storage
        
    def test_write_dataset(self):
        data = {self.id_name:array([], dtype='int32')}
        expected_internal_storage = {self.table_name:data}
        
        self.storage._write_dataset(self.table_name, data)
        
        self.assert_(ma.allequal(self.storage._mystorage[self.table_name][self.id_name], 
            expected_internal_storage[self.table_name][self.id_name]))
        self.assertEqual(self.storage._mystorage[self.table_name].keys(), 
            expected_internal_storage[self.table_name].keys())
        self.assertEqual(self.storage._mystorage.keys(), expected_internal_storage.keys())
        
    def test_determine_field_names(self):
        self.storage._mystorage = {self.table_name:{self.id_name:None, self.attr_name:None}}
        
        expected_field_names = self.storage._mystorage[self.table_name].keys()
        
        field_names = self.storage._determine_field_names(self.table_name)
        
        self.assertEqual(field_names, expected_field_names)
        
if __name__ == '__main__':
    opus_unittest.main()