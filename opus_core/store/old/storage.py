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
        

    def _select_attributes(self, requested_attributes, available_attributes,
                           case_insensitive=False):
        """
        requested_attributes may be one of:
            '*' - get all
            'a_name' - just get attribute named 'a_name'
            ['a', 'b'] - only get attributes 'a' and 'b'
        if case_insensitive is true the method raises an exception if 
        available_attributes contains duplicate case-insensitive entries
        """
        result = []
                
        if requested_attributes == '*':
            result = available_attributes
            
        else:
            if not isinstance(requested_attributes, list):
                requested_attributes = [requested_attributes]
                
            if case_insensitive:
                available_attributes_lower = list(Set([
                    each_attribute.lower() 
                    for each_attribute in available_attributes
                    ]))
                if len(available_attributes)!=len(available_attributes_lower):
                    raise AttributeError("List of available attributes "
                        "contains duplicate case-insensitive entries.")
            
                for attribute_name in requested_attributes:
                    if attribute_name.lower() not in available_attributes_lower:
                        raise AttributeError("Requested attribute '%s' is not an "
                            "available attribute."
                                % attribute_name)
                    
                    result.append(attribute_name)
                
            else:
                for attribute_name in requested_attributes:
                    if attribute_name not in available_attributes:
                        raise AttributeError("Requested attribute '%s' is not an "
                            "available attribute."
                                % attribute_name)
                
                    result.append(attribute_name)
                            
        return result
        
    def _lower_case(self, string_or_list_of_strings):
        """
        Returns a new string or a new list of strings matching the original, 
        save that the string or each string in the list is now lowercase.
        """
        try:
            result = string_or_list_of_strings.lower()
        except AttributeError:
            result = [each_string.lower() for each_string in string_or_list_of_strings]
        return result
        
    def _get_python_type_from_numpy_type(self, numpy_type):
        """
        Return the Python type to use for the values in a numpy array container.
        """
        if numpy_type.startswith('string'):
            return str   
            
        return self.__NUMPY_TYPE_TO_PYTHON_TYPE_MAP[numpy_type]
    
    __NUMPY_TYPE_TO_PYTHON_TYPE_MAP = {
        'bool8': bool,
        'int8': int,
        'uint8': int,
        'int16': int,
        'uint16': int,
        'int32': int,
        'uint32': int,
        'int64': long,
        'uint64': long,
        'float32': float,
        'float64': float,
        'complex64': complex,
        'complex128': complex,
        }
    
    def _get_numpy_type_from_python_type(self, python_type):
        return self.__PYTHON_TYPE_TO_NUMPY_TYPE_MAP[python_type]
    
    __PYTHON_TYPE_TO_NUMPY_TYPE_MAP = {
        int: 'int32',
        long: 'int64',
        float: 'float32',
        str: 'a255',
        unicode: 'a255',
        }
            

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