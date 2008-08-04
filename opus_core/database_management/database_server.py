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
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine

from opus_core.database_management.engine_handlers.mssql import MSSQLServerManager
from opus_core.database_management.engine_handlers.mysql import MySQLServerManager
from opus_core.database_management.engine_handlers.postgres import PostgresServerManager
from opus_core.database_management.engine_handlers.sqlite import SqliteServerManager

import os


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
        
        if self.protocol == 'postgres':
            self.protocol_manager = PostgresServerManager()
        elif self.protocol == 'mysql':
            self.protocol_manager = MySQLServerManager()
        elif self.protocol == 'sqlite':
            self.protocol_manager = SqliteServerManager()
        elif self.protocol == 'mssql':
            self.protocol_manager = MSSQLServerManager()
            
        self.open()
        self.show_output = False
        self.open_databases = {}
        
        #print self.get_connection_string()
        
    def open(self):

        self.protocol_manager.create_default_database_if_absent(self.config)
        
        self.engine = create_engine(self.get_connection_string(), connect_args={})
        self.metadata = MetaData(
            bind = self.engine
        ) 
        
    def get_connection_string(self, scrub = False):
        return self.protocol_manager.get_connection_string(server_config = self.config,
                                                           scrub = scrub)

    def log_sql(self, sql_query, show_output=False):
        if show_output == True:
            logger.log_status("SQL: " + sql_query, tags=["database"], verbosity_level=3)            
        
    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Does not return data.
        Args;
            query = a SQL statement
        """
        from opus_core.database_management.opus_database import convert_to_mysql_datatype, _log_sql
        engine = self.engine
        preprocessed_query = convert_to_mysql_datatype(query)
        _log_sql(preprocessed_query, self.show_output)
        engine.execute(preprocessed_query)
        
    def create_database(self, database_name):
        """
        Create a database on this database server.
        """
        if not self.has_database(database_name):
            self.protocol_manager.create_database(server = self,
                                                  database_name = database_name)
                       

    def drop_database(self, database_name):
        """
        Drop this database.
        """        
        if self.has_database(database_name):
            if database_name in self.open_databases:
                for db in self.open_databases[database_name]:
                    db.close()
                    
            self.protocol_manager.drop_database(server = self,
                                                database_name = database_name)


    def get_database(self, database_name):
        """
        Returns an object connecting to this database on this database server.
        """
        from opus_core.database_management.opus_database import OpusDatabase
        database = OpusDatabase(
                database_server_configuration = self.config,
                database_name=database_name)
        
        if database_name in self.open_databases:
            self.open_databases[database_name].append(database)
        else:
            self.open_databases[database_name] = [database]
            
        return database
        
    def has_database(self, database_name):
        return self.protocol_manager.has_database(server = self,
                                           database_name = database_name)
       
    
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
        for database_name, dbs in self.open_databases.items():
            for db in dbs:
                try:
                    db.close()
                except:
                    pass
        self.engine.dispose()
        del self.engine
        del self.metadata
        

from opus_core.tests import opus_unittest
from opus_core.database_management.database_server_configuration \
    import DatabaseServerConfiguration, _get_installed_database_engines

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
    
    def get_mssql_server(self):
        server_config = DatabaseServerConfiguration(
            protocol = 'mssql',
            test = True)
        s = DatabaseServer(server_config)     
        return s

    def get_sqlite_server(self):
        server_config = DatabaseServerConfiguration(
            protocol = 'sqlite',
            test = True)
        s = DatabaseServer(server_config)     
        return s
            
    def helper_create_drop_and_has_database(self, db_server):
        db_name = 'test_database_server'
        db_server.drop_database(db_name)
        self.assertFalse(db_server.has_database(db_name))
        
        db_server.create_database(db_name)
        self.assertTrue(db_server.has_database(db_name))
        
        db_server.drop_database(db_name)
        self.assertFalse(db_server.has_database(db_name))
                
    def test_mysql_create_drop_and_has_database(self):
        if 'mysql' in _get_installed_database_engines():
            server = self.get_mysql_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
        
    def test_postgres_create_drop_and_has_database(self):
        if 'postgres' in _get_installed_database_engines():
            server = self.get_postgres_server()
            self.helper_create_drop_and_has_database(server)
            server.close()

    def test_mssql_create_drop_and_has_database(self):
        if 'mssql' in _get_installed_database_engines():
            if not 'MSSQLDEFAULTDB' in os.environ:
                logger.log_warning('MSSQLDEFAULTDB is not set in the environment variables. Skipping test_mssql_create_drop_and_has_database')
            else:
                server = self.get_mssql_server()
                self.helper_create_drop_and_has_database(server)
                server.close()

    def test_sqlite_create_drop_and_has_database(self):
        if 'sqlite' in _get_installed_database_engines():
            server = self.get_sqlite_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
                                                             
if __name__ == '__main__':
    opus_unittest.main()