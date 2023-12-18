# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


import os
import tempfile
from shutil import rmtree
from numpy import array
from glob import glob
from opus_core.tests import opus_unittest
from opus_core.fork_process import ForkProcess
from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache
from filecmp import dircmp, cmpfiles

    
class AbstractFunctionalTest(object):
    """
    An abstract test class to make it easy to test exporting from all forms
    """
    format = ''

        
    def setUp(self):
        self.export_from_cache_opus_path = "opus_core.tools.do_export_cache_to_%s" % self.format
        self.export_to_cache_opus_path = "opus_core.tools.do_export_%s_to_cache" % self.format
        self.year = 1000
        
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.test_data = {
            self.year:{
                'table_a':{
                    'id':array([1,2,3]),
                    'id_name': array(['1','2','3']),
                    'value1': array([1.0, 2.001, 3], dtype='float'),
                    'value2': array([True, False, False]),
                    },
                'table_b':{
                    'id':array([1,2,3]),
                    'id_name': array(['one','two','three']),
                    'value1': array([1.0, 2.001, 3], dtype='float'),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, self.test_data)
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

#    def test_use_directory_that_does_not_exist(self):
#        optional_args = '-c %s -o %s %s' % (
#            os.path.join(self.temp_dir, "a_directory_that_does_not_exist"),
#            self.temp_dir,
#            self.additional_args
#            )
#        self.assertRaises(StandardError,
#                          ForkProcess().fork_new_process,
#                          self.tool_script_opus_path, 
#                          resources = None,
#                          optional_args = optional_args,
#                          quiet=True)        

    def test_export_all_tables(self):
        output_temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        optional_args = ['-c', os.path.join(self.temp_dir, str(self.year)), '-o', output_temp_dir]
        ForkProcess().fork_new_process(self.export_from_cache_opus_path, 
                                       resources = None, 
                                       optional_args = optional_args)
        
        table_names = list(self.test_data[self.year].keys())
        files = [os.path.splitext(os.path.split(f)[1])[0] for f in glob(output_temp_dir + '/*')]
        self.assertEqual( set(files), set(table_names))
        
        ## below is covered by test_export_one_table
        #export_year = str(self.year + 100)
        #for afile in files:            
            #optional_args = ['-d', output_temp_dir, '-c', self.temp_dir, '-y', export_year, '-t', afile]
            #ForkProcess().fork_new_process(self.export_to_cache_opus_path, 
                                           #resources = None, 
                                           #optional_args = optional_args)

        #exported_datasets = [os.path.split(f)[1] for f in glob(os.path.join(self.temp_dir, export_year) + '/*')]
        #self.assertEqual( set(exported_datasets), set(table_names))
        
        #org_dir = os.path.join(self.temp_dir, str(self.year))
        #exp_dir = os.path.join(self.temp_dir, export_year)
        #for table_name in table_names:
            #flt_file_names = os.listdir(os.path.join(org_dir, table_name))
            #self.assertEqual( cmpfiles(os.path.join(org_dir, table_name), 
                                       #os.path.join(exp_dir, table_name), 
                                       #flt_file_names),
                              #(flt_file_names, [], [] )
                              #)

    def test_export_one_table(self):
        for table_name in list(self.test_data[self.year].keys()):
            self._test_export_one_table(table_name)
            
    def _test_export_one_table(self, table_name):
        output_temp_dir = tempfile.mkdtemp(dir=self.temp_dir)
        optional_args = ['-c', os.path.join(self.temp_dir, str(self.year)), '-o', output_temp_dir, '-t', table_name]
        ForkProcess().fork_new_process(self.export_from_cache_opus_path, 
                                       resources = None, 
                                       optional_args = optional_args)
        
        files = [os.path.splitext(os.path.split(f)[1])[0] for f in glob(output_temp_dir + '/*')]
        self.assertEqual( set(files), set([table_name]))
        
        export_year = str(self.year + 100)        
        optional_args = ['-d', output_temp_dir, '-c', self.temp_dir, '-y', export_year, '-t', table_name]
        ForkProcess().fork_new_process(self.export_to_cache_opus_path, 
                                       resources = None, 
                                       optional_args = optional_args)

        exported_datasets = [os.path.split(f)[1] for f in glob(os.path.join(self.temp_dir, export_year) + '/*')]
        self.assertEqual( set(exported_datasets), set([table_name]))
        
        org_dir = os.path.join(self.temp_dir, str(self.year))
        exp_dir = os.path.join(self.temp_dir, export_year)
        flt_file_names = os.listdir(os.path.join(org_dir, table_name))
        self.assertEqual( cmpfiles(os.path.join(org_dir, table_name), 
                                   os.path.join(exp_dir, table_name), 
                                   flt_file_names),
                          (flt_file_names, [], [] )
                          )
        rmtree(output_temp_dir)
        rmtree(exp_dir)

class TestCsv(AbstractFunctionalTest, opus_unittest.OpusTestCase):
    format = 'csv'

class TestTab(AbstractFunctionalTest, opus_unittest.OpusTestCase):
    format = 'tab'

try:        
    from dbfpy.dbf import Dbf
    class TestDbf(AbstractFunctionalTest, opus_unittest.OpusTestCase):
        format = 'dbf'
except ImportError:
    pass
    
if __name__=="__main__":
    opus_unittest.main()