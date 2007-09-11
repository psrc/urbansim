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

import os
import re
import csv

from opus_core.opus_error import OpusError
from opus_core.store.old.storage import Storage

class delimited_storage(Storage):
    """
    A storage object that saves table and attribute data into a directory, 
    giving each table its own file in the directory. Uses the Python csv module,
    which supports different field delimiters and quoting behaviors.
    """
    
    # Grab all of the csv.QUOTE_* properties to save the user from the need to
    #     import csv when specifying a quoting behavior.
    for property in dir(csv):
        if property.startswith('QUOTE_'):
            exec('%s = csv.%s' % (property, property))
    
    def __init__(self, 
            storage_location, 
            delimiter,  
            file_extension,
            quoting = csv.QUOTE_MINIMAL,
            doublequote = True,
            escapechar = None,
            lineterminator = '\r\n',
            quotechar = '"',
            skipinitialspace = False,
            ):
        self._output_directory = storage_location

        if len(file_extension) == 0:
            raise ValueError('File extension must be a non-empty string.')

        self._file_extension = file_extension
        
        # Initialize csv dialect
        self._delimiter = delimiter
        self._quoting = quoting
        self._doublequote = doublequote
        self._escapechar = escapechar
        self._lineterminator = lineterminator
        self._quotechar = quotechar
        self._skipinitialspace = skipinitialspace
        
        class MyDialect(csv.Dialect):
            delimiter = self._delimiter
            doublequote = self._doublequote
            escapechar = self._escapechar
            lineterminator = self._lineterminator
            quotechar = self._quotechar
            quoting = self._quoting
            skipinitialspace = self._skipinitialspace
        
        csv.register_dialect('my_format', MyDialect)
    
    def get_delimiter(self):
        return self._delimiter
    
    def write_dataset(self, write_resources):
        out_table_name = write_resources['out_table_name']
        values = write_resources['values']
        
        fixed_column_ordering = write_resources.get('fixed_column_ordering', None)
        append_type_info = write_resources.get('append_type_info', True)
        
        self._write_dataset(out_table_name, values, fixed_column_ordering, append_type_info)
    
    def _write_dataset(self, out_table_name, values, fixed_column_ordering = None, append_type_info = True):
        if not os.path.exists(self._output_directory):
            os.makedirs(self._output_directory)
        
        file_path = self._get_file_path_for_table(out_table_name)
        
        if fixed_column_ordering is None:
            attribute_names = values.keys()
            attribute_names.sort()
        else:
            attribute_names = fixed_column_ordering
        
        header = []
        attribute_values = []
        for attribute_name in attribute_names:
            if not append_type_info:
                column_header = attribute_name
            else:
                column_header = ('%s:%s%s' 
                    % (attribute_name, 
                       values[attribute_name].dtype.kind, 
                       values[attribute_name].dtype.itemsize))
            header.append(column_header)
            
            attribute_values.append(values[attribute_name])
        
        output = open(file_path, 'wb')
        try:
            writer = csv.writer(output, 'my_format')
            
            # write headers
            writer.writerow(header)
            
            # write data
            for i in range(len(attribute_values[0])):
                row = []
                for attribute in attribute_values:        
                    row.append(attribute[i])
                    
                writer.writerow(row)
        finally:
            output.close()
        
    def has_table(self, table_name):
        return os.path.exists(self._get_file_path_for_table(table_name))
    
    def _get_file_path_for_table(self, table_name):
        filename = '%s.%s' % (table_name, self._file_extension)
        return os.path.join(self._output_directory, filename)

    def _get_header_information(self, table_name):
        attribute_names, attribute_types = self.__get_header_information_from_table(table_name)
        
        if None in attribute_types:
            attribute_types = self.__infer_header_information_in_table(table_name, attribute_types)
            
        return attribute_names, attribute_types
    
    __attribute_name_and_type_pattern = re.compile('^\s*([_A-Za-z]\w*)\s*(?:\:\s*([buifcSUV][0-9]*)\s*)?$')
    def __get_header_information_from_table(self, table_name):
        file_path = self._get_file_path_for_table(table_name)
        
        if not os.path.exists(file_path):
            raise NameError("Table '%s' could not be found in %s." 
                % (table_name, self._output_directory))
        
        input = open(file_path, 'rb')
        try:
            reader = csv.reader(input, 'my_format')
            
            # load header
            header_information = reader.next()
            
        finally:
            input.close()
            
        available_attribute_names = []
        available_attribute_types = []
        for column_header in header_information:
            match = self.__attribute_name_and_type_pattern.match(column_header)
            
            if not match:
                raise NameError("Invalid column header '%s' in %s" % (column_header, file_path))
                
            available_attribute_names.append(match.group(1))
            available_attribute_types.append(match.group(2))
            
            
        return available_attribute_names, available_attribute_types
        
    def __infer_header_information_in_table(self, table_name, attribute_types):
        file_path = self._get_file_path_for_table(table_name)
        
        if not os.path.exists(file_path):
            raise NameError("Table '%s' could not be found in %s." 
                % (table_name, self._output_directory))
        
        input = open(file_path, 'rb')
        try:
            reader = csv.reader(input, 'my_format')
            
            # load header
            header_information = reader.next()
            
            try:
                first_data_row = reader.next()
            except:
                raise OpusError("Cannot determine the column types for table "
                    "'%s'. Type information must either be present in the "
                    "header or there must be at least one row of data from "
                    "which to infer it. (In file '%s')"
                        % (table_name, file_path))
            
        finally:
            input.close()
            
        header_information = []
        for column_value in first_data_row:
            try:
                float(column_value)
            except ValueError:
                header_information.append('S')
                
            else:
                header_information.append('f8')
            
        return header_information
    
    
