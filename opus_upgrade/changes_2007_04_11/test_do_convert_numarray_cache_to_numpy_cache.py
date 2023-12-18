# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import sys
import tempfile

import numpy

from shutil import rmtree

from opus_core.tests import opus_unittest
from opus_core.store.file_flt_storage import file_flt_storage
from opus_core.opus_package import OpusPackage

from opus_upgrade.changes_2007_04_11.do_convert_numarray_cache_to_numpy_cache import ConvertNumarrayCacheToNumpyCache

class TestDoConvertNumarrayCacheToNumpyCache(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_do_convert_numarray_cache_to_numpy_cache')
        
        package = OpusPackage()
        opus_package_path = package.get_path_for_package('opus_upgrade')
        
        self.root_path = os.path.join(opus_package_path, 'changes_2007_04_11')
        self.test_data_path = os.path.join(self.root_path, 'test_data')

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_convert_files(self):
        numarray_file_path = os.path.join(self.test_data_path, 'numarray_inputs', 'do_not_change_me.sometext')
        numpy_file_path = os.path.join(self.test_data_path, 'numpy_inputs', 'do_not_change_me.sometext')
        
        output_directory = self.temp_dir
        convert = ConvertNumarrayCacheToNumpyCache()
        
        convert.convert_file(os.path.join(self.test_data_path, 'numarray_inputs'), 'do_not_change_me.sometext', output_directory)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'do_not_change_me.sometext')))
        
        endian = file_flt_storage.storage_file(None)._get_native_endian_file_extension_character()

        convert.convert_file(os.path.join(self.test_data_path, 'numarray_inputs'), 'f.Int32', output_directory)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'f.%si4' % endian)))
        
        convert.convert_file(os.path.join(self.test_data_path, 'numarray_inputs'), 'd.Float32', output_directory)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'd.%sf4' % endian)))
        
        convert.convert_file(os.path.join(self.test_data_path, 'numarray_inputs'), 'c.txt', output_directory)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'c.iS7')))
        
        # Does the file contain the expected data?
        f = open(os.path.join(output_directory, 'c.iS7'), 'rb')
        actual = f.read()
        f.close()
        
        f = open(os.path.join(self.test_data_path, 'numpy_inputs', 'c.iS7'), 'rb')
        expected = f.read()
        f.close()
        
        self.assertEqual(expected, actual)
        
    def test_copy_entire_cache_using_object(self):
        directory_to_copy = os.path.join(self.test_data_path, 'numarray_inputs')
        numpy_directory_containing_expected_data = os.path.join(self.test_data_path, 'numpy_inputs')
        output_directory = self.temp_dir
        
        converter = ConvertNumarrayCacheToNumpyCache()
        converter.execute(directory_to_copy, output_directory)
        
        self.assertTrue(self._are_directories_same(numpy_directory_containing_expected_data, output_directory))
        
        # Should notice that empty directory is gone.
        rmtree(os.path.join(output_directory, 'a'))
        self.assertTrue(not self._are_directories_same(numpy_directory_containing_expected_data, output_directory))
        
        # Make them the same again
        converter.execute(directory_to_copy, output_directory)
        # Then change contents of one of the files.
        numpy.array([100]).tofile(os.path.join(output_directory, 'f.li4'))
        self.assertTrue(not self._are_directories_same(numpy_directory_containing_expected_data, output_directory))
        
        # Make them the same again
        converter.execute(directory_to_copy, output_directory)
        # Add directory in output_directory
        os.mkdir(os.path.join(output_directory, 'new_dir'))
        self.assertTrue(not self._are_directories_same(numpy_directory_containing_expected_data, output_directory))
        
    def _are_directories_same (self, first_path, second_path):
        return (self._is_first_directory_subset_of_second(first_path, second_path) and
                self._is_first_directory_subset_of_second(second_path, first_path))
     
    def _is_first_directory_subset_of_second(self, first_path, second_path):
        files_and_directories_to_ignore = ['CVS', '.svn']
        
        def files_have_same_data(first_path, second_path):
            f = open(first_path)
            first = f.read()
            f.close()
            f = open(second_path)
            second = f.read()
            f.close()
            return first == second
        
        for file_or_dir_name in os.listdir(first_path):
            if file_or_dir_name in files_and_directories_to_ignore:
                continue
            first_file_or_dir_path = os.path.join(first_path, file_or_dir_name)
            second_file_or_dir_path = os.path.join(second_path, file_or_dir_name)
            if not os.path.exists(second_file_or_dir_path):
                return False
            if os.path.isfile(first_file_or_dir_path):
                if not files_have_same_data(first_file_or_dir_path, second_file_or_dir_path):
                    return False
            else:
                if not self._is_first_directory_subset_of_second(first_file_or_dir_path, second_file_or_dir_path):
                    return False
        return True
                
    def deactivted_test_copy_entire_cache_using_command_line(self):
        directory_to_copy = os.path.join(self.test_data_path, 'numarray_inputs')
        numpy_directory_containing_expected_data = os.path.join(self.test_data_path, 'numpy_inputs')
        output_directory = self.temp_dir
        command_file_path = os.path.join(self.root_path, 'do_convert_numarray_cache_to_numpy_cache.py')

        cmd = '%s %s --cache_files_directory %s --output_directory %s' % (
            sys.executable,
            command_file_path,
            directory_to_copy,
            output_directory,
            )
        
        print(cmd)
        result = os.system(cmd)
        self.assertEqual(0, result)
        
        # Check that output files have correct data.
        self.assertTrue(self._are_directories_same(numpy_directory_containing_expected_data, output_directory))
        

if __name__ == '__main__':
    opus_unittest.main()