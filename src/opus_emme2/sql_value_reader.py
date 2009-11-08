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

class SqlValueReader(object):
    """Wrapper class to read one arbitrary value in the database. 
    """
    def __init__(self, database_connection, table_name):
        self.db = database_connection
        self._table_name = table_name
    
    def get_value(self, column_name, **selectors):
        """Read exactly one value from a column. 
        Example:
              get_value(some_column, year=2001, zone=123)
                   - gets the value from some_column where year=2001 and zone=123
           selectors are optional. However, an exception will be raised if exactly one value is not returned.
        """
        table = self._table_name
        query = 'select %(column_name)s from $$.%(table)s' % locals()
        if selectors:
            query += ' where %s' % ' and '.join(['%s=%s' % 
                                                 (name, str(value)) for (name, value) in selectors.iteritems()])
        result = self.db.GetResultsFromQuery(query)
        if len(result) != 2:
            raise StandardError("There was not exactly one value returned by the query: %s" % query)
        return result[1][0]

#================================================================================
# Tests
#================================================================================
import os

from opus_core.tests import opus_unittest
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.misc import does_test_database_server_exist

if does_test_database_server_exist(module_name=__name__):

    from opus_core.store.mysql_database_server import MysqlDatabaseServer
    class TestSqlValueReader(opus_unittest.OpusTestCase):
        def setUp(self):
            db_server_config = DatabaseServerConfiguration(host_name=os.environ['MYSQLHOSTNAME'],
                                                           user_name=os.environ['MYSQLUSERNAME'], 
                                                           password=os.environ['MYSQLPASSWORD']) 
            
            self.db_server = MysqlDatabaseServer(db_server_config)
            
            self.database_name = 'test_const_taz_cols'
            self.db_server.drop_database(self.database_name)
            self.db_server.create_database(self.database_name)
            self.database = self.db_server.get_database(self.database_name)
    
            self.database.DoQuery("create table constant_taz_columns (`TAZ` int(11), " + 
                                  "`PCTMF` double, `GQI` int(11), `GQN` int(11), " + 
                                  "`FTEUNIV` int(11), `DEN` int(11), `FAZ` int(11), `YEAR` int(11))")
            self.database.DoQuery("insert into constant_taz_columns values " + 
                                  "(1, 19.9, 3, 11, 42, 1, 1, 2000), " + 
                                  "(2, 29.9, 1, 3, 241, 2, 2, 2000), " +
                                  "(1, 99.9, 9, 9, 2419, 29, 29, 2010), " +
                                  "(2, 89.9, 8, 8, 2418, 28, 28, 2010)")
        
        def test_get_constant(self):
            taz_reader = SqlValueReader(self.database, 'constant_taz_columns')
            self.assertEqual(taz_reader.get_value('faz', taz=2, year=2000), 2)
            self.assertEqual(taz_reader.get_value('pctmf', taz=1, year=2000), 19.9)
            self.assertEqual(taz_reader.get_value('gqi', taz=1, year=2000), 3)
            self.assertEqual(taz_reader.get_value('pctmf', taz=1, year=2010), 99.9)
            self.assertEqual(taz_reader.get_value('den', taz=2, year=2010), 28)

        def tearDown(self):
            self.db_server.drop_database(self.database_name)
            self.database.close()
        
if __name__=='__main__':
    opus_unittest.main()