# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.store.delimited_storage import delimited_storage

class csv_storage(delimited_storage):
    def __init__(self, storage_location, *args, **kwargs):
        delimited_storage.__init__(self, 
            storage_location,
            delimiter = ',',
            file_extension = 'csv', 
            *args, **kwargs
            )


from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

import os

from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

class TestCsvStorage(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage')
            
        self.storage = csv_storage(storage_location=self.temp_dir)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    # Simple test. There's no need to test delimited_storage all over again.
    def test_csv_storage(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1,2,3]),
                'baz': array(['one', 'two', 'three']),
                }
            )
            
        filename = os.path.join(self.temp_dir, 'foo.csv')
        self.assert_(os.path.exists(filename))
            
        expected = {
            'bar': array([1,2,3]),
            'baz': array(['one', 'two', 'three']),
            }
            
        actual = self.storage.load_table(
            table_name = 'foo', 
            column_names = ['bar', 'baz']
            )
            
        self.assertDictsEqual(expected, actual)

if __name__ == '__main__':
    opus_unittest.main()