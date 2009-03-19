# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


import os
import tempfile
from shutil import rmtree

from numpy import array

from opus_core.tests import opus_unittest
from opus_core.fork_process import ForkProcess
from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache

    
class AbstractFunctionalTestForDoExportCacheToDelimitedFiles(object):
    """
    An abstract test class to make it easy to test exporting from all forms of 
    delimited storage.
    
    Child class must define the following properties:
    - type, e.g. "comma"
    - file_extension, e.g. ".csv"
    """
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_do_export_cache_to_%s_delimited_files' %
                                         self.type)
        test_data = {
            1000:{
                'table_a':{
                    'id':array([1,2,3]),
                    },
                'table_b':{
                    'id':array([1,2,3]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, test_data)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    def test_use_directory_that_does_not_exist(self):
        path_to_cache = 'a_directory_that_does_not_exist'
        tool_opus_path = 'opus_core.tools.do_export_cache_to_%s_delimited_files' % self.type
        optional_args = '-c %s -o %s' % (
            path_to_cache,
            self.temp_dir,
            )
        self.assertRaises(StandardError,
                          ForkProcess().fork_new_process,
                          tool_opus_path, 
                          resources = None, 
                          optional_args = optional_args,
                          quiet=True)

    def test_does_copy_entire_cache(self):
        path_to_cache = os.path.join(self.temp_dir, '1000')
        tool_opus_path = 'opus_core.tools.do_export_cache_to_%s_delimited_files' % self.type
        optional_args = ['-c', path_to_cache, '-o', self.temp_dir]
        ForkProcess().fork_new_process(tool_opus_path, 
                                       resources = None, 
                                       optional_args = optional_args)
        
        # Test for a few tales that worked.
        self.assert_(os.path.exists(os.path.join(self.temp_dir, 'table_a' + self.file_extension)))
        self.assert_(os.path.exists(os.path.join(self.temp_dir, 'table_b' + self.file_extension)))

    def test_does_copy_one_table(self):
        path_to_cache = os.path.join(self.temp_dir, '1000')
        tool_opus_path = 'opus_core.tools.do_export_cache_to_%s_delimited_files' % self.type
        optional_args = ['-c', path_to_cache, '-o', self.temp_dir, '-t', 'table_a']
        ForkProcess().fork_new_process(tool_opus_path, 
                                       resources = None, 
                                       optional_args = optional_args)
        self.assert_(os.path.exists(os.path.join(self.temp_dir, 'table_a' + self.file_extension)))
        self.assert_(not os.path.exists(os.path.join(self.temp_dir, 'table_b' + self.file_extension)))


class FunctionalTestForDoExportCacheToCommaDelimitedFiles(AbstractFunctionalTestForDoExportCacheToDelimitedFiles, opus_unittest.OpusTestCase):
    type = 'comma'
    file_extension = '.csv'

class FunctionalTestForDoExportCacheToTabDelimitedFiles(AbstractFunctionalTestForDoExportCacheToDelimitedFiles, opus_unittest.OpusTestCase):
    type = 'tab'
    file_extension = '.tab'

if __name__=="__main__":
    opus_unittest.main()