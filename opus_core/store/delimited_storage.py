# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import re
import csv
from glob import glob

from numpy import array, dtype
from numpy.random import randint
from opus_core.opus_error import OpusError
from opus_core.logger import logger
from opus_core.store.storage import Storage


class delimited_storage(Storage):
    """
    A storage object that saves table and value data into a directory, 
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

        if not file_extension:
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
        self._dialect_name = "my_format%s" % randint(0, 99999999)
        
        class MyDialect(csv.Dialect):
            delimiter = self._delimiter
            doublequote = self._doublequote
            escapechar = self._escapechar
            lineterminator = self._lineterminator
            quotechar = self._quotechar
            quoting = self._quoting
            skipinitialspace = self._skipinitialspace
        
        csv.register_dialect(self._dialect_name, MyDialect)
        
    def get_storage_location(self):
        return self._output_directory
    
    def write_table(self, 
                    table_name, 
                    table_data, 
                    mode = Storage.OVERWRITE,
                    fixed_column_order = None,
                    append_type_info = True):
        
        if not os.path.exists(self._output_directory):
            os.makedirs(self._output_directory)
        
        file_path = self._get_file_path_for_table(table_name)

        if mode == Storage.APPEND:
            old_data = self.load_table(table_name = table_name)
            old_data.update(table_data)
            table_data = old_data
                    
        column_size, column_names = self._get_column_size_and_names(table_data)
        
        if fixed_column_order is None:
            column_names.sort()
        else:
            column_names = fixed_column_order
        
        header = []
        values = []
        for column_name in column_names:
            if append_type_info:
                column_header = ('%s:%s%s' 
                    % (column_name, 
                       table_data[column_name].dtype.kind,
                       table_data[column_name].dtype.itemsize))
            else:
                column_header = column_name
                
            header.append(column_header)
            values.append(table_data[column_name])
            
        output = open(file_path, 'wb')
        try:
            writer = csv.writer(output, self._dialect_name)
            
            # write headers
            writer.writerow(header)
            
            # write data
            for i in range(column_size):
                row = []
                for value in values:        
                    row.append(value[i])
                    
                writer.writerow(row)
        finally:
            output.close()
        
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        file_path = self._get_file_path_for_table(table_name)
        
        if not os.path.exists(file_path):
            raise NameError("Table '%s' could not be found in %s." 
                % (table_name, self._output_directory))
        
        # load header
        available_column_names, available_column_types = self._get_header_information(table_name)
        
        if lowercase:
            available_column_names = self._lower_case(available_column_names)
        
        input = open(file_path, 'rb')
        try:
            reader = csv.reader(input, self._dialect_name)
            
            reader.next() # skip header because it was already read above
    
            index_map = self._get_index_map(column_names, available_column_names)
            
            # load data
            result = []
            for dummy_column_name in available_column_types:
                result.append([])
                
            for row in reader:
                for i in range(len(row)):
                    if i in index_map:
                        if available_column_types[i] == 'b1':
                            result[i].append(row[i] == 'True')
                        elif available_column_types[i] == 'f4':
                            result[i].append(float(row[i]))
                        else:
                            result[i].append(row[i])

                    
            table = {}
            for index in index_map:
                column_dtype = dtype(available_column_types[index])
                
                # Cast each value to its appropriate python type.
                for j in range(len(result[index])):
                    try:
                        result[index][j] = column_dtype.type(result[index][j])
                    except:
                        logger.log_error("Error encountered when processing row %s for column %s of type %s: %s." % \
                                         (j+1, available_column_names[index], column_dtype, result[index][j]) )
                        raise
                    
                table[available_column_names[index]] = array(result[index], dtype=column_dtype)
        
        finally:
            input.close()
        
        return table
        
    def get_column_names(self, in_table_name, lowercase=True):
        available_column_names, dummy_available_column_types = self._get_header_information(in_table_name)
        if lowercase:
            available_column_names = self._lower_case(available_column_names)
        return available_column_names
    
    def get_table_names(self):
        file_names = glob(os.path.join(self._output_directory, '*.%s' % self._file_extension))
        return [os.path.splitext(os.path.basename(file_name))[0] for file_name in file_names]
        
    def has_table(self, table_name):
        return os.path.exists(self._get_file_path_for_table(table_name))
    
    def _get_index_map(self, column_names, available_column_names):
        """
        Returns a list whose entries are either None or an index.
        If the value is None, it means that that entry in 
        available_column_names was not requested.
        If the value is an index, it means that the location of the 
        requested value name is at that index location in
        the available_column_names list.
        
        column_names may be:
            Storage.ALL_COLUMNS - include all columns
            'a_name' - include just the column named 'a_name'
            ['a', 'b'] - include just the column 'a' and 'b'.
        """
        selected_column_names = self._select_columns(column_names, available_column_names)        
        
        column_index = {}
        for i in range(len(available_column_names)):
            column_index[available_column_names[i]] = i
            
        index_map = []
        for column_name in selected_column_names:
            try:
                index = column_index[column_name]
            except KeyError:
                raise AttributeError("Column '%s' is not available." 
                    % column_name)
                
            index_map.append(index)
            
        return index_map
    
    def _get_file_path_for_table(self, table_name):
        filename = '%s.%s' % (table_name, self._file_extension)
        return os.path.join(self._output_directory, filename)

    def _get_header_information(self, table_name):
        column_names, column_types = self.__get_header_information_from_table(table_name)
        
        inferred_column_types = None
        for i in range(len(column_types)):
            if column_types[i] is None:
                if inferred_column_types is None:
                    inferred_column_types = self.__infer_header_information_in_table(table_name)
                column_types[i] = inferred_column_types[i]
            elif re.match(r'S[0-9]+', column_types[i]):
                column_types[i] = 'S'
                
        return column_names, column_types
    
    __column_name_and_type_pattern = re.compile('^\s*([_A-Za-z][\w\.]*)\s*(?:\:\s*([buifcSUV][0-9]*)\s*)?$')
    def __get_header_information_from_table(self, table_name):
        file_path = self._get_file_path_for_table(table_name)
        
        if not os.path.exists(file_path):
            raise NameError("Table '%s' could not be found in %s." 
                % (table_name, self._output_directory))
        
        input = open(file_path, 'rb')
        try:
            reader = csv.reader(input, self._dialect_name)
            
            # load header
            header_information = reader.next()
            
        finally:
            input.close()
            
        available_column_names = []
        available_column_types = []
        for column_header in header_information:
            match = self.__column_name_and_type_pattern.match(column_header)
            
            if not match:
                raise NameError("Invalid column header '%s' in %s" % (column_header, file_path))
                
            available_column_names.append(match.group(1))
            available_column_types.append(match.group(2))

        return available_column_names, available_column_types
        
    def __infer_header_information_in_table(self, table_name):
        file_path = self._get_file_path_for_table(table_name)
        
        if not os.path.exists(file_path):
            raise NameError("Table '%s' could not be found in %s." 
                % (table_name, self._output_directory))
        
        input = open(file_path, 'rb')
        try:
            reader = csv.reader(input, self._dialect_name)
            
            # skip header
            reader.next()
            
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
from opus_core.store.storage import TestStorageInterface
from opus_core.tests.utils.cache_extension_replacements import replacements
from shutil import rmtree
from tempfile import mkdtemp

class TestDelimitedStorage(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage')
            
        self.storage = delimited_storage(
            storage_location = self.temp_dir,
            delimiter = ',',
            file_extension = 'csv',
            )
        
        self.table_name = 'test_table'
        self.storage.write_table(
            table_name = self.table_name,
            table_data = {
                'attribute1': array([1,2,3,4]),
                'attribute2': array([5.5,6.6,7.7,8.8]),
                'attribute3': array(['a','b','c','d']),
                }
            )
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test_write_table_to_nonexistent_directory(self):
        base_location = os.path.join(self.temp_dir, 'base')
        temp_location = os.path.join(base_location, 'some', 'nested', 'structure')
        temp_storage = delimited_storage(
            storage_location = temp_location,
            delimiter = ',',
            file_extension = 'spam',
            )
        
        temp_storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1]),
                'baz': array([2]),
                }
            )
            
        self.assert_(os.path.exists(os.path.join(temp_location, 'foo.spam')))
            
        if os.path.exists(base_location):
            rmtree(base_location)
        
    def test_load_table(self):
        self.assert_(os.path.exists(
            os.path.join(self.temp_dir, '%s.csv' % self.table_name)))
        
        expected = {
            'attribute1': array([1,2,3,4]),
            'attribute2': array([5.5,6.6,7.7,8.8]),
            'attribute3': array(['a','b','c','d']),
            }
        actual = self.storage.load_table(table_name=self.table_name)
        self.assertDictsEqual(expected, actual)
        
        self.assertRaises(NameError, self.storage.load_table, table_name='idonotexist')
        
        expected = {
            'attribute1': array([1,2,3,4]),
            'attribute2': array([5.5,6.6,7.7,8.8]),
            'attribute3': array(['a','b','c','d']),
            }
        actual = self.storage.load_table(table_name=self.table_name, column_names=Storage.ALL_COLUMNS)
        self.assertDictsEqual(expected, actual)
        
        expected = {
            'attribute1': array([1,2,3,4]),
            }
        actual = self.storage.load_table(table_name=self.table_name, column_names=['attribute1'])
        self.assertDictsEqual(expected, actual)
        
        expected = {
            'attribute1': array([1,2,3,4]),
            'attribute2': array([5.5,6.6,7.7,8.8]),
            }
        actual = self.storage.load_table(table_name=self.table_name, column_names=['attribute1', 'attribute2'])
        self.assertDictsEqual(expected, actual)
        
    def test_write_table_and_load_table(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1]),
                'baz': array([2]),
                }
            )
            
        expected = {
            'bar': array([1]),
            'baz': array([2]),
            }
        
        actual = self.storage.load_table(table_name='foo', column_names=['bar', 'baz'])
        self.assertDictsEqual(expected, actual)
        
    def test_get_column_names(self):
        expected = ['attribute1', 'attribute2', 'attribute3']
        actual = self.storage.get_column_names(in_table_name=self.table_name)
        
        self.assertEqual(expected, actual)
        
        self.assertRaises(NameError, self.storage.get_column_names, in_table_name='idonotexist')
    
    def test_get_index_map(self):
        actual = self.storage._get_index_map(
            column_names = ['b', 'd'],
            available_column_names = ['a', 'b', 'c', 'd', 'e'],
            )
        expected = [1, 3]
        self.assertEqual(expected, actual)
        
        actual = self.storage._get_index_map(
            column_names = Storage.ALL_COLUMNS,
            available_column_names = ['a', 'b', 'c', 'd', 'e'],
            )
        expected = range(len(['a', 'b', 'c', 'd', 'e']))
        self.assertEqual(expected, actual)        
        
        actual = self.storage._get_index_map(
            column_names = 'c',
            available_column_names = ['a', 'b', 'c', 'd', 'e'],
            )
        expected = [2]
        self.assertEqual(expected, actual)         
        
        actual = self.storage._get_index_map(
            column_names = ['a', 'e'],
            available_column_names = ['a', 'b', 'c', 'd', 'e'],
            )
        expected = [0, 4]
        self.assertEqual(expected, actual)
        
        self.assertRaises(AttributeError, self.storage._get_index_map,
            column_names = ['z'],
            available_column_names = ['a', 'b', 'c', 'd', 'e'],
            )
            
    def test_stings_with_quotes_and_commas_data(self):
        
        expected_data = {
            'a': array(["a,b", "a'b", 'a"b', '"a","b"']),
            'b': array(["a,b", "a b", 'a b', ' a , b ']),
            'c': array(["a b", "a'b", 'a"b', '"a" "b"']),
            'd': array(["a b", "a b", 'a b', ' a   b ']),
            }
        
        self.storage.write_table(
            table_name = 'foo',
            table_data = expected_data
            )
        
        actual_data = self.storage.load_table(table_name='foo')
        self.assertDictsEqual(expected_data, actual_data)

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
        
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([original_string]),
                }
            )
    
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
            
    def test_lowercase(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1]),
                'BAZ': array([2]),
                },
            )
        
        actual = self.storage.get_column_names(
            in_table_name = 'foo',
            lowercase = False,
            )
        expected = ['bar', 'BAZ']
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), len(expected))
        
        actual = self.storage.get_column_names(
            in_table_name = 'foo',
            lowercase = True,
            )
        expected = ['bar', 'baz']
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), len(expected))
        
        actual_data = self.storage.load_table(
            table_name = 'foo',
            lowercase = False,
            )
        expected = ['bar', 'BAZ']
        self.assertEqual(actual_data.keys(), expected)
        
        actual_data = self.storage.load_table(
            table_name = 'foo',
            lowercase = True,
            )
        expected = ['bar', 'baz']
        self.assertEqual(actual_data.keys(), expected)
        
    def test_has_table(self):
        self.assert_(not self.storage.has_table('foo'))
        
        self.storage.write_table(
            table_name = 'foo',
            table_data =  {
                'bar': array([1]),
                }
            )
        
        self.assert_(self.storage.has_table('foo'))
        
    def test_get_header_information_in_table(self):
        dummy_column_names, column_types = self.storage._delimited_storage__get_header_information_from_table(self.table_name)      
        expected_column_types = ['i%(bytes)u'%replacements, 'f8', 'S1']
        self.assertEqual(column_types, expected_column_types)
        
    def test_column_name_and_type_pattern(self):
        pattern = self.storage._delimited_storage__column_name_and_type_pattern
        
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
            )
        expected_header_information = ['f8', 'f8', 'S']
        self.assertEqual(expected_header_information, inferred_header_information)
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([], dtype='int32'),
                }
            )
        self.assertRaises(OpusError, self.storage._delimited_storage__infer_header_information_in_table,
            table_name = 'foo', 
            )
            
    def test_get_header_information(self):
        # Header information exists:
        column_names, column_types = self.storage._get_header_information(self.table_name)
        expected_column_names = ['attribute1', 'attribute2', 'attribute3']
        expected_column_types = ['i%(bytes)u'%replacements, 'f8', 'S']
        self.assertEqual(expected_column_names, column_names)
        self.assertEqual(expected_column_types, column_types)
        # Make a file with no header information:
        file_path = self.storage._get_file_path_for_table('foo')
        foo = open(file_path, 'wb')
        try:
            foo.write("attribute1,attribute2,attribute3\n1,1.1,a")
           # attribute1,attribute2,attribute3
           # 1,1.1,a
        finally:
            foo.close()
        column_names, column_types = self.storage._get_header_information('foo')
        expected_column_names = ['attribute1', 'attribute2', 'attribute3']
        expected_column_types = ['f8', 'f8', 'S']
        self.assertEqual(expected_column_names, column_names)
        self.assertEqual(expected_column_types, column_types)
        
    def test_delimiter(self):
        base_dir = os.path.join(self.temp_dir, 'base')
        
        storage = delimited_storage(
            storage_location = base_dir,
            delimiter = '!',
            file_extension = 'bang',
            )
        
        storage.write_table(
            table_name = 'foo',
            table_data = {
                'bar': array([1]),
                'baz': array([2]),
                }
            )

        expected_file_path = os.path.join(base_dir, 'foo.bang')
        self.assert_(os.path.exists(expected_file_path))
        
        foo_file = open(storage._get_file_path_for_table('foo'), 'rb')
        try:
            for line in foo_file:
                self.assert_('!' in line)
                
        finally:
            foo_file.close()
            
    def test_two_delimited_storage_objects(self):
        tab_storage = delimited_storage(
            storage_location = self.temp_dir,
            delimiter = '\t',
            file_extension = 'tab',
            )
        
        tab_storage.write_table(
            table_name = 'test_table2',
            table_data = {
                'attr1': array([1,2,3,4]),
                'attr2': array(['a','b','c','d']),
                }
            )
            
        expected = {
            'attribute1': array([1, 2,3,4])
            }
        expected2 = {
            'attr1': array([1, 2,3,4])
            }
        # read from csv
        actual = self.storage.load_table(table_name='test_table', column_names=['attribute1'])
        self.assertDictsEqual(expected, actual)
        # read from tab
        actual = tab_storage.load_table(table_name='test_table2', column_names=['attr1'])
        self.assertDictsEqual(expected2, actual)
            
class TestDelimitedStorageGetTableNames(TestStorageInterface):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage_get_table_names')
        self.storage = delimited_storage(
            storage_location = self.temp_dir,
            delimiter = ',',
            file_extension = 'test',
            )
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_get_table_names_one_table(self):
        open(os.path.join(self.temp_dir, 'table1.test'), 'w').close()
        expected = ['table1']
        actual = self.storage.get_table_names()
        self.assertEquals(expected, actual)
        
    def test_get_table_names_many_tables(self):
        expected = ['table1', 'table2', 'table7']
        expected.sort()
        for table_name in expected:
            open(os.path.join(self.temp_dir, '%s.test' % table_name), 'w').close()
        actual = self.storage.get_table_names()
        actual.sort()
        self.assertEquals(expected, actual)


if __name__ == '__main__':
    opus_unittest.main()
