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

from opus_core.logger import logger
from table_creator import TableCreator

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
            raise NameError, "Invalid table name specified! (%s)" % table_name
            
        db.DoQuery('INSERT INTO %s (building_type_id, name, units, is_residential) VALUES'
            '(1, "commercial", "commercial_sqft", 0),' 
            '(2, "governmental", "governmental_sqft", 0),'
            '(3, "industrial", "industrial_sqft", 0),'
            '(4, "residential", "residential_units", 1);'
                % table_name)
        

import os    
from opus_core.tests import opus_unittest

from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import LocalhostDatabaseServerConfiguration


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_name = 'test_create_table'
        
        self.db_server = MysqlDatabaseServer(LocalhostDatabaseServerConfiguration())
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
            
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        self.assert_(not self.db.table_exists('building_types'))
        
        
    def test_create_table(self):
        CreateBuildingTypesTable().create_building_types_table(
            LocalhostDatabaseServerConfiguration(), self.db_name)
        
        self.assert_(self.db.table_exists('building_types'))
    
            
if __name__ == '__main__':
    opus_unittest.main()
