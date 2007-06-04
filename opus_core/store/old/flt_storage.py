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

from glob import glob

import numpy

from opus_core.logger import logger
from opus_core.store.old.storage import Storage
from opus_core.misc import is_file_in_directory
from opus_core.variables.attribute_type import AttributeType

        
class flt_storage(Storage): 
    DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES = 'computed'
    
    def __init__(self, storage_location):
        self._base_directory = storage_location

    def determine_field_names(self, load_resources, attributes=None):
        in_table_name = load_resources.get('in_table_name', '')
        lowercase = load_resources.get('lowercase', False)

        if attributes is None:
            attributes = load_resources.get('attributes', '*')
            
        return self._determine_field_names(in_table_name=in_table_name, 
            attributes=attributes, lowercase=lowercase)
    
    def _determine_field_names(self, in_table_name='', attributes='*', lowercase=True):
        file_paths = self._get_file_paths_for_stored_attributes(in_table_name)
        
        vars = []
        for file_path in file_paths:
            shortname, attribute_type = self._determine_file_short_name_and_attribute_type(file_path, lowercase)
            vars.append( (shortname, attribute_type) )

        return self.filter_attributes(attribute_names_and_types=vars, filter=attributes)
    
    def write_dataset(self, write_resources):
        if 'values' not in write_resources:
            return

        out_table_name = write_resources.get('out_table_name', '')
        valuetypes = write_resources.get('valuetypes', {})
        attrtype = write_resources.get('attrtype', 0)
        values = write_resources['values']
        
        return self._write_dataset(out_table_name=out_table_name, 
            valuetypes=valuetypes, attrtype=attrtype, values=values)
    
    def _write_dataset(self, out_table_name, values, attrtype, valuetypes={}):
        """
        'out_table_name' specifies the subdirectory relative to base directory. 
        'values' is a dictionary where keys are the attribute names and values 
            are value arrays of the corresponding attributes. 
        'attrtype' is a dictionary where keys are the attribute names and values
            are the types of the corresponding attributes (PRIMARY,COMPUTED).
        """
        dir = os.path.join(self._get_base_directory(), out_table_name)
        
        if not os.path.exists(dir):
            os.makedirs(dir)

        for attribute_name in values:
            attribute_data = values[attribute_name]
            extension = self._extension_for_numpy_type(attribute_data.dtype)
            
            if (attrtype <> 0) and (attrtype[attribute_name] == AttributeType.PRIMARY):
                # Store primary attribute
                dir_path = dir
                
            else:
                # Store computed attribute
                dir_path = os.path.join(dir, self.DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

            existing_files_of_this_name = glob(os.path.join(dir_path, '%s.*' % attribute_name))
            for existing_file_name in existing_files_of_this_name:
                os.remove(existing_file_name)
                    
            self._write_to_file(dir_path, attribute_name, attribute_data)
            

            
           
    def _determine_file_short_name_and_attribute_type(self, file_path, lowercase=False):
        """Return the attribute name and whether it is PRIMARY or COMPUTED."""
        path, ext = os.path.splitext(file_path)
        dir, shortname = os.path.split(path)
        prefix_path, last_directory_name = os.path.split(dir)
        
        if last_directory_name == self.DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES:
            type = AttributeType.COMPUTED
        else:
            type = AttributeType.PRIMARY
            
        if lowercase:
            shortname = shortname.lower()
            
        return shortname, type
    
    def _get_extension(self, file_path):
        path, extension = os.path.splitext(file_path)
    
        if len(extension) == 0:
            raise NameError("Cannot determine numpy type since the file extension is missing from '%s'." % file_path)
        
        return extension[1:]
                
    def get_var_names(self, name):
        if re.match(r'computed/', name) or re.match(r'computed\\', name):
            return (name[len('computed')+1:], AttributeType.COMPUTED)
        else:
            return (name,AttributeType.PRIMARY)
                
    def filter_attributes(self, attribute_names_and_types, filter):
        """ Return attributes of type specified by filter.
        'attribute_names_and_types' is a list of tuples (name, type). Type is either PRIMARY or COMPUTED. 
        'filter' is either a list of attributes or one of PRIMARY and COMPUTED. If it is an empty list, all attributes are passed. 
        """
        result = []       
        for attribute_name, attribute_type in attribute_names_and_types:
            if isinstance(filter,list) and (attribute_name in filter):
                result = result + [attribute_name]
            elif (filter == attribute_type) or (filter == '*'):
                result = result + [attribute_name]
        return result            
        
    def get_dataset_names(self):
        base_dir = self._get_base_directory()
        
        if os.path.exists(base_dir):
            dir_names = os.listdir(base_dir)
            
            valid_dirs = []
            for dir_name in dir_names:
                if not os.path.isdir(os.path.join(base_dir, dir_name)):
                    continue
                    
                field_names = self._determine_field_names(in_table_name=dir_name)
                if field_names:
                    valid_dirs.append(dir_name)
            
            return valid_dirs
            
        else:
            raise FltError("Cache base directory '%s' does not exist!" % base_dir)
                    
    def has_table(self, table):
        return is_file_in_directory(table, self._get_base_directory())

    def _get_base_directory(self):
        return self._base_directory
    
    def _load_header(self, header_file_name):
        """ 
        Gets the content of the header for some attribute. 
        attribute is the name of the attribute.
        The header content is returned as a dict.
        """    
        header_records = {}
        for record in file(header_file_name):
            recdata = record.split()
            header_records[recdata[0]] = recdata[1]
            
        return header_records
        
    def _get_file_paths_for_stored_attributes(self, in_table_name=''):
        dataset_path = os.path.join(self._get_base_directory(), in_table_name)
        
        if not os.path.exists(dataset_path):
            raise FltError("Cache directory '%s' does not exist!" % dataset_path)
            
        primary_attribute_names = glob(os.path.join(dataset_path, '*.*'))
        computed_attribute_names = glob(os.path.join(dataset_path, self.DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES, '*.*'))
        
        return primary_attribute_names + computed_attribute_names
            
    def _map_byteorder_symbol_to_extension_character(self, byteorder_character):
        if byteorder_character == '=':
            return self._get_native_endian_file_extension_character()
            
        return {
            '<': 'l', # little-endian
            '>': 'b', # big-endian
            '|': 'i', # irrelevant
            }[byteorder_character]
            
    def _map_extension_character_to_byteorder_symbol(self, extension_character):
        return {
            'l': '<', # little-endian
            'b': '>', # big-endian
            'i': '|', # irrelevant
            }[extension_character]
    
    def _get_native_endian_file_extension_character(self):
        if array([1], dtype='<i4').dtype.byteorder == '=':
            return self._map_byteorder_symbol_to_extension_character('<')
        else:
            return self._map_byteorder_symbol_to_extension_character('>')
    
    def _extension_for_numpy_type(self, dtype):
        """Returns the file extension for this numpy type."""
        
        str = dtype.str
        
        return self._map_byteorder_symbol_to_extension_character(str[0]) + str[1:]
        
    def _numpy_type_for_extension(self, extension):
        """Returns the numpy type for this file extension."""
        
        try:
            return self._map_extension_character_to_byteorder_symbol(extension[0]) + extension[1:]
        except KeyError:
            raise NameError("Unrecognized file extension: '%s'" % extension)
            

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
    
    def _load_from_file(self, file_path):
        """Reads data from a file."""
        extension = self._get_extension(file_path)
        
        try:
            dtype = self._numpy_type_for_extension(extension)
        except NameError:
            raise NameError("Unrecognized file extension '%s': %s" % (extension, file_path))
        
        f = file(file_path, mode="rb")
        try:
            data = numpy.fromfile(f, dtype=dtype)
        finally:
            f.close()
        
        return data
    
    
class FltError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.value


from numpy import array
from tempfile import mkdtemp
from shutil import rmtree

from numpy import ma

import opus_core
from opus_core.tests import opus_unittest

class FunctionalTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_tmp_flt_storage_functional')
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
class FltStorageTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_tmp_flt_storage')
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
    
    def get_test_storage(self):
        return flt_storage(storage_location = 
            os.path.join(opus_core.__path__[0], 'data', 'flt'))
        
    def test_flt_directory_does_not_exist(self):
        store = self.get_test_storage()
        
        try:
            store._get_file_paths_for_stored_attributes(in_table_name='idonotexist')
            self.fail('Retrieving an flt directory that does not exist did not fail.')
        except FltError:
            pass
    
    def test_extension_and_numpy_types(self):
        storage = flt_storage(storage_location=self.temp_dir)
        
        test_data = [# data | numpy type | expected file extension
            ([1], '<i4', 'li4'),
            ([1], '>i2', 'bi2'),
            ([1], '|i1', 'ii1'),
            ([1L], '<i8', 'li8'),
            ([True, False], '|b1', 'ib1'),
            ([1.5, 3.14159], '<f8', 'lf8'),
            ([1+3j], '<c16', 'lc16'),
            (['a', 'bc'], '|S4', 'iS4'),
            ([u'a', u'bc'], '>U4', 'bU4'),
            ([self], '|O' + str(array([self]).itemsize), 'iO' + str(array([self]).itemsize)),
            ]
            
        # Test converting numpy types to file extensions
        for data, dtype, extension in test_data:
            self.assertEqual(
                storage._extension_for_numpy_type(array(data, dtype=dtype).dtype),
                extension,
                )
                
        # Test converting file extensions to numpy types
        for data, dtype, extension in test_data:
            self.assertEqual(
                storage._numpy_type_for_extension(extension),
                dtype,
                )
    
    def test_get_file_paths_for_stored_attributes(self):
        storage = flt_storage(storage_location=self.temp_dir)
        
        table_name = 'some_table'
        table_path = os.path.join(self.temp_dir, table_name)
        
        os.makedirs(table_path)
        self.assert_(os.path.exists(table_path))

        file_path1 = os.path.join(table_path, 'a.b')
        
        f = open(file_path1, 'wb')
        f.write('')
        f.close()
        
        file_names = storage._get_file_paths_for_stored_attributes(table_name)
        expected_file_names = [file_path1]
        
        self.assertEqual(file_names, expected_file_names)
        
        file_path2 = os.path.join(table_path, 'alpha.beta')
        
        f = open(file_path2, 'wb')
        f.write('')
        f.close()
        
        file_names = storage._get_file_paths_for_stored_attributes(table_name)
        expected_file_names = [file_path1, file_path2]
        expected_file_names.sort()
        file_names.sort()
        
        self.assertEqual(file_names, expected_file_names)
        
        
        # Test that a directory name does not affect the file names returned.
        os.makedirs(os.path.join(table_path, 'some_subdirectory'))
        
        file_names = storage._get_file_paths_for_stored_attributes(table_name)
        file_names.sort()
        
        self.assertEqual(file_names, expected_file_names)
        
    def test_reading_and_writing_primary_attribute_to_file(self):
        storage = flt_storage(storage_location=self.temp_dir)
        
        # Test writing 
        my_attribute = array([9,99,999], dtype='<i4')
        
        storage._write_to_file(self.temp_dir, 'my_attribute', my_attribute)
        
        expected_filename = os.path.join(self.temp_dir, 'my_attribute.li4')
        self.assert_(os.path.exists(expected_filename))
        
        # Test reading
        loaded_data = storage._load_from_file(expected_filename)
        
        self.assert_(ma.allequal(my_attribute, loaded_data))
        self.assertEqual(my_attribute.dtype, loaded_data.dtype)

    def test_writing_attribute_to_file_when_file_of_same_attribute_name_and_different_type_already_exists(self):
        
        attribute_name= "some_attribute"
        table_name = 'same_attribute_name_different_types'
        os.mkdir(os.path.join(self.temp_dir, table_name)) 
        existing_file = file(os.path.join(self.temp_dir , table_name, attribute_name + ".li4"), "w")
        existing_file.close()
        storage = flt_storage(storage_location=self.temp_dir)
        # Test writing 
        my_attributes = { attribute_name: array([9,99,999], dtype='<i8') }
        my_types = { attribute_name: AttributeType.PRIMARY }
        
        storage._write_dataset(out_table_name=table_name, values=my_attributes, attrtype=my_types)
        self.assert_(not (os.path.exists(existing_file.name)))
        self.assert_(os.path.exists(os.path.join(self.temp_dir, table_name, attribute_name + ".li8")))


        
    def test__determine_file_short_name_and_attribute_type(self):
        storage = flt_storage(storage_location=self.temp_dir)
        
        data = [
            (os.path.join('a','b','attr.li4'), ('attr', AttributeType.PRIMARY)),
            (os.path.join('a','attr.li4'), ('attr', AttributeType.PRIMARY)),
            (os.path.join('attr.li4'), ('attr', AttributeType.PRIMARY)),
            (os.path.join('a','b',storage.DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES,'c','attr.li4'), ('attr', AttributeType.PRIMARY)),

            (os.path.join('a','b',storage.DIRECTORY_NAME_FOR_COMPUTED_ATTRIBUTES,'attr.li4'), ('attr', AttributeType.COMPUTED)),
            ]
        
        for path, expected_result in data:
            result = storage._determine_file_short_name_and_attribute_type(path)
            self.assertEqual(expected_result, result)
        
        

if __name__ == '__main__':
    opus_unittest.main()