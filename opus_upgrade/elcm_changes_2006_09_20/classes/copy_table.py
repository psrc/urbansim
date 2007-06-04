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


class CopyTable(object):
    def copy_table(self, db_config, db_name, from_table_name, to_table_name):
        db_server = MysqlDatabaseServer(db_config)
        
        try:
            db = db_server.get_database(db_name)
        except:
            raise NameError, "Unknown database '%s'!" % db_name

        logger.log_status('Copying %s to %s.' 
            % (from_table_name, to_table_name))
        try:
            db.drop_table(to_table_name)
            db.DoQuery('CREATE TABLE %s SELECT * FROM $$.%s;' 
                % (to_table_name, from_table_name))
        except:
            raise NameError, "Unknown or invalid table specified!"
        

import os    
from opus_core.tests import opus_unittest

from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import LocalhostDatabaseServerConfiguration

class TestCopyTable(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_server = MysqlDatabaseServer(LocalhostDatabaseServerConfiguration())
        
        self.db_name = 'test_copy_table'
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
        
        self.from_table = 'from_table'
        self.to_table = 'to_table'
        
        self.db.DoQuery('CREATE TABLE %s (id INT);' % self.from_table)
            
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        try:
            self.db.DoQuery('select * from %s;' % self.from_table)
        except:
            self.fail('Expected input table %s did not exist. (Check setUp)' 
                % self.from_table)
                    
        try:
            self.db.DoQuery('select * from %s;' % self.to_table)
            self.fail('Output table %s already exists. (Check setUp)' 
                % self.to_table)
        except: pass
        
        
    def test_copy_table(self):
        CopyTable().copy_table(LocalhostDatabaseServerConfiguration(), self.db_name, 
            self.from_table, 
            self.to_table)
        
        for table in (self.from_table, self.to_table):
            try:
                self.db.DoQuery('select * from %s;' % table)
            except:
                self.fail('Expected output table %s does not exist.' % table)
        
        
if __name__ == '__main__':
    opus_unittest.main()