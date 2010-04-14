# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import shutil
from glob import glob
import numpy
from opus_core.logger import logger
from opus_core.store.storage import Storage
from opus_core.misc import is_file_in_directory
        
class file_flt_storage(Storage): 
    
    #there are weird issues with how this was ported over from the old storage classes
    
    class storage_file(object):
        def __init__(self, name):
            self._name = name
            
        def get_name(self):
            return self._name
        
        def get_type(self):
            extension_position = self._name.rfind('.')+1
            byteorder_symbol = self._name[extension_position:extension_position+1]
            type = self._map_extension_character_to_byteorder_symbol(byteorder_symbol)
            if type is None:
                return None
            type =  type + self._name[extension_position+1:]
            return type.encode()
        
        def get_short_name(self):
            type = self.get_type()
            if type is None:
                return os.path.basename(self._name)
            return os.path.basename(self._name)[:-len(type)-1]
        
        @classmethod
        def new_storage_file(cls, short_name, type, path):
            byteorder_symbol = type[0:1]
            byteorder_extension = cls._map_byteorder_symbol_to_extension_character(byteorder_symbol)
            extension = byteorder_extension + type[1:]
            name = '%s.%s' % (os.path.join(path, short_name), extension)
            return cls(name)
        
        @classmethod
        def _map_byteorder_symbol_to_extension_character(cls, byteorder_character):
            map = {
                '<': 'l', # little-endian
                '>': 'b', # big-endian
                '|': 'i', # irrelevant
                }
            if array([1], dtype='<i4').dtype.byteorder == '=':
                map['='] = map['<']
            else:
                map['='] = map['>']
            
            return map[byteorder_character]
        
        #_map_byteorder_symbol_to_extension_character = classmethod(_map_byteorder_symbol_to_extension_character)
                
        def _map_extension_character_to_byteorder_symbol(self, extension_character):
            try:
                return {
                    'l': '<', # little-endian
                    'b': '>', # big-endian
                    'i': '|', # irrelevant
                    }[extension_character]
            except:
                return None
                    
        def _extension_for_numpy_type(self, dtype):
            """Returns the file extension for this numpy type."""    
            str = dtype.str
            return self._map_byteorder_symbol_to_extension_character(str[0]) + str[1:]
                
    
        def _get_native_endian_file_extension_character(self):
            if array([1], dtype='<i4').dtype.byteorder == '=':
                return self._map_byteorder_symbol_to_extension_character('<')
            else:
                return self._map_byteorder_symbol_to_extension_character('>')

        def _write_to_file(self, directory, attribute_name, attribute_data):
            """Writes data to a file."""
            extension = self._extension_for_numpy_type(attribute_data.dtype)
            filename = '%s.%s' % (attribute_name, extension)
        
            file_path = os.path.join(directory, filename)
        
            f = file(file_path, mode="wb")
            try:
                try:
                    attribute_data.tofile(f)
                
                except ValueError:
                    logger.log_error(
                        "Unable to write attribute '%s' to disk. The disk may be "
                        "full or the location write-protected. (%s)"
                            % (attribute_name, file_path))
                    raise
                
            finally:
                f.close()
    
    def __init__(self, storage_location):
        self._base_directory = storage_location

        
    """@classmethod
    def _map_byteorder_symbol_to_extension_character(cls, byteorder_character):
        map = {
            '<': 'l', # little-endian
            '>': 'b', # big-endian
            '|': 'i', # irrelevant
            }
        if array([1], dtype='<i4').dtype.byteorder == '=':
            map['='] = map['<']
        else:
            map['='] = map['>']
            
        return map[byteorder_character]"""

    def has_table(self, table):
        return is_file_in_directory(table, self._get_base_directory())
        

        
    def get_storage_location(self):
        return self._base_directory

    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        files = self._get_files(table_name=table_name)
        
        result = {}
        
        for file in files:
            if lowercase:
                column_name = file.get_short_name().lower()
            else:
                column_name = file.get_short_name()
                
            if column_names == Storage.ALL_COLUMNS or column_name in column_names:
                result[column_name] = numpy.fromfile(file.get_name(), dtype=file.get_type())
        
        return result
    
    def get_column_names(self, table_name, lowercase=True):
        files = self._get_files(table_name)
        
        result = [file.get_short_name() for file in files]
        if lowercase:
            result = [file.lower() for file in result]

        return result
    
    def _get_base_directory(self):
        return self._base_directory
    
    def get_table_names(self):
        dataset_path = self._get_base_directory()
        if os.path.exists(dataset_path):
            file_names = glob(os.path.join(dataset_path, '*'))
            return [os.path.basename(name) for name in file_names 
                    if os.path.isdir(name) and len(self.get_column_names(name))>0]
            
        else:
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
    
    def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
        """
        'table_name' specifies the subdirectory relative to base directory. 
        'table_data' is a dictionary where keys are the column names and values 
            are value arrays of the corresponding columns. 
        """
        dir = os.path.join(self._get_base_directory(), table_name)
        
        if not os.path.exists(dir):
            logger.log_status("%s doesn't exist and is created" % dir)
            os.makedirs(dir)
            
        unused_column_size, column_names = self._get_column_size_and_names(table_data)

        for column_name in column_names:
            col_type = table_data[column_name].dtype.str
                    
            column_file = self.storage_file.new_storage_file(column_name, col_type, dir)
            
            existing_files_of_this_name = glob(os.path.join(dir, '%s.*' % column_name))

            if (len (existing_files_of_this_name) > 1):
                message = "Column '%s' has multiple files with different file extensions:\n" % column_name
                for existing_file_name in existing_files_of_this_name:
                    message += existing_file_name + "\n"
                message += "Either the process of copying files into this directory is flawed, or there is a bug in Opus."
                raise FltError(message)   
            
            if mode == Storage.OVERWRITE:
                for existing_file_name in existing_files_of_this_name:
                    os.remove(existing_file_name)            
            
            if mode == Storage.OVERWRITE or len(existing_files_of_this_name) == 0:
                table_data[column_name].tofile(column_file.get_name())
    
