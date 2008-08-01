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
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration


class TableCreator(object):
    """Shared functionality for update scripts that need to create a table.
    """
    def _get_db(self, db_config, db_name):
        dbconfig = DatabaseServerConfiguration(
            protocol = 'mysql',
            host_name = db_config.host_name,
            user_name = db_config.user_name,
            password = db_config.password                                       
        )
        db_server = DatabaseServer(dbconfig)
        
        try:
            return db_server.get_database(db_name)
        except:
            raise NameError, "Unknown database '%s'!" % db_name      
        
    def _backup_table(self, db, table_name):
        try:
            if db.table_exists(table_name):
                # create backup of table.
                db.DoQuery('DROP TABLE IF EXISTS %s_bak;' % table_name)
                db.DoQuery('create table %s_bak select * from %s;' % (table_name, table_name))
        except:
            pass
        
    def _drop_table(self, db, table_name):
        try:
            db.DoQuery('DROP TABLE IF EXISTS %s;' % table_name)
        except:
            raise NameError, "Invalid table name specified! (%s)" % table_name


import os        
from opus_core.tests import opus_unittest

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_name = 'test_create_table'
        
        self.db_server = DatabaseServer(DatabaseServerConfiguration(protocol = 'mysql'))
        
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
            
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        try:
            self.db.DoQuery('select * from building_types;')
            self.fail('Output table building_tpes already exists. (Check setUp)')
        except: pass
        
    def test_create_table(self):
        creator = TableCreator()
        db = creator._get_db(DatabaseServerConfiguration(protocol = 'mysql'), self.db_name)
        self.assert_(not db.table_exists('test_table'))
        self.assert_(not db.table_exists('test_table_bak'))
        
        db.DoQuery('CREATE TABLE test_table '
                '(id INT, name varchar(50), units varchar(50));')
        self.assert_(db.table_exists('test_table'))
        self.assert_(not db.table_exists('test_table_bak'))

        creator._backup_table(db, 'test_table')
        self.assert_(db.table_exists('test_table'))
        self.assert_(db.table_exists('test_table_bak'))
        
        creator._drop_table(db, 'test_table')
        self.assert_(not db.table_exists('test_table'))
        self.assert_(db.table_exists('test_table_bak'))
            
if __name__ == '__main__':
    opus_unittest.main()