#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from sets import Set

from opus_core.resources import Resources
from opus_core.logger import logger

class Storage(object):
    """ Class for reading and writing to a storage device."""
    
    def write_dataset(self, write_resources=None):
        """Writes a dataset to the given storage media.
        Uses write_resourcess to determine what to write:
            'out_table_name' is the name of the 'table' to write. 
            'values' is a dictionary where keys are the attribute names and values 
                are value arrays of the corresponding attributes. 
            'attrtype' is a dictionary where keys are the attribute names and values 
                are the types of the corresponding attributes (PRIMARY,COMPUTED).
        """
        raise NotImplementedError, "Storage method 'write_dataset' not implemented."
                    

from opus_core.tests import opus_unittest


class TestStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = Storage()
        
    def tearDown(self):
        pass
        
    def test__select_attributes_case_sensitive(self):
        requested_attributes = ['A', 'b']
        available_attributes = ['A', 'b', 'c']
        expected_result = ['A', 'b']
        
        actual_result = self.storage._select_attributes(requested_attributes, available_attributes)
        
        self.assertEqual(expected_result, actual_result)
        
        requested_attributes = ['a']
        available_attributes = ['A']
        
        self.assertRaises(AttributeError, self.storage._select_attributes, requested_attributes, available_attributes)
        
    def test__select_attributes_raise_attribute_error_case_sensitive(self):
        requested_attributes = ['a', 'b']
        available_attributes = ['b', 'c']
        
        self.assertRaises(AttributeError, self.storage._select_attributes, requested_attributes, available_attributes)
        
    def test__select_attributes_case_insensitive(self):
        requested_attributes = ['a', 'B']
        available_attributes = ['A', 'b', 'c']
        expected_result = ['a', 'B']
        
        actual_result = self.storage._select_attributes(requested_attributes, available_attributes, case_insensitive=True)
        
        self.assertEqual(expected_result, actual_result)
        
        requested_attributes = ['a', 'B']
        available_attributes = ['b', 'c']
        
        self.assertRaises(AttributeError, self.storage._select_attributes, requested_attributes, available_attributes, case_insensitive=True)
        
        requested_attributes = ['a']
        available_attributes = ['a', 'A']
        
        self.assertRaises(AttributeError, self.storage._select_attributes, requested_attributes, available_attributes, case_insensitive=True)
    
    def test_get_python_type_from_numpy_type(self):
        self.assertEqual(self.storage._get_python_type_from_numpy_type('int32'), int)
        self.assertEqual(self.storage._get_python_type_from_numpy_type('string8'), str)
        
        self.assertRaises(KeyError, self.storage._get_python_type_from_numpy_type, 'int3333')
        
    def test_get_numpy_type_from_python_type(self):
        self.assertEqual(self.storage._get_numpy_type_from_python_type(int), 'int32')
        
        self.assertRaises(KeyError, self.storage._get_numpy_type_from_python_type, dict)
        
    def test__lower_case(self):
        expected = ['foo', 'bar', 'teststring']
        actual = self.storage._lower_case(['foo', 'BAR', 'TestString'])
        self.assertEqual(expected, actual)
        
        expected = 'foo'
        actual = self.storage._lower_case('FOO')
        self.assertEqual(expected, actual)

    
if __name__ == '__main__':
    opus_unittest.main()