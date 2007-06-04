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
from opus_core.store.mysql_database_server import MysqlDatabaseServer


class CreateJobBuildingTypesTable(object):
    def create_building_types_table(self, db_config, db_name):
        table_name = 'job_building_types'
        
        db_server = MysqlDatabaseServer(db_config)
        
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

from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import LocalhostDatabaseServerConfiguration


class TestCreateJobBuildingTypesTable(opus_unittest.OpusTestCase):
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
        try:
            self.db.DoQuery('select * from job_building_types;')
            self.fail('Output table job_building_tpes already exists. (Check setUp)')
        except: pass
        
        
    def test_create_table(self):
        CreateJobBuildingTypesTable().create_building_types_table(
            LocalhostDatabaseServerConfiguration(), self.db_name)
        
        try:
            self.db.DoQuery('select * from job_building_types;')
        except:
            self.fail('Expected output table job_building_types does not exist.')
    
            
    def test_values(self):
        CreateJobBuildingTypesTable().create_building_types_table(
            LocalhostDatabaseServerConfiguration(), self.db_name)
        
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