from opus_core.tests import opus_unittest
from sets import Set
from shutil import rmtree
from tempfile import mkdtemp
from numpy import array
from opus_core.resources import Resources
from opus_core.tests.utils.cache_extension_replacements import replacements

class TestDelimitedStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage')
            
        self.storage = delimited_storage(
            storage_location = self.temp_dir,
            delimiter = ',',
            file_extension = 'csv',
            )
        
        self.table_name = 'test_table'
        self.storage._write_dataset(
            out_table_name = self.table_name,
            values = {
                'attribute1': array([1,2,3,4]),
                'attribute2': array([5.5,6.6,7.7,8.8]),
                'attribute3': array(['a','b','c','d']),
                }
            )
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test__write_dataset_to_nonexistent_directory(self):
        base_location = os.path.join(self.temp_dir, 'base')
        temp_location = os.path.join(base_location, 'some', 'nested', 'structure')
        temp_storage = delimited_storage(
            storage_location = temp_location,
            delimiter = ',',
            file_extension = 'spam',
            )
        
        temp_storage._write_dataset(
            out_table_name = 'foo',
            values = {
                'bar': array([1]),
                'baz': array([2]),
                }
            )
            
        self.assert_(os.path.exists(os.path.join(temp_location, 'foo.spam')))
            
        if os.path.exists(base_location):
            rmtree(base_location)
        
    def test_QUOTE_properties(self):
        try:
            self.storage.QUOTE_MINIMAL
        except:
            self.fail('Could not access the QUOTE_MINIMAL property of '
                'delimited_storage.')
    
    def test_trailing_spaces(self):
        """
        We expect that numpy strips extra spaces. Not much we can do about
        that. This test is really only here in hope that one day numpy will
        cease this behavior, in which case this test ought to fail.
        """
        expected_string = ' alpha'
        original_string = expected_string + ' '*10 # This should be at least 2 spaces
        self.assert_(original_string.endswith(' '))
        
        self.storage.write_dataset(Resources({
            'out_table_name': 'foo',
            'values': {
                'bar': array([original_string]),
                }
            }))
    
        file_path = self.storage._get_file_path_for_table('foo')
        self.assert_(os.path.exists(file_path))
        
        input = open(file_path, 'rb')
        try:
            input.readline()
            input.readline()
            
            line = input.readline()
            self.assert_(not len(line) > len(expected_string)+2) # allow for a possible \r\n
            
        finally:
            input.close()
            
    def test_has_table(self):
        self.assert_(not self.storage.has_table('foo'))
        
        self.storage.write_dataset(Resources({
            'out_table_name': 'foo',
            'values': {
                'bar': array([1]),
                }
            }))
        
        self.assert_(self.storage.has_table('foo'))
        
    def test_get_header_information_in_table(self):
        attribute_names, attribute_types = self.storage._delimited_storage__get_header_information_from_table(self.table_name)
        
        expected_attribute_types = ['i%(bytes)u'%replacements, 'f8', 'S1']
        self.assertEqual(attribute_types, expected_attribute_types)
        
    def test_attribute_name_and_type_pattern(self):
        pattern = self.storage._delimited_storage__attribute_name_and_type_pattern
        
        good_headers_to_test = [
            ('field_name:f8', 'field_name', 'f8'),
            (' field_name:f8', 'field_name', 'f8'),
            ('field_name :f8', 'field_name', 'f8'),
            ('field_name: f8', 'field_name', 'f8'),
            ('field_name:f8 ', 'field_name', 'f8'),
            ('field_name:f8\t', 'field_name', 'f8'),
            ('field_name', 'field_name', None),
            ('   field_name   ', 'field_name', None),
            ('_field_name', '_field_name', None),
            ('field_name1234', 'field_name1234', None),
            ('_', '_', None),
            ]
        
        for header, expected_name, expected_type in good_headers_to_test:
            match = pattern.match(header)
            
            self.assert_(match is not None)
            self.assertEqual(match.group(1), expected_name)
            self.assertEqual(match.group(2), expected_type)
             
        bad_headers_to_test = [
            'field_name!',
            ':f8',
            'field_name:',
            'a b',
            'field_name f8',
            'field_name:f8 f8',
            'field_name:32',
            'field_name:_f8',
            '1a',
            '!a',
            ]
        
        for header in bad_headers_to_test:
            match = pattern.match(header)
            
            self.assert_(match is None)
                 
    def test_infer_header_information_in_table(self):
        inferred_header_information = self.storage._delimited_storage__infer_header_information_in_table(
            table_name = self.table_name, 
            attribute_types = [None, None, None],
            )
        expected_header_information = ['f8', 'f8', 'S']
        self.assertEqual(expected_header_information, inferred_header_information)

        self.storage.write_dataset(Resources({
            'out_table_name': 'foo',
            'values': {
                'bar': array([], dtype='int32'),
                }
            }))

        self.assertRaises(OpusError, self.storage._delimited_storage__infer_header_information_in_table,
            table_name = 'foo', 
            attribute_types = [None],
            )
            
    def test_get_header_information(self):
        # Header information exists:
        attribute_names, attribute_types = self.storage._get_header_information(self.table_name)
        expected_attribute_names = ['attribute1', 'attribute2', 'attribute3']
        expected_attribute_types = ['i%(bytes)u'%replacements, 'f8', 'S1']
        
        self.assertEqual(expected_attribute_names, attribute_names)
        self.assertEqual(expected_attribute_types, attribute_types)
        
        # Make a file with no header information:
        file_path = self.storage._get_file_path_for_table('foo')
        foo = open(file_path, 'wb')
        try:
           foo.write("attribute1,attribute2,attribute3\n1,1.1,a")
           # attribute1,attribute2,attribute3
           # 1,1.1,a
        
        finally:
            foo.close()

        attribute_names, attribute_types = self.storage._get_header_information('foo')
        expected_attribute_names = ['attribute1', 'attribute2', 'attribute3']
        expected_attribute_types = ['f8', 'f8', 'S']
        
        self.assertEqual(expected_attribute_names, attribute_names)
        self.assertEqual(expected_attribute_types, attribute_types)
        
    def test_delimiter(self):
        base_dir = os.path.join(self.temp_dir, 'base')
        
        storage = delimited_storage(
            storage_location = base_dir,
            delimiter = '!',
            file_extension = 'bang',
            )
        
        storage.write_dataset(Resources({
            'out_table_name': 'foo',
            'values': {
                'bar': array([1]),
                'baz': array([2]),
                }
            }))

        expected_file_path = os.path.join(base_dir, 'foo.bang')
        self.assert_(os.path.exists(expected_file_path))
        
        foo_file = open(storage._get_file_path_for_table('foo'), 'rb')
        try:
            for line in foo_file:
                self.assert_('!' in line)
                
        finally:
            foo_file.close()      


if __name__ == '__main__':
    opus_unittest.main()