#    def _get_base_directory(self):
#        return self._base_directory
    
    def delete_table(self, table_name):
        dir = os.path.join(self._get_base_directory(), table_name)
        if os.path.exists(dir):
            shutil.rmtree(dir)
            logger.log_status("Table %s successfully deleted." % dir)
            return True
        return False
            
    def _get_files(self, table_name=''):
        dataset_path = os.path.join(self._get_base_directory(), table_name)
        if os.path.exists(dataset_path):
            file_names = glob(os.path.join(dataset_path, '*.*'))
            return [self.storage_file(name) for name in file_names]
            
        else:
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
        
    def listdir_in_base_directory(self):
        return os.listdir( self._get_base_directory() )
        
        

class FltError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.value

import sys
from opus_core.tests import opus_unittest
from opus_core.opus_package import OpusPackage
from opus_core.store.storage import TestStorageInterface
from opus_core.tests.utils.cache_extension_replacements import replacements
from numpy import array, fromfile, int32
from shutil import rmtree
from tempfile import mkdtemp

class StorageFileTests(opus_unittest.OpusTestCase):
    
    def test_get_short_name(self):
        storage_file = file_flt_storage.storage_file('path/to/table/test.li4')
        self.assertEqual('<i4', storage_file.get_type())
        self.assertEqual('test', storage_file.get_short_name())
        
        storage_file = file_flt_storage.storage_file('path/to/table/foo.iS11')
        self.assertEqual('|S11', storage_file.get_type())
        self.assertEqual('foo', storage_file.get_short_name())
        
    def test_new_storage_file(self):
        storage_file = file_flt_storage.storage_file.new_storage_file('test', '<i4', 'path/to/table')
        self.assertEqual('test', storage_file.get_short_name())
        self.assertEqual('<i4', storage_file.get_type())
        expected = os.path.join('path/to/table', 'test.li4')
        self.assertEqual(expected, storage_file.get_name())
        
    def test_get_type_from_unicode_filename(self):
        storage_file = file_flt_storage.storage_file(u'path/to/table/test.li4')
        self.assertEquals('<i4', storage_file.get_type())
        self.assertEquals(type('<i4'), type(storage_file.get_type()))
        
class StorageTests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        opus_core_path = OpusPackage().get_opus_core_path()
        local_test_data_path = os.path.join(
            opus_core_path, 'data', 'test_cache', '1980')
        self.storage = file_flt_storage(local_test_data_path)
    
    def test_get_files(self):
        expected = ['city_id', 'city_name']
        expected.sort()
        actual = self.storage.get_column_names('cities')
        actual.sort()
        self.assertEqual(expected, actual)
        
    def test_load_table(self):
        expected = {
            'city_id': array([3, 1, 2], dtype='<i4'),
            'city_name': array(['Unknown', 'Eugene', 'Springfield']),
            }
        actual = self.storage.load_table('cities')
        self.assertDictsEqual(expected, actual)
        
    def test_get_table_names_1981(self):
        opus_core_path = OpusPackage().get_opus_core_path()
        local_test_data_path = os.path.join(
            opus_core_path, 'data', 'test_cache', '1981')
        storage = file_flt_storage(local_test_data_path)
        expected = ['base_year', 'cities']
        actual = storage.get_table_names()
        expected.sort()
        actual.sort()
        self.assertEquals(expected, actual)
        
