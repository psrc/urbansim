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
from opus_core.logger import logger
from inprocess.travis.opus_core.exception.database_import_exception import DatabaseImportException
from inprocess.travis.opus_core.exception.cant_connect_to_database_exception import CantConnectToDatabaseException
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine


class DatabaseServer(object):
    """
    Handles all non-transactional queries to the database server. 
    Will also return a connection to a specific database. 
    """
    def __init__(self, database_server_configuration):
        """
        Connects to this database server.
        """
        self.config = database_server_configuration
        
        self.protocol = database_server_configuration.protocol
        self.host_name = database_server_configuration.host_name
        self.user_name = database_server_configuration.user_name
        self.password = database_server_configuration.password
        
        try:
            engine = create_engine(self.get_connection_string())
            self.metadata = MetaData(
                bind = engine
            )      
        except Exception, e:
            raise DatabaseImportException(e)    
                
        try:
            self.cursor = engine.connect()
            self.show_output = False
        except Exception, e:
            raise CantConnectToDatabaseException(e)

    def get_connection_string(self):
        return '%s://%s:%s@%s'%(self.protocol, self.user_name, self.password, self.host_name) 
    
    def log_sql(self, sql_query, show_output=False):
        if show_output == True:
            logger.log_status("SQL: " + sql_query, tags=["database"], verbosity_level=3)            
        
    def create_database(self, database_name):
        """
        Create a database on this database server.
        """
        if self.protocol in ['mysql', 'mssql']: #mssql is untested
            self.cursor.execute('''
                CREATE DATABASE %s;
            '''%database_name)
        elif self.protocol == 'postgres': #in postgres, need to end the transaction first
            self.cursor.execute('''
                END;
                CREATE DATABASE %s;
            '''%database_name)            

    def drop_database(self, database_name):
        """
        Drop this database.
        """
        # First check if database exists
        if self.has_database(database_name):
            self.cursor.execute('''
                DROP DATABASE %s
            '''%database_name)

    def get_database(self, database_name, scenario=True):
        """
        Returns an object connecting to this database on this database server.
        
        If the database contains a 'scenario_information' table and the argument 'scenario' is True, 
        return a ScenarioDatabase object.  Else return an OpusDatabase object.
        """
        from inprocess.travis.opus_core.database_management.opus_database import OpusDatabase
        database = OpusDatabase(
                database_server_config = self.config,
                database_name=database_name)
        
        if scenario and database.table_exists('scenario_information'):
            from inprocess.travis.opus_core.database_management.scenario_database import ScenarioDatabase
            database = ScenarioDatabase(
                database_server_config = self.config,
                database_name = database_name)
        return database
        
    def has_database(self, database_name):
        #sqlalchemy doesn't really support database management at the server level...
        if self.protocol == 'mysql':
            query = '''
                SHOW DATABASES LIKE '%s'
            '''%database_name
        elif self.protocol == 'postgres':
            query = '''
                SELECT datname FROM pg_database;
            '''
        elif self.protocol == 'mssql': #note: this is untested
            query = 'sp_databases'
        #TODO: add other protocols
        
        result = self.cursor.execute(query)
        dbs = [db[0] for db in result.fetchall()]
        return database_name in dbs
    
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
        

from opus_core.tests import opus_unittest
from inprocess.travis.opus_core.configurations.database_server_configuration \
    import DatabaseServerConfiguration

class Tests(opus_unittest.OpusTestCase):
        
    def get_mysql_server(self):
        server_config = DatabaseServerConfiguration(
            protocol = 'mysql',
            test = True)
        return DatabaseServer(server_config) 
    
    def get_postgres_server(self):
        server_config = DatabaseServerConfiguration(
            protocol = 'postgres',
            test = True)
        return DatabaseServer(server_config) 
    
    def helper_create_drop_and_has_database(self, db_server):
        db_name = 'test_database_server'
        self.assertFalse(db_server.has_database(db_name))
        
        db_server.create_database(db_name)
        self.assertTrue(db_server.has_database(db_name))
        
        db_server.drop_database(db_name)
        self.assertFalse(db_server.has_database(db_name))
                
    def test_mysql_create_drop_and_has_database(self):
        try:
            import MySQLdb
        except:
            pass
        else:
            server = self.get_mysql_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
        
    def test_postgres_create_drop_and_has_database(self):
        try:
            import psycopg2
        except:
            pass
        else:
            server = self.get_postgres_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
                                 
if __name__ == '__main__':
    opus_unittest.main()