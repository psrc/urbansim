# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


import os, sys
import tempfile
from shutil import rmtree
from numpy import array
from glob import glob
from opus_core.tests import opus_unittest
from subprocess import Popen
from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache
from filecmp import dircmp, cmpfiles
from opus_core.misc import module_path_from_opus_path
from opus_core.logger import logger
from opus_core.database_management.opus_database import OpusDatabase
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import _get_installed_database_engines
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
    
class AbstractFunctionalTest(object):
    protocol = ''
    def setUp(self):
        self.db_config = TestDatabaseConfiguration(protocol = self.protocol)
        self.db_config_node = self.db_config._database_configuration_node()
        self.db_server = DatabaseServer(self.db_config)

        self.test_db = 'OpusDatabaseTestDatabase'
        
        self.export_from_cache_opus_path = "opus_core.tools.do_export_cache_to_sql"
        self.export_to_cache_opus_path = "opus_core.tools.do_export_sql_to_cache"
        self.year = 1000
        
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.test_data = {
            self.year:{
                'table_a':{
                    'tablea_id':array([1,2,3]),
                    'tablea_id_name': array(['1','2','3']),
                    'value1': array([1.0, 2.001, 3], dtype='float'),
                    'value2': array([True, False, False], dtype='i'),  ## sqlit is having problem handling bool type
                    },
                'table_b':{
                    'tableb_id':array([1,2,3]),
                    'tableb_id_name': array(['one','two','three']),
                    'value3': array([1.0, 2.001, 3], dtype='float'),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, self.test_data)
                
    def tearDown(self):
        if self.db_server.has_database(self.test_db):
            self.db_server.drop_database(self.test_db)
        self.db_server.close()
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    def test_export_all_tables(self):
        logger.log_status("Test export all tables for %s with %s" % (self.protocol, self.__class__))
        optional_args = ['-c', os.path.join(self.temp_dir, str(self.year)), 
                         '-d', self.test_db, 
                         '--database_configuration=%s' % self.db_config_node ]
        self._call_script(self.export_from_cache_opus_path,
                          args = optional_args)

        
        self.assertTrue(self.db_server.has_database(database_name = self.test_db))
        db = OpusDatabase(database_server_configuration = self.db_config, 
                          database_name = self.test_db)
        
        table_names = self.test_data[self.year].keys()
        existing_tables = db.get_tables_in_database()        
        self.assertEqual( set(existing_tables), set(table_names) )

        ## export data from db to cache
        export_year = str(self.year + 100)        
        exp_dir = os.path.join(self.temp_dir, export_year)

        optional_args = ['-d', self.test_db, 
                         '-c', self.temp_dir, 
                         '-y', export_year,
                         '--database_configuration=%s' % self.db_config_node ]
        self._call_script(self.export_to_cache_opus_path,
                          args = optional_args)

        exported_datasets = [os.path.split(f)[1] for f in glob(exp_dir + '/*')]
        self.assertEqual( set(exported_datasets), set(table_names))
        
        org_dir = os.path.join(self.temp_dir, str(self.year))
        self._two_caches_are_identical(org_dir, exp_dir)

        db.close()
        self.db_server.drop_database(self.test_db)
        rmtree(exp_dir)
        
    def test_export_one_table(self):
        logger.log_status("Test export single table for %s with %s" % (self.protocol, self.__class__))
        for table_name in self.test_data[self.year].keys():
            self._test_export_one_table(table_name)
            
    def _test_export_one_table(self, table_name):
        optional_args = ['-c', os.path.join(self.temp_dir, str(self.year)), 
                         '-d', self.test_db,
                         '-t', table_name,
                         '--database_configuration=%s' % self.db_config_node ]
        self._call_script(self.export_from_cache_opus_path,
                          args = optional_args)
        
        self.assertTrue(self.db_server.has_database(database_name = self.test_db))
        db = OpusDatabase(database_server_configuration = self.db_config, 
                          database_name = self.test_db)
        existing_tables = db.get_tables_in_database()
        self.assertEqual( set(existing_tables), set([table_name]) )
        
        export_year = str(self.year + 100)        
        exp_dir = os.path.join(self.temp_dir, export_year)
        
        optional_args = ['-d', self.test_db, 
                         '-c', self.temp_dir, 
                         '-y', export_year,
                         '-t', table_name,
                         '--database_configuration=%s' % self.db_config_node ]
        self._call_script(self.export_to_cache_opus_path,
                          args = optional_args)

        exported_datasets = [os.path.split(f)[1] for f in glob(os.path.join(self.temp_dir, export_year) + '/*')]
        self.assertEqual( set(exported_datasets), set([table_name]))
        
        org_dir = os.path.join(self.temp_dir, str(self.year))
        self._two_caches_are_identical(org_dir, exp_dir, table_names=[table_name])

        db.close()
        self.db_server.drop_database(self.test_db)
        rmtree(exp_dir)

    def _call_script(self, opus_path, args):
            Popen( " %s %s %s" % (sys.executable, module_path_from_opus_path(opus_path), ' '.join(args)),
                   shell = True
                 ).communicate()        

    def _two_caches_are_identical(self, cache_a, cache_b, table_names=None):
        """ Check to see if two caches contains identical datasets 
        even though their data types can be different
        """
        if table_names is None:
            table_names = os.listdir(cache_a)
        for table_name in table_names:
            field_names_a = glob(os.path.join(cache_a, table_name) + '/*')
            field_names_b = glob(os.path.join(cache_b, table_name) + '/*')
            self.assertEqual(len(field_names_a), len(field_names_b))
            field_names_a.sort(); field_names_b.sort()
            [self.assertTrue(cmp(f_a, f_b)) for f_a, f_b in zip(field_names_a, field_names_b)]        
        
installed_engines = _get_installed_database_engines()

if 'sqlite' in installed_engines:
    class Testsqlite(AbstractFunctionalTest, opus_unittest.OpusTestCase):
        protocol = 'sqlite'

if 'mysql' in installed_engines:
    class Testmysql(AbstractFunctionalTest, opus_unittest.OpusTestCase):
        protocol = 'mysql'

## Masked tests for postgres until we have a test server running
#if 'postgres' in installed_engines:
#    class Testposgres(AbstractFunctionalTest, opus_unittest.OpusTestCase):
#        protocol = 'postgres'
        
if __name__=="__main__":
    opus_unittest.main()