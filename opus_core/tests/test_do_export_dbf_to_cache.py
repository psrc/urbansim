# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from opus_core.tests import opus_unittest
import os, sys, tempfile
from shutil import rmtree
from opus_core.opus_package import OpusPackage
from opus_core.tests.utils.cache_extension_replacements import replacements

class Tests(opus_unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_do_export_dbf_to_cache')

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test(self):
        try:        
            from dbfpy.dbf import Dbf as _dbf_class
        except ImportError:
            return
#            raise ImportError('Must install Python module dbfpy to use '
#                               'dbf_storage; see http://dbfpy.sourceforge.net/.')
        else:
            opus_package_path = OpusPackage().get_opus_core_path()
            cacher_file_path = os.path.join(opus_package_path, 'tools', 'do_export_dbf_to_cache.py')
            
            params_needed = [
                'dbf_directory',
                'table_name',
                'attribute_cache_directory',
                'cache_year'
                ]
            
            dbf_directory = os.path.join(opus_package_path, 'tests', 'data', 'dbf')
            table_name = 'test_medium'
            attribute_cache_directory = os.path.join(self.temp_dir, 'cache')
            cache_year = '2000'
            
            cmd_format = '%s %s' % (sys.executable, cacher_file_path)
            cmd_dict = {}
            for param in params_needed:
                cmd_format += (' --%s %%(%s)s' % (param, param))
                cmd_dict[param] = eval(param)
            cmd = cmd_format % cmd_dict
            
            # The system command formed above will fail confusingly when executed without dbfpy.
            # Is dbfpy installed?
                    
            result = os.system(cmd)
    
            # Did command run without any errors?
            self.assertEqual(0, result)
            
            # Was attribute cache directory for this year created?
            self.assert_(os.path.exists(os.path.join(attribute_cache_directory, cache_year)))
            self.assert_(os.path.exists(os.path.join(attribute_cache_directory, cache_year, table_name)))
            
            # Are the computed attributes there?
            attribute_dir = os.path.join(attribute_cache_directory, cache_year, table_name)
            # The file extensions will depend on whether the architecture is 32 or 64 bit, and on
            # whether it is little-endian or big-endian.
            file_templates = ['dummyfloat.%(endian)sf8', 'dummyint.%(endian)si%(bytes)u', 'keyid.%(endian)si%(bytes)u']
            files_in_dir = os.listdir(attribute_dir)
            for template in file_templates:
                f = template%replacements
                if not os.path.exists(os.path.join(attribute_dir, f)):
                    self.fail("Didn't find attribute '%s' in %s." % (f, attribute_dir))

if __name__ == "__main__":
        opus_unittest.main()