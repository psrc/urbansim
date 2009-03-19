# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
from opus_core.store.storage import Storage
#from opus_core.store.old.dbf_storage import dbf_storage as dbf_storage_old
from opus_core.tests import opus_unittest
from glob import glob


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
        _file_extension = 'dbf'
        
        """
        Class for managing data stored on disk in a DBF format (DBase file).
        """
        def __init__(self, storage_location, digits_to_right_of_decimal=4):
            if self._my_dbf is None:
                raise ImportError('Must install dbfpy before using dbf_storage.\n'
                                  'See http://dbfpy.sourceforge.net/')
            
            self._directory = storage_location
            self._digits_to_right_of_decimal = digits_to_right_of_decimal
        
        def get_storage_location(self):
            return self._directory
            
        def _get_base_directory(self):
            return self._directory
        
        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
            
            """
            The entry 'table_name' is a file name. The first line in the file is considered to 
            contain column names.
            """
            dbf = self._get_dbf_for_table(table_name)
            
            # Get the header information.
            available_column_descriptors = {}
    
            available_column_names = self.get_column_names(
                table_name = table_name,
                lowercase = lowercase
            )
            for field_descriptor in dbf.header.fields:
                column_name = field_descriptor.name
                if lowercase:
                    column_name = column_name.lower()
                available_column_descriptors[column_name] = field_descriptor
               
            # narrow the column names we are interested in based on the column_names parameter    
            column_names = self._select_columns(column_names, available_column_names)
                
            # Create a place to put the row data.
            result = {}
            for column_name in column_names:
                result[column_name] = []
                
            # Get the row data
            for rec in dbf:
                if rec.deleted:
                    continue
                for column_name in column_names:
                    value = rec[column_name]
                    result[column_name].append(value)
            
            # Convert the row data into numpy containers.
            for column_name in column_names:
                dbf_type_code_for_column = available_column_descriptors[column_name].typeCode
                if dbf_type_code_for_column in ('N', 'I', 'F'):
                    result[column_name] = array(result[column_name])
                elif dbf_type_code_for_column in ('L'):
                    result[column_name] = array(result[column_name])     
                elif dbf_type_code_for_column in ('C'):
                    result[column_name] = array(result[column_name])                
                else:
                    msg = ("Unsupported data type '%s' found in DBF file.  We "
                           "support Numeric (N), Integer (I), Float (F), "
                           "Logical (L), and Character (C) types.  "
                           "DBF file is '%s' ") % (
                               field_descriptor.typeCode, 
                               self._get_file_path_for_table(table_name)
                           )
                    raise TypeError(msg)
            
            dbf.close()
            return result
        
        def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
            #TODO: implement Storage.APPEND for dbfstore
            if mode != Storage.OVERWRITE:
                raise 'dbf_storage does not support anything except Storage.OVERWRITE'
            
            if not os.path.exists(self._directory):
                os.makedirs(self._directory)
                
            dbf_file_name = self._get_file_path_for_table(table_name)
            db = _dbf_class(dbf_file_name, new=True)
            number_of_rows, column_names = self._get_column_size_and_names(table_data)
            short_names = self._make_unique_names_list(column_names)
            
            for key in column_names:
                type = self.__NUMPY_TYPES_TO_DBFPY_TYPES[table_data[key].dtype.char]
                
                if type == 'L':
                    db.addField( (short_names[key], type) )
                
                else:
                    if type == 'N':
                        digits = (18, ) ### TODO: Calculate actual digits needed.
                    
                    elif type == 'F':
                        digits = (18, self._digits_to_right_of_decimal) ### TODO: Calculate actual decimal places needed.
                        
                    elif type == 'C':
                        digits = (table_data[key].dtype.itemsize, )
                        
                    db.addField( (short_names[key], type) + digits )
                
            for i in range(number_of_rows):
                rec = db.newRecord()
                
                for key in column_names:
                    if str(table_data[key].dtype.char) == '?': # bool8
                        if table_data[key][i]:
                            rec[short_names[key]] = True
                        else:
                            rec[short_names[key]] = False
                    else:
                        rec[short_names[key]] = table_data[key][i]
                        
                rec.store()
                
            db.close()
            self._short_names = short_names
        
        def get_column_names(self, table_name, lowercase=True):
            dbf = self._get_dbf_for_table(table_name)
            
            available_column_names = []
            for field_descriptor in dbf.header.fields:
                column_name = field_descriptor.name
                
                if lowercase:
                    column_name = column_name.lower()
                    
                available_column_names.append(column_name)
                
            return available_column_names
        
        def get_table_names(self):
            file_names = glob(os.path.join(self._directory, '*.%s' % self._file_extension))
            return [os.path.splitext(os.path.basename(file_name))[0] for file_name in file_names]
    
        def _get_file_path_for_table(self, table_name):
            filename = '%s.%s' % (table_name, self._file_extension)
            return os.path.join(self._directory, filename)
        
        def _get_dbf_for_table(self, table_name):
            file_path = self._get_file_path_for_table(table_name)
    
            if not os.path.exists(file_path):
                raise NameError("DBF file could not be found.  Path = %s." 
                    % file_path)
            
            return self._my_dbf(file_path, readOnly=True)
        
        def _make_unique_names_list(self, list, length=10):
            """
            this method takes a list of strings and a length and returns a dict
            with all strings of the list as keys and a unique name for each key
            which has a maximum of 'length' characters
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
        
        __NUMPY_TYPES_TO_DBFPY_TYPES = {
        '?': 'L',
        'b': 'N',
        'h': 'N',
        'i': 'N',
        'l': 'N',
        'q': 'N',
        'p': 'N',
        'B': 'N',
        'H': 'N',
        'I': 'N',
        'L': 'N',
        'Q': 'N',
        'P': 'N',
        'f': 'F',
        'd': 'F',
        'g': 'F',
        'S': 'C',
        'U': 'C',
        }
    
        

    import tempfile
    from shutil import rmtree    
        
    from numpy import array
    
    from opus_core.opus_package import OpusPackage
    from opus_core.store.storage import TestStorageInterface
    
    
    class DbfStorageTests(opus_unittest.OpusTestCase):
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
                    
        def test_small_load_dataset(self):
            actual = self.storage.load_table(table_name='test_small')
            expected = {'id':array([1])}
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
                         
        def test_medium_load_dataset(self):
            actual = self.storage.load_table(table_name='test_medium')
            expected = {'keyid':array([1,2]),'dummyint':array([2,3]), 'dummyfloat':array([2.2,3.3])}
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionaries not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
            
        def test_medium_strings_load_dataset(self):
            actual = self.storage.load_table(table_name='test_medium_strings')
            expected = {}
            expected['keyid'] = array([2,1])
            expected['dummystr'] = array(["Two", "One"])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
            
        def test_column_names_parameter_for_medium_strings_load_dataset(self):
            actual = self.storage.load_table(
                table_name = 'test_medium_strings',
                column_names = Storage.ALL_COLUMNS,
                )
            expected = {}
            expected['keyid'] = array([2,1])
            expected['dummystr'] = array(["Two", "One"])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
            
            actual = self.storage.load_table(
                table_name = 'test_medium_strings', 
                column_names = ['dummystr'],
                )
            expected = {}
            expected['dummystr'] = array(["Two", "One"])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
    
            actual = self.storage.load_table(
                table_name = 'test_medium_strings', 
                column_names = ['keyid'],
                )
            expected = {}
            expected['keyid'] = array([2,1])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n'
                                  'actual=   %s  \n expected= %s' %(actual,expected))
    
        def test_medium_strings_with_deleted_record(self):
            actual = self.storage.load_table(
                table_name = 'test_medium_strings_with_deleted_record',
                )
            expected = {}
            expected['keyid'] = array([2,1])
            expected['dummystr'] = array(["Two", "One"])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n actual=   %s  \n'
                                  'expected= %s' %(actual,expected))
            
        def test_logical_values_including_not_initialized(self):
            actual = self.storage.load_table(table_name='test_logical')
            expected = {}
            expected['keyid'] = array([1,2,3,4,5])
            expected['works'] = array([True,True,-1,False,False])
            self.assertDictsEqual(actual, expected, msg='expected and actual dictionarys not equal! \n actual=   %s  \n'
                                  'expected= %s' %(actual,expected))
    
        def test_get_column_names(self):
            expected = ['keyid', 'works']
            actual = self.storage.get_column_names(table_name='test_logical')
            
            self.assertEqual(expected, actual)
            
            self.assertRaises(NameError, self.storage.get_column_names, table_name='idonotexist')
            
            
    class DbfStorageWriteTests(TestStorageInterface):
        def setUp(self):
            self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_dbf_storage_tests')
            self.storage = dbf_storage(self.temp_dir)
            self.out_table_name = 'test_write'
            
        def tearDown(self):
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)
            
        def helper_write_table(self, values, expected=None):
            self.storage.write_table(table_name=self.out_table_name,
                                        table_data=values)
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
            
        def test_write_table_one_column_one_numeric_value(self):
            values = {
                'a': array([1]),
                }
            self.helper_write_table(values)
            
        def test_write_table_one_column_multiple_rows(self):
            values = {
                'a': array([2, 4]),
                }
            self.helper_write_table(values)
            
        def test_write_table_different_column_name(self):
            values = {
                'b': array([2, 4]),
                }
            self.helper_write_table(values)
            
        def test_write_table_two_columns(self):
            values = {    
                'a': array([1, 3]),
                'b': array([2, 4]),
                }
            self.helper_write_table(values)
            
        def test_write_table_big_numeric_value(self):
            values = {
                'a': array([999999999999999]),
                }
            self.helper_write_table(values)
            
        def test_write_table_float_value(self):
            values = {
                'a': array([11.1236]),
                }
            self.helper_write_table(values)
            
        def test_write_table_string_value(self):
            values = {
                'a': array(['foobar']),
                }
            self.helper_write_table(values)
            
        def test_write_table_big_string_value(self):
            values = {
                'a': array(['a'*255]),
                }
            self.helper_write_table(values)
            
        def test_write_table_logical_value(self):
            values = {
                'a': array([True, False, False, True]),
                }
            self.helper_write_table(values)
            
        def test_write_table_column_with_more_than_10_characters(self):
            values = {
                'morethantencharacters': array([1]),
                }
            expected = {
                'morethante': array([1]),
                }
            self.helper_write_table(values, expected)
            
        def test_write_table_float_to_configurable_fixed_point(self):
            
            def helper_test_float_type(expected):
                db = _dbf_class(self.storage._get_file_path_for_table(self.out_table_name))
                for name, type, length, decimalcount in [field.fieldInfo() for field in db.header.fields]:
                    self.assertEqual('FLOAT', name)
                    self.assertEqual('F', type)
                    self.assertEqual(18, length)
                    self.assertEqual(expected, decimalcount)
                db.close()
            
            values = {
                'float': array([1.23456789]),
                }
            
            self.storage.write_table(table_name=self.out_table_name,
                                        table_data=values)
            helper_test_float_type(4)
            
            self.storage = dbf_storage(self.temp_dir, digits_to_right_of_decimal=7)
            self.storage.write_table(table_name=self.out_table_name, 
                                        table_data=values)
            helper_test_float_type(7)
            
            
    class DbfStorageMakeUniqueShortNamesTests(opus_unittest.OpusTestCase):
        
        def setUp(self):
            opus_core_path = OpusPackage().get_opus_core_path()
            self.local_test_data_path = os.path.join(
                opus_core_path, 'tests', 'data', 'dbf')
            self.storage = dbf_storage(self.local_test_data_path)
            
        def tearDown(self):
            del self.storage
            
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

            
    class TestDbfStorageGetTableNames(opus_unittest.OpusTestCase):
        def setUp(self):
            self.temp_dir = tempfile.mkdtemp(prefix='opus_core_test_dbf_storage_get_table_names')
            self.storage = dbf_storage(storage_location = self.temp_dir)
            
        def tearDown(self):
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)
                
        def test_get_table_names_one_table(self):
            open(os.path.join(self.temp_dir, 'city_name.dbf'), 'w').close()
            expected = ['city_name']
            actual = self.storage.get_table_names()
            self.assertEquals(expected, actual)
            
        def test_get_table_names_two_table(self):
            open(os.path.join(self.temp_dir, 'city_name.dbf'), 'w').close()
            open(os.path.join(self.temp_dir, 'year.dbf'), 'w').close()
            expected = ['city_name', 'year']
            expected.sort()
            actual = self.storage.get_table_names()
            actual.sort()
            self.assertEquals(expected, actual)
            
if __name__ == '__main__':
    opus_unittest.main()  