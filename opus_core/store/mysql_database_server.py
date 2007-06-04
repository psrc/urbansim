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

from opus_core.opus_error import OpusError
from opus_core.store.opus_database import OpusDatabase
from opus_core.store.database_server import DatabaseServer
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.logger import logger
from opus_core.exception.mysqldb_import_exception import MySqlDbImportException
from opus_core.exception.cant_connect_to_mysql_exception import CantConnectToMySqlException

class MysqlDatabaseServer(DatabaseServer):
    """
    New database server that gets all of its info from the 
    configuration.
    """
    def __init__(self, config):
        """
        Return a connection to this database server.
        """
        self.host_name = config.host_name
        self.user_name = config.user_name
        self.password = config.password
        try:
            from MySQLdb import connect
            from MySQLdb import OperationalError            
        except ImportError, e:
            raise MySqlDbImportException(e)    
        try:
            DatabaseServer.__init__(self,
                                connect(host=self.host_name, 
                                        user=self.user_name, 
                                        passwd=self.password))
        except OperationalError, e:
            raise CantConnectToMySqlException(e)

            
        
    def create_database(self, database_name):
        """
        Create this database on this database server.
        """
        self.cursor.execute("CREATE DATABASE %s;" % database_name)

    def drop_database(self, database_name):
        """
        Drop this database.
        """
        # First check if database exists, since MySQL complains even with "if exists".
        if self.has_database(database_name):
            self.cursor.execute("drop database %s" % database_name)

    def get_database(self, database_name, scenario=True):
        """
        Returns an object connecting to this database on this database server.
        
        If the database contains a 'scenario_information' table and the argument 'scenario' is True, 
        return a ScenarioDatabase object.  Else return an OpusDatabase object.
        """
        self.database = OpusDatabase(hostname=self.host_name, 
                                     username=self.user_name, 
                                     password=self.password,
                                     database_name=database_name)
        if scenario and self.database.table_exists('scenario_information'):
            # This is a scenario database, so return one of those objects
            self.database.close()
            self.database = ScenarioDatabase(hostname = self.host_name, 
                                             username = self.user_name, 
                                             password = self.password,
                                             database_name = database_name)
        return self.database
        
    def has_database(self, database_name):
        query = 'show databases like "%s"' % database_name
        self.cursor.execute(query)
        y = []
        results = self.cursor.fetchall()
        map(lambda x: y.append(x[0]), results)
        return database_name in y
    
    __type_name_to_string = {
        'string':'text',
        'integer':'int(11)',
        'float':'float',
        'double':'double',
        'boolean':'int(1)',
        }
    
    def type_string(self, type_name):
        """
        Returns the appropriate string for this type on this database server.
        """
        return self.__type_name_to_string[type_name.lower()]
    
    def close(self):
        """Explicitly close the connection, without waiting for object deallocation"""
        self.cursor.close()
        self.con.close()
        

from opus_core.tests import opus_unittest


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

                     
if __name__ == '__main__':
    opus_unittest.main()