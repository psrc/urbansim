# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array
#from opus_core.store.old.storage import Storage as Storage_old

class Storage:
    ALL_COLUMNS = '*'
    OVERWRITE = 'o'
    APPEND = 'a'
    
    
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
    def load_table(self, table_name, column_names=ALL_COLUMNS, lowercase=True):
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
    def write_table(self, table_name, table_data, mode = OVERWRITE):
        """
        Writes the given table to storage with the given name. The table_data
        parameter takes a dictionary with the column data. Mode determines what 
        how the table_data will interact with data already written to the same
        storage location. 
        
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

    #TODO: be more principled here...
    def table_exists(self, table_name):
        try:
            self.get_column_names(table_name)
        except:
            return False
        return True
        
    # _determine_field_names
    def get_column_names(self, table_name, lowercase=True):
        """
        Returns a list of the columns in the given table.
        """
        raise NotImplementedError()
    
    def _get_column_size_and_names(self, table_data):
        column_names = list(table_data.keys())
        # Check that every column has the same number of items
        column_size = None
        for column_name in column_names:
            next_column_size = table_data[column_name].size
            if column_size is None:
                column_size = next_column_size
            
            if not next_column_size == column_size:
                raise ValueError('Data in each column must be of the same length: %s(%s)!=%s' % (next_column_size, column_name, column_size))
            
        
        if column_size is None:
            raise ValueError('No data to write!')
        
        return column_size, column_names
    
    def _lower_case(self, string_or_list_of_strings):
        """
        Returns a new string or a new list of strings matching the original, 
        save that the string or each string in the list is now lowercase.
        """
        if isinstance(string_or_list_of_strings, str):
            result = string_or_list_of_strings.lower()
        else:
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
                available_columns_lower = list(set([
                    each_column.lower() 
                    for each_column in available_columns
                    ]))
                if len(available_columns)!=len(available_columns_lower):
                    raise AttributeError("List of available columns "
                        "contains duplicate case-insensitive entries.")
                    
                available_columns = available_columns_lower
                
            for column_name in requested_columns:
                if case_insensitive:
                    test_column_name = column_name.lower()
                else:
                    test_column_name = column_name
                    
                if test_column_name not in available_columns:
                    raise AttributeError("Requested column '%s' is not an "
                        "available column. Requested columns: %s. Available columns: %s"
                            % (column_name, requested_columns, available_columns))
            
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
        'int64': int,
        'uint64': int,
        'float32': float,
        'float64': float,
        'complex64': complex,
        'complex128': complex,
        }
    
    def _get_numpy_type_from_python_type(self, python_type):
        return self.__PYTHON_TYPE_TO_NUMPY_TYPE_MAP[python_type]
    
    __PYTHON_TYPE_TO_NUMPY_TYPE_MAP = {
        int: 'int32',
        int: 'int64',
        float: 'float32',
        str: 'a255',
        str: 'a255',
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
