# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from .table_creator import TableCreator

class CreateBuildingTypesTable(TableCreator):
    def create_building_types_table(self, config, db_name):
        table_name = 'building_types'
        
        logger.log_status('Creating table %s.' % table_name)

        db = self._get_db(config, db_name)
        self._backup_table(db, table_name)
        self._drop_table(db, table_name)
        self._create_table(db, table_name)

    def _create_table(self, db, table_name):
        try:
            db.DoQuery('CREATE TABLE %s '
                '(building_type_id INT, name varchar(50), units varchar(50), is_residential int(1));' 
                % table_name)
        except:
            raise NameError("Invalid table name specified! (%s)" % table_name)
            
        db.DoQuery('INSERT INTO %s (building_type_id, name, units, is_residential) VALUES'
            '(1, "commercial", "commercial_sqft", 0),' 
            '(2, "governmental", "governmental_sqft", 0),'
            '(3, "industrial", "industrial_sqft", 0),'
            '(4, "residential", "residential_units", 1);'
                % table_name)
        

import os    
from opus_core.tests import opus_unittest

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_name = 'test_create_table'
        
        self.db_server = DatabaseServer(TestDatabaseConfiguration(protocol = 'mysql'))
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
            
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        self.assertTrue(not self.db.table_exists('building_types'))
        
        
    def test_create_table(self):
        CreateBuildingTypesTable().create_building_types_table(
            TestDatabaseConfiguration(protocol = 'mysql'), self.db_name)
        
        self.assertTrue(self.db.table_exists('building_types'))
    
            
if __name__ == '__main__':
    opus_unittest.main()
