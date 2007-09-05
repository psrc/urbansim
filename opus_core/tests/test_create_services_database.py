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

import os
from opus_core.tests import opus_unittest

from opus_core.fork_process import ForkProcess
from opus_core.store.mysql_database_server import MysqlDatabaseServer

from opus_core.misc import does_test_database_server_exist
from opus_core.tests.utils.database_server_configuration_for_tests import DatabaseServerConfigurationForTests


if does_test_database_server_exist(module_name=__file__):
    class Test(opus_unittest.OpusTestCase):
        def setUp(self):
            self.database_name = '__test_services_code__'
            self.db_server = MysqlDatabaseServer(DatabaseServerConfigurationForTests())
            self.db_server.drop_database(self.database_name)
            
        def tearDown(self):
            self.db_server.drop_database(self.database_name)
            self.db_server.close()
    
        def test_create_when_already_exists(self):
            """Shouldn't do anything if the database already exists."""
            self.db_server.create_database(self.database_name)
            db = self.db_server.get_database(self.database_name)
            self.assert_(not db.table_exists('run_activity'))
            
            ForkProcess().fork_new_process('opus_core.tools.create_services_database', resources=None, 
                                           optional_args='--database %s --hostname %s' % (
                                               self.database_name, os.environ['MYSQLHOSTNAMEFORTESTS']))
                                               
            self.assert_(db.table_exists('run_activity'))
    
        def test_create(self):
            """Should create run_activity table if the database doesn't exist."""
            ForkProcess().fork_new_process('opus_core.tools.create_services_database', resources=None, 
                                           optional_args='--database %s --hostname %s' % (
                                               self.database_name, os.environ['MYSQLHOSTNAMEFORTESTS']))
            db = self.db_server.get_database('mysql')
            results = db.GetResultsFromQuery('show databases')
            for database in results:
                print database
            self.assert_(self.db_server.has_database(self.database_name))
            db = self.db_server.get_database(self.database_name)
            self.assert_(db.table_exists('run_activity'))


if __name__=="__main__":
    opus_unittest.main()