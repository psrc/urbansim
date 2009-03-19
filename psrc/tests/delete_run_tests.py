# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os, sys
import tempfile
from shutil import rmtree

from opus_core.tests import opus_unittest
from opus_core.logger import logger
from opus_core.misc import module_path_from_opus_path

from psrc.tests.test_run_manager import _do_run_simple_test_run
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer

class DeleteRunsTests(opus_unittest.OpusIntegrationTestCase):
    ### TODO: These tests can be moved into opus_core once 
    ###       _do_run_simple_test_run has been re-written without psrc 
    ###       dependencies.

    def do_cmd(self, cmd):
        print cmd
        os.system(cmd)
        
    def setUp(self):
        self.config = TestDatabaseConfiguration(database_name='services_test')
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        _do_run_simple_test_run(self, self.temp_dir, self.config, end_year=2004)

    def tearDown(self):
        rmtree(self.temp_dir)
        server = DatabaseServer(self.config)
        server.drop_database('services_test')
        
    #def test_delete_all_years(self):
        #cache_dir = self.resources['cache_directory']
        #self.assert_(os.path.exists(cache_dir))
        #path = module_path_from_opus_path('opus_core.tools.delete_run')
        #python_cmd = 'python %s --run-id=%d --database=services_test' % (
            #path,
            #self.resources['run_id'])
        ## Close all log files so we can delete the cache.
        #logger.disable_all_file_logging()
        #os.system(python_cmd)
        #self.assert_(not os.path.exists(cache_dir))
    
    def test_delete_some_years(self):            
        cache_dir = self.resources['cache_directory']
        self.assert_(os.path.exists(cache_dir))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2000')))
        path = module_path_from_opus_path('opus_core.tools.delete_run')
        
        cmd_template = sys.executable + ' %(path)s --run-id=%(run_id)d --years-to-delete=%(years_to_delete)s --services_database=services_test'
        
        # First just delete 2 years of data.
        python_cmd = cmd_template % {
            'path':path,
            'run_id':self.resources['run_id'],
            'years_to_delete':'[2001,2002]'}
        
        # Close all log files so we can delete the cache.
        logger.disable_all_file_logging()
        self.do_cmd(python_cmd)
        self.assert_(os.path.exists(cache_dir))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2000')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2001')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2002')))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2003')))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2004')))
        
        # Now see if we can delete another year of data.
        python_cmd = cmd_template % {
            'path':path,
            'run_id':self.resources['run_id'],
            'years_to_delete':'2003'}
        # Close all log files so we can delete the cache.
        logger.disable_all_file_logging()
        self.do_cmd(python_cmd)
        self.assert_(os.path.exists(cache_dir))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2000')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2001')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2002')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2003')))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2004')))
        
        # Trying to delete the same year again should be a no-op.
        python_cmd = cmd_template % {
            'path':path,
            'run_id':self.resources['run_id'],
            'years_to_delete':'1997'}
        # Close all log files so we can delete the cache.
        logger.disable_all_file_logging()
        self.do_cmd(python_cmd)
        self.assert_(os.path.exists(cache_dir))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2000')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2001')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2002')))
        self.assert_(not os.path.exists(os.path.join(cache_dir, '2003')))
        self.assert_(os.path.exists(os.path.join(cache_dir, '2004')))
        
        # Now try to delete the rest of the years of data
        python_cmd = '%(executable)s %(path)s --run-id=%(run_id)d --services_database=services_test' % {
            'executable':sys.executable,
            'path':path,
            'run_id':self.resources['run_id']}
        # Close all log files so we can delete the cache.
        logger.disable_all_file_logging()
        self.do_cmd(python_cmd)
        self.assert_(not os.path.exists(cache_dir))
    

if __name__ == "__main__":
    opus_unittest.main()