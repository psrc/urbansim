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

from opus_core.store.delimited_storage import delimited_storage


class tab_storage(delimited_storage):
    def __init__(self, storage_location, *args, **kwargs):
        delimited_storage.__init__(self, 
            storage_location,
            delimiter = '\t',
            file_extension = 'tab', 
            *args, **kwargs
            )


from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

import os

from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

class TestTabStorage(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage')
            
        self.storage = tab_storage(storage_location=self.temp_dir)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    # Simple test. There's no need to test delimited_storage all over again.
    def test_tab_storage(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1,2,3]),
                'baz': array(['one', 'two', 'three']),
                }
            )
            
        filename = os.path.join(self.temp_dir, 'foo.tab')
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