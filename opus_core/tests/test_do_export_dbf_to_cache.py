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


from opus_core.tests import opus_unittest

import os, sys
import tempfile

from shutil import rmtree

from opus_core.opus_package import OpusPackage


class Tests(opus_unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_do_export_dbf_to_cache')

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def test(self):
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
        try:        
            from dbfpy.dbf import Dbf as _dbf_class
        except ImportError:
            raise ImportError('Must install Python module dbfpy to use '
                               'dbf_storage; see http://dbfpy.sourceforge.net/.')
                
        result = os.system(cmd)

        # Did command run without any errors?
        self.assertEqual(0, result)
        
        # Was attribute cache directory for this year created?
        self.assert_(os.path.exists(os.path.join(attribute_cache_directory, cache_year)))
        self.assert_(os.path.exists(os.path.join(attribute_cache_directory, cache_year, table_name)))
        
        # Are the computed attributes there?
        attribute_dir = os.path.join(attribute_cache_directory, cache_year, table_name)
        
        files_to_check_endian_template = [
            'dummyfloat.%sf8',
            'dummyint.%si4',
            'keyid.%si4',
            ]
        files_in_dir = os.listdir(attribute_dir)
        for file_endian_template in files_to_check_endian_template:
            if ((not os.path.exists(os.path.join(attribute_dir, file_endian_template%'l'))) and
                    (not os.path.exists(os.path.join(attribute_dir, file_endian_template%'b')))):
                self.fail("Neither attribute '%s' nor '%s' exist in %s." % (
                    file_endian_template%'l',
                    file_endian_template%'b',
                    attribute_dir
                    ))
        

if __name__ == "__main__":
        opus_unittest.main()