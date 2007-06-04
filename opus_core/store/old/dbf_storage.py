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
from opus_core.store.old.storage import Storage
from opus_core.tests import opus_unittest


try:
    from dbfpy.dbf import Dbf as _dbf_class
    
except:
    # If dbfpy is not installed, provide a dbf_storage class
    # that will raise a useful exception if someone tries to 
    # create an instance of this class.
    class dbf_storage(Storage):
        def __init__(self, *args, **kwargs):
            raise ImportError('Must install Python module dbfpy to use '
                              'dbf_storage; See http://dbfpy.sourceforge.net/.')
    
    class DbfStorageTests(opus_unittest.OpusTestCase):
        def test(self):
            self.assertRaises(ImportError, dbf_storage)
            
else:
    # This is the normal case where dbfpy is installed.
    # The dbf_storage class defined here is the one that works with dbfpy.
    import os
    
    class dbf_storage(Storage): 
        
        # hook for unit tests
        _my_dbf = _dbf_class
        _short_names = None
        
        """
        Class for managing data stored on disk in a DBF format (DBase file).
        """
        def __init__(self, storage_location, digits_to_right_of_decimal=3):
            if self._my_dbf is None:
                raise ImportError('Must install dbfpy before using dbf_storage.\n'
                                  'See http://dbfpy.sourceforge.net/')
            
            self._directory = storage_location
            self._field_info_for_tables = {}
            self._digits_to_right_of_decimal = digits_to_right_of_decimal
            
        def set_field_info_for_table(self, table_name, field_info):
            """
            field_info is a dictionary whose key is column name, and
            whose value is the field information for that column.
            The schema of the field information depends upon the type
            of column.
            
            The field information is based upon 
            http://www.clicketyclick.dk/databases/xbase/format/data_types.html#DATA_TYPES
            
            For instance, a table with three columns 'a_number', 'a_string', and 'a_bool'
            field_info could have the field_info:
            
                {
                    'a_number':{
                        'type':'numeric',
                        'length':11,
                        'decimals':3,
                    },
                    'a_string':{
                        'type':'string',
                        'length':120,
                    },
                    'a_bool':{
                        'type':'bool',
                        'encoding':'YN',
                    }
                }
            
            'type' may be 'numeric', 'string', or 'bool'.
            For numeric, 'length' includes decimal point and must be < 18 (or 20 for FoxPro or Clipper).
            For string, 'length' must be < 254.
            For bool, 'encoding' specifies characters written for True/False; may be one 
            of 'YN','yn','TF',or 'tf'
            """
            self._field_info_for_tables[table_name] = field_info
            
        def _get_base_directory(self):
            return self._directory
        
        def write_dataset(self, write_resources):
            out_table_name = write_resources['out_table_name']
            values = write_resources['values']
        
            self._write_dataset(
                out_table_name=out_table_name,
                values=values,
                )
        
        def _write_dataset(self, out_table_name, values):
            dbf_file_name = self._get_file_path_for_table(out_table_name)
            db = _dbf_class(dbf_file_name, new=True)
            try:
                short_names = self._make_unique_names_list(values.keys())
                for attribute_name in values:
                    type_tuple = self._get_dbf_type_tuple_for_numpy_array(values[attribute_name])
                    db.addField((short_names[attribute_name], ) + type_tuple)
                    
                length = max([len(values[key]) for key in values.keys()])
                
                # Write each complete rows at a time
                for i in range(length):
                    row = db.newRecord()
                    for attribute_name in values:
                        value = values[attribute_name][i]
                        
                        # The following code is to work around a bug in numpy/dbfpy.
                        # For some reason, we can get boolean values of type 'boolscalar'
                        # which will not correctly compare "x is True" when x = True.
                        # It does work, however, if we replace the 'boolscalar' values
                        # with plain-old-python bool values.
                        if values[attribute_name].dtype.kind == 'b':
                            if value:
                                row[short_names[attribute_name]] = True
                            else:
                                row[short_names[attribute_name]] = False
                        else:
                            row[short_names[attribute_name]] = values[attribute_name][i]
                    row.store()
            finally:
                db.close()
                
            self._short_names = short_names
        
        def determine_field_names(self, load_resources):
            in_table_name = load_resources['in_table_name']
            lowercase = load_resources.get('lowercase', True)
            
            return self._determine_field_names(
                in_table_name = in_table_name,
                lowercase = lowercase,
                )
        
        def _determine_field_names(self, in_table_name, lowercase=True):
            dbf = self._get_dbf_for_table(in_table_name)
            
            available_column_names = []
            for field_descriptor in dbf.header.fields:
                column_name = field_descriptor.name
                
                if lowercase:
                    column_name = column_name.lower()
                    
                available_column_names.append(column_name)
                
            return available_column_names
    
        def _get_file_path_for_table(self, table_name):
            filename = '%s.dbf' % (table_name)
            return os.path.join(self._directory, filename)
        
        def _get_dbf_for_table(self, table_name):
            file_path = self._get_file_path_for_table(table_name)
    
            if not os.path.exists(file_path):
                raise NameError("DBF file could not be found.  Path = %s." 
                    % file_path)
            
            return self._my_dbf(file_path, readOnly=True)
        
        def _make_unique_names_list(self, list, length=10):
            """
            This method takes a list of strings and a length and returns a dict
            with all strings of the list as keys and a unique name for each key
            which has a maximum of 'length' characters.
            
            This is used to make sure that the column names are short enough 
            and unique, for instance.
            """
            result = {}
            temp = []
            for name in list:
                short_name = name[:length]
                new_name = short_name
                i = 1
                while new_name in temp:
                    extension = '(%i)' % i
                    new_name = short_name[:length-len(extension)] + extension
                    i = i + 1
                temp.append(new_name)
                result[name] = new_name
                    
            return result
        
        def _get_dbf_type_tuple_for_numpy_array(self, an_array):
            """Returns the dbf type information for this array.
            Dbf type is of form (type_char, length)
            where type_char is one:
                'N' for numbers
                'F' for fixed point numbers
                'L' for boolean
                'C' for characters
            """
            kind = an_array.dtype.kind
            if kind == 'i':
                return ('N', 18)
            elif kind == 'f':
                return ('F', 18, self._digits_to_right_of_decimal + 1)
            elif kind == 'b':
                return ('L', )
            elif kind == 'S':
                return ('C', an_array.dtype.itemsize)
            else:
                raise TypeError("Numpy array of type '%s' has no corresponding dbf type." % an_array.dtype)
    
        

    from shutil import rmtree
    from tempfile import mkdtemp

    from numpy import array
    
    from opus_core.opus_package import OpusPackage
    from opus_core.resources import Resources
    
    
    class DbfStorageLoadTests(opus_unittest.OpusTestCase):
        def setUp(self):
            opus_core_path = OpusPackage().get_opus_core_path()
            self.local_test_data_path = os.path.join(
                opus_core_path, 'tests', 'data', 'dbf')
            self.storage = dbf_storage(self.local_test_data_path)
            
        def tearDown(self):
            del self.storage
            
        def test_new_equality_method(self):
            self.assertDictsEqual({},{})
            self.assertDictsEqual({'a':1,'b':2},{'a':1,'b':2})
            self.assertDictsNotEqual({'a':1,'b':2},{'a':1,'b':4})
            self.assertDictsNotEqual({'a':1},{'a':1,'b':2})     
            self.assertDictsNotEqual({'a':1,'b':2},{'a':1})  
                    
        def test_determine_field_names(self):
            expected = ['keyid', 'works']
            actual = self.storage.determine_field_names(Resources({
                'in_table_name': 'test_logical',
                }))
            self.assertEqual(expected, actual)
            
            self.assertRaises(
                NameError, 
                self.storage.determine_field_names, 
                Resources({
                    'in_table_name': 'idonotexist',
                    })
                )
            
    class DbfStorageWriteTests(opus_unittest.OpusTestCase):
        def setUp(self):
            self.temp_dir = mkdtemp(prefix='opus_core_test_dbf_storage')
            self.storage = dbf_storage(self.temp_dir)
            self.out_table_name = 'test_write'
            
        def tearDown(self):
            del self.storage
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)
            
        def helper__write_dataset(self, values, expected=None):
            self.storage._write_dataset(out_table_name=self.out_table_name,
                                        values=values)
            self.helper_test_dbf_file(values, expected)
            
        def helper_test_dbf_file(self, values, expected=None):
            if expected == None:
                expected = values
            db = _dbf_class(self.storage._get_file_path_for_table(self.out_table_name))
            length = max([len(values[key]) for key in values.keys()])
            i = 0
            field_type = {}
            for name, type in [field.fieldInfo()[:2] for field in db.header.fields]:
                field_type[name] = type
            for rec in db:
                for key in expected.keys():
                    if field_type[key.upper()] is 'F':
                        self.assertAlmostEqual(expected[key][i], rec[key])
                    else:
                        self.assertEqual(expected[key][i], rec[key])
                i = i + 1
            self.assertEquals(length, i, msg="More values expected than the dbf file contains")
            db.close()
            
        def test__write_dataset_one_attribute_one_numeric_value(self):
            values = {
                'a': array([1]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_one_attribute_multiple_rows(self):
            values = {
                'a': array([2, 4]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_different_attribute_name(self):
            values = {
                'b': array([2, 4]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_two_attributes(self):
            values = {    
                'a': array([1, 3]),
                'b': array([2, 4]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_big_numeric_value(self):
            values = {
                'a': array([999999999999999]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_float_value(self):
            values = {
                'a': array([11.1236]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_string_value(self):
            values = {
                'a': array(['foobar']),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_big_string_value(self):
            values = {
                'a': array(['a'*255]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_logical_value(self):
            values = {
                'a': array([True, False, False, True]),
                }
            self.helper__write_dataset(values)
            
        def test__write_dataset_attribute_with_more_than_10_characters(self):
            values = {
                'morethantencharacters': array([1]),
                }
            expected = {
                'morethante': array([1]),
                }
            self.helper__write_dataset(values, expected)
            
        def test__write_dataset_float_to_configurable_fixed_point(self):
            
            def helper_test_float_type(expected):
                db = _dbf_class(self.storage._get_file_path_for_table(self.out_table_name))
                for name, type, length, digits_to_right_of_decimal_including_period in [field.fieldInfo() for field in db.header.fields]:
                    self.assertEqual('FLOAT', name)
                    self.assertEqual('F', type)
                    self.assertEqual(18, length)
                    self.assertEqual(expected, digits_to_right_of_decimal_including_period)
                db.close()
            
            values = {
                'float': array([1.23456789]),
                }
            
            self.storage._write_dataset(out_table_name=self.out_table_name,
                                        values=values)
            helper_test_float_type(4)
            
            self.storage = dbf_storage(self.temp_dir, digits_to_right_of_decimal=6)
            self.storage._write_dataset(out_table_name=self.out_table_name, 
                                        values=values)
            helper_test_float_type(7)
            
        def test_write_dataset(self):
            values = {
                'a': array(['foobar', 'x', 'y', 'z']), 
                'b': array([5, 6, 7, 8]), 
                'c': array([True, False, False, True]), 
                }
            self.storage.write_dataset(Resources({
                'out_table_name': self.out_table_name,
                'values': values
                }))
            self.helper_test_dbf_file(values)
            
        def test_write_dataset_return_dict_with_short_names(self):
            values = {
                '1234567890abc': array([1]),
                '1234567890def': array([1]),
                }
            expected = {
                '1234567890abc':'1234567890',
                '1234567890def':'1234567(1)',
                }
            self.assertEqual(None, self.storage._short_names)
            self.storage.write_dataset(Resources({
                'out_table_name': self.out_table_name,
                'values': values
                }))
            actual = self.storage._short_names
            self.assertDictsEqual(expected, actual)
            
    class DbfStorageMakeUniqueShortNamesTests(opus_unittest.OpusTestCase):
        
        def setUp(self):
            self.temp_dir = mkdtemp(prefix='opus_core_test_dbf_storage')
            self.storage = dbf_storage(self.temp_dir)
            
        def tearDown(self):
            del self.storage
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)
            
        def test__make_short_names_list(self):
            values = ['1234567890abcdefg']
            expected = {'1234567890abcdefg':'1234567890'}
            actual = self.storage._make_unique_names_list(values, 10)
            self.assertEqual(expected, actual)
            
            values = ['1234567890abcdefg']
            expected = {'1234567890abcdefg':'12345'}
            actual = self.storage._make_unique_names_list(values, 5)
            self.assertEqual(expected, actual)
            
        def test__make_unique_short_names_list(self):
            values = ['1234567890abcdefg', '1234567890ytfytf']
            expected = {
                '1234567890abcdefg':'1234567890', 
                '1234567890ytfytf':'1234567(1)', 
                }
            actual = self.storage._make_unique_names_list(values)
            self.assertEqual(expected, actual)
            
    class DbfStoragePlainTests(opus_unittest.OpusTestCase):
        def test__get_dbf_type_tuple_for_numpy_array(self):
            digits_to_right_of_decimal = 5
            storage = dbf_storage(storage_location='', digits_to_right_of_decimal=digits_to_right_of_decimal)
            
            data = [
                (array([1]), ('N', 18)),
                (array([1.1]), ('F', 18, 6)),
                (array([True]), ('L', )),
                (array(['a']), ('C', 1)),
                (array(['a','abc']), ('C', 3)),
                ]
            
            for an_array, expected_dbf_type in data:
                dbf_type_tuple = storage._get_dbf_type_tuple_for_numpy_array(an_array)
                self.assertEqual(expected_dbf_type, dbf_type_tuple)
                
            self.assertRaises(TypeError,
                              storage._get_dbf_type_tuple_for_numpy_array,
                              array([1+2j]),
                          )
            

if __name__ == '__main__':
    opus_unittest.main()  