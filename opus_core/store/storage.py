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

from sets import Set
from numpy import array
from opus_core.store.old.storage import Storage as Storage_old

class Storage(Storage_old):
    ALL_COLUMNS = '*'
    
    def get_storage_location(self):
        """Returns a unique description of the location that this storage object is
        reading from or writing to.
        """
        raise NotImplementedError()
    
    def get_table_names(self):
        """
        Returns a list of the names of the tables in storage. 
        """
        return []

    # _load_dataset
    def load_table(self, table_name, column_names=ALL_COLUMNS, lowercase=True,
            id_name=None # Required for SQL-based storages
            ):
        """
        Returns a dictionary with the data for the requested columns.
        
        e.g.: {
            'column1': array([...data...]),
            'column2': array([...data...]),
            .
            .
            .
            }
        """
        raise NotImplementedError()
        
    # _write_dataset
    def write_table(self, table_name, table_data):
        """
        Writes the given table to storage with the given name. The table_data
        parameter takes a dictionary with the column data.
        
        e.g.: {
            'column1': array([...data...]),
            'column2': array([...data...]),
            .
            .
            .
            }
        Raises a ValueError if table_data is empty or the column_sizes are different
        """
        self._get_column_size_and_names(table_data)
        raise NotImplementedError()

    # _determine_field_names
    def get_column_names(self, table_name, lowercase=True):
        """
        Returns a list of the columns in the given table.
        """
        raise NotImplementedError()
    
    def chunk_columns(self, table_name, column_names=ALL_COLUMNS, nchunks=1):
        """Returns a nested list of columns using column_names as input. 
        The list of column names is chunked into an even list nchunk elements
        whereof each element is a list of columns.
        e.g.: column_names=['col1','col2','col3','col4','col5'] and nchunks=3
        returns [ ['col1','col2'],['col3','col4'],['col5'] ]
        
        if column_names is empty the method returns an empty list
        if the number of chunks (nchunks) is higher than the number of 
        column_names the method returns a list of number of column_names lists
        with each column_name in its own list.
        e.g.: column_names=['col1','col2','col3'] and nchunks=5
        returns [ ['col1'],['col2'],['col3'] ]
        """
        
        available_column_names = self.get_column_names(table_name)
        if table_name+'.computed' in self.get_table_names():
            available_column_names = available_column_names + self.get_column_names(table_name+'.computed')
            
        column_names = self._select_columns(column_names, available_column_names)
        number_of_columns = len(column_names)
        result = []
        if number_of_columns>0:
            chunksize = max(1,int(number_of_columns/nchunks)+1)
            number_of_chunks = min(nchunks, number_of_columns)
            lastchunk = number_of_columns - (number_of_chunks-1)*chunksize
            
            for i in range(number_of_chunks)[0:(number_of_chunks-1)]:
                result = result + [column_names[i*chunksize:(i+1)*chunksize]]
            result = result + \
                [column_names[(number_of_columns-lastchunk):number_of_columns]]
        return result
    
    def _get_column_size_and_names(self, table_data):
        column_names = table_data.keys()
        # Check that every column has the same number of items
        column_size = None
        for column_name in column_names:
            next_column_size = table_data[column_name].size
            if column_size is None:
                column_size = next_column_size
            
            if not next_column_size == column_size:
                raise ValueError('Data in each column must be of the same length.')
            
        
        if column_size is None:
            raise ValueError('No data to write!')
        
        return column_size, column_names
    
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
    
    def _select_columns(self, requested_columns, available_columns,
                           case_insensitive=False):
        """
        requested_columns may be one of:
            Storage.ALL_COLUMNS - get all
            'a_name' - just get column named 'a_name'
            ['a', 'b'] - only get column 'a' and 'b'
        if case_insensitive is true the method raises an exception if 
        available_columns contains duplicate case-insensitive entries
        """
        result = []
                
        if requested_columns == Storage.ALL_COLUMNS:
            result = available_columns
            
        else:
            if not isinstance(requested_columns, list):
                requested_columns = [requested_columns]
                
            if case_insensitive:
                available_columns_lower = list(Set([
                    each_column.lower() 
                    for each_column in available_columns
                    ]))
                if len(available_columns)!=len(available_columns_lower):
                    raise AttributeError("List of available columns "
                        "contains duplicate case-insensitive entries.")
            
                for column_name in requested_columns:
                    if column_name.lower() not in available_columns_lower:
                        raise AttributeError("Requested column '%s' is not an "
                            "available column."
                                % column_name)
                    
                    result.append(column_name)
                
            else:
                for column_name in requested_columns:
                    if column_name not in available_columns:
                        raise AttributeError("Requested column '%s' is not an "
                            "available column."
                                % column_name)
                
                    result.append(column_name)
                            
        return result
    
    def _get_python_type_from_numpy_type(self, numpy_type):
        """
        Return the Python type to use for the values in a numpy container.
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
        
    def _assert_no_nones(self, table_name, column_name, values):
        # TODO: find a faster way to do this check
        pass
#        try:
#            values = values.tolist()
#        except:
#            pass
#        
#        if None in values: 
#            raise ValueError("Nones/NULLs found in table '%s' in column '%s'."
#                % (table_name, column_name))
            
    
from opus_core.tests import opus_unittest


class TestStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = Storage()
        
    def tearDown(self):
        pass
        
    def test__lower_case(self):
        expected = ['foo', 'bar', 'teststring']
        actual = self.storage._lower_case(['foo', 'BAR', 'TestString'])
        self.assertEqual(expected, actual)
        
        expected = 'foo'
        actual = self.storage._lower_case('FOO')
        self.assertEqual(expected, actual)
        
    def test__select_columns_case_sensitive(self):
        requested_columns = ['A', 'b']
        available_columns = ['A', 'b', 'c']
        expected_result = ['A', 'b']
        
        actual_result = self.storage._select_columns(requested_columns, available_columns)
        
        self.assertEqual(expected_result, actual_result)
        
        requested_columns = ['a']
        available_columns = ['A']
        
        self.assertRaises(AttributeError, self.storage._select_columns, requested_columns, available_columns)
        
    def test__select_columns_raise_column_error_case_sensitive(self):
        requested_columns = ['a', 'b']
        available_columns = ['b', 'c']
        
        self.assertRaises(AttributeError, self.storage._select_columns, requested_columns, available_columns)
        
    def test__select_columns_case_insensitive(self):
        requested_columns = ['a', 'B']
        available_columns = ['A', 'b', 'c']
        expected_result = ['a', 'B']
        
        actual_result = self.storage._select_columns(requested_columns, available_columns, case_insensitive=True)
        
        self.assertEqual(expected_result, actual_result)
        
        requested_columns = ['a', 'B']
        available_columns = ['b', 'c']
        
        self.assertRaises(AttributeError, self.storage._select_columns, requested_columns, available_columns, case_insensitive=True)
        
        requested_columns = ['a']
        available_columns = ['a', 'A']
        
        self.assertRaises(AttributeError, self.storage._select_columns, requested_columns, available_columns, case_insensitive=True)
        
class DummyStorage(Storage):
        def get_column_names(self, table_name, lowercase=True):
            if table_name is 'table_doc':
                return ['col1','col2','col3','col4','col5']
            if table_name is 'table_20':
                return range(20)
            if table_name is 'table_3':
                return ['col1','col2','col3']
            return []
        
class TestStorageInterface(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = Storage()
    
    def test_write_table_no_data_to_write(self):
        self.assertRaises(
            ValueError, 
            self.storage.write_table,
            table_name = 'foo',
            table_data = {}, 
            )
    
    def test_write_table_columns_with_different_sizes(self):
        self.assertRaises(
            ValueError, 
            self.storage.write_table,
            table_name = 'foo',
            table_data = {
                'a': array([1]),
                'b': array([1, 2]),
                }, 
            )
        
    def test_chunk_columns_documentation(self):
        storage = DummyStorage()
        expected = [ ['col1','col2'],['col3','col4'],['col5'] ]
        actual = storage.chunk_columns(table_name='table_doc',
                                      column_names=['col1','col2','col3','col4','col5'],
                                      nchunks = 3)
        self.assertEqual(expected, actual)
        
    def test_chunk_columns_20_columns_7_chunks(self):
        storage = DummyStorage()
        expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19]]
        actual = storage.chunk_columns(table_name='table_20',
                                      column_names=Storage.ALL_COLUMNS,
                                      nchunks = 7)
        self.assertEqual(expected, actual)
        
    def test_chunk_columns_empty_column_list(self):
        storage = DummyStorage()
        expected = []
        actual = storage.chunk_columns(table_name='table_empty',
                                      column_names=Storage.ALL_COLUMNS,
                                      nchunks = 7)
        self.assertEqual(expected, actual)
        
    def test_chunk_columns_to_many_chunks(self):
        storage = DummyStorage()
        expected = [ ['col1'],['col2'],['col3'] ]
        actual = storage.chunk_columns(table_name='table_3',
                                      column_names=Storage.ALL_COLUMNS,
                                      nchunks = 5)
        self.assertEqual(expected, actual)
        
# TODO: uncomment this test once have faster way to run the assert.
#    def test_assert_no_nones(self):
#        self.assertRaises(ValueError, self.storage._assert_no_nones, 
#            '', '', array([None]))
#        self.assertRaises(ValueError, self.storage._assert_no_nones, 
#            '', '', array([1,None,3]))
#        
#        self.storage._assert_no_nones('', '', array(['not none']))
#        self.storage._assert_no_nones('', '', array(['None']))
#        self.storage._assert_no_nones('', '', array([-1,0,1,2,3]))
#        self.storage._assert_no_nones('', '', array([False,True]))
    
    
if __name__ == '__main__':
    opus_unittest.main()
