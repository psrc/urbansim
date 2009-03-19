# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.logger import logger
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration



class CreateJobBuildingTypesTable(object):
    def create_building_types_table(self, db_config, db_name):
        table_name = 'job_building_types'

        dbconfig = DatabaseServerConfiguration(
            host_name = db_config.host_name,
            user_name = db_config.user_name,
            protocol = 'mysql',
            password = db_config.password                                       
        )
        db_server = DatabaseServer(dbconfig)
        
        try:
            db = db_server.get_database(db_name)
        except:
            raise NameError, "Unknown database '%s'!" % db_name

        logger.log_status('Creating table %s.' % table_name)
        try:
            db.DoQuery('DROP TABLE IF EXISTS %s;' % table_name)
            db.DoQuery('CREATE TABLE %s '
                '(id INT, name varchar(50), home_based INT);' 
                % table_name)
        except:
            raise NameError, "Invalid table name specified! (%s)" % table_name
            
        db.DoQuery('INSERT INTO %s (id, name, home_based) VALUES'
            '(1, "commercial", 0),' 
            '(3, "industrial", 0),'
            '(2, "governmental", 0),'
            '(4, "home_based", 1);'
                % table_name)
        

import os    
from opus_core.tests import opus_unittest
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class TestCreateJobBuildingTypesTable(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_name = 'test_create_table'
        
        self.db_server = DatabaseServer(TestDatabaseConfiguration(protocol = 'mysql',))
        
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
            
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        try:
            self.db.DoQuery('select * from job_building_types;')
            self.fail('Output table job_building_tpes already exists. (Check setUp)')
        except: pass
        
        
    def test_create_table(self):
        CreateJobBuildingTypesTable().create_building_types_table(
            TestDatabaseConfiguration(protocol = 'mysql'), self.db_name)
        
        try:
            self.db.DoQuery('select * from job_building_types;')
        except:
            self.fail('Expected output table job_building_types does not exist.')
    
            
    def test_values(self):
        CreateJobBuildingTypesTable().create_building_types_table(
            TestDatabaseConfiguration(protocol = 'mysql'), self.db_name)
        
        expected_results = [
            ['id', 'name', 'home_based'],
            [1, "commercial", 0],
            [3, "industrial", 0],
            [2, "governmental", 0],
            [4, "home_based", 1]
            ]
        
        try:
            results = self.db.GetResultsFromQuery(
                'select * from job_building_types;')
        except:
            self.fail('Expected output table job_building_types does not exist.')
        
        self.assert_(expected_results == results,
            "Table job_building_types has incorrect values! "
            "Expected: %s. Received: %s" % (expected_results, results))
            
        
if __name__ == '__main__':
    opus_unittest.main()