class StorageWriteTests(TestStorageInterface):
    
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_flt_storage')
        self.storage = file_flt_storage(self.temp_dir)
        self.table_name = 'testtable'
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_write_char_array(self):
        expected = array(['string1', 'string227'])
        table_data = {
            'char_column': expected,
            }
        file_name = os.path.join(self.temp_dir, self.table_name, 'char_column.iS9')
        
        self.storage.write_table(self.table_name, table_data)
        self.assert_(os.path.exists(file_name))
        actual = numpy.fromfile(file_name, dtype='|S9')
        self.assert_((expected==actual).all())
        
    def test_write_int_array(self):
        expected = array([100, 70])
        table_data = {
            'int_column': expected,
            }
        # file_name is e.g. 'int_column.li4' for a little-endian 32 bit machine
        file_name = 'int_column.%(endian)si%(bytes)u' % replacements
        # numpy_dtype is e.g. '<i4' for a little-endian 32 bit machine
        numpy_dtype = '%(numpy_endian)si%(bytes)u' % replacements
        file_path = os.path.join(self.temp_dir, self.table_name, file_name)
        self.storage.write_table(self.table_name, table_data)
        self.assert_(os.path.exists(file_path))
        actual = numpy.fromfile(file_path, dtype=numpy_dtype)
        self.assert_((expected==actual).all())
        
    def test_write_float_and_boolean_array(self):
        expected_float = array([100.17, 70.00])
        expected_bool = array([True, False])
        table_data = {
            'float_column': expected_float,
            'bool_column': expected_bool,
            }
        if sys.byteorder=='little':
            file_name = 'float_column.lf8'
            numpy_ext = '<f8'
        else:
            file_name = 'float_column.bf8'
            numpy_ext = '>f8'
        file_path = os.path.join(self.temp_dir, self.table_name, file_name)
        self.storage.write_table(self.table_name, table_data)
        self.assert_(os.path.exists(file_path))
        actual = fromfile(file_path, numpy_ext)
        self.assert_((expected_float == actual).all())
        file_path = os.path.join(self.temp_dir, self.table_name, 'bool_column.ib1')
        self.storage.write_table(self.table_name, table_data)
        self.assert_(os.path.exists(file_path))
        actual = fromfile(file_path, '|b1')
        self.assert_((expected_bool == actual).all())
        
    def test_writing_column_to_file_when_file_of_same_column_name_and_different_type_already_exists(self):
        
        column_name= "some_column"
        os.mkdir(os.path.join(self.temp_dir, self.table_name)) 
        existing_file = file(os.path.join(self.temp_dir , self.table_name, column_name + ".li4"), "w")
        existing_file.close()
        storage = file_flt_storage(storage_location=self.temp_dir)
        # Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        
        storage.write_table(table_name=self.table_name, table_data=my_data)
        self.assert_(not (os.path.exists(existing_file.name)))
        self.assert_(os.path.exists(os.path.join(self.temp_dir, self.table_name, column_name + ".li8")))




    def test_writing_column_to_file_when_two_files_of_same_column_name_and_different_type_already_exist(self):        

        column_name= "some_column"
        os.mkdir(os.path.join(self.temp_dir, self.table_name)) 
        existing_file_1 = file(os.path.join(self.temp_dir , self.table_name, column_name + ".li4"), "w")
        existing_file_1.close()
        existing_file_2 = file(os.path.join(self.temp_dir , self.table_name, column_name + ".bi4"), "w")
        existing_file_2.close()           
        storage = file_flt_storage(storage_location=self.temp_dir)
        # Test writing 
        my_data = { column_name: array([9,99,999], dtype='<i8') }
        self.assertRaises(FltError, storage.write_table, self.table_name, my_data)
        self.assert_(not (os.path.exists(os.path.join(self.temp_dir, self.table_name, column_name + ".li8"))))        
        
        

if __name__ == '__main__':
    opus_unittest.main()