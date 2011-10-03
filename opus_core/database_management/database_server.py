# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine

import os
from opus_core.database_management.engine_handlers.engine_factory import DatabaseEngineManagerFactory


class DatabaseServer(object):
    """
    Handles all non-transactional queries to the database server. 
    Will also return a connection to a specific database. 
    """
    def __init__(self, database_server_configuration, creating_base_database = False):
        """
        Connects to this database server.
        """
        self.config = database_server_configuration
        
        self.protocol_manager = DatabaseEngineManagerFactory.get_engine(database_server_configuration)
            
        self.open(creating_base_database)
        self.show_output = False
        self.open_databases = {}
        
        #print self.get_connection_string()
        
    def open(self, creating_base_database = False):

        if not creating_base_database:
            self.protocol_manager.create_default_database_if_absent(self.config)
            connect_string = self.get_connection_string()
        else:
            connect_string = self.get_connection_string(get_base_db = True)
            
        self.engine = create_engine(connect_string, connect_args={})
        self.metadata = MetaData(
            bind = self.engine
        ) 
        
    def get_connection_string(self, get_base_db = False, scrub = False):
        return self.protocol_manager.get_connection_string(server_config = self.config,
                                                           get_base_db = get_base_db,
                                                           scrub = scrub)

    def log_sql(self, sql_query):
        logger.log_status("SQL: " + sql_query, tags=["database"], verbosity_level=3)            
        
    def execute(self, query):
        try:
            result = self.engine.execute(query)
        except:
            print query
            raise
        return result
        
    '''Deprecated: DO NOT USE'''
    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Does not return data.
        Args;
            query = a SQL statement
        """
        from opus_core.database_management.opus_database import convert_to_mysql_datatype, _log_sql
        preprocessed_query = convert_to_mysql_datatype(query)
        if self.show_output:
            _log_sql(preprocessed_query)
        self.execute(preprocessed_query)
        
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

    def get_database(self, database_name, create_if_doesnt_exist = True):
        """
        Returns an object connecting to this database on this database server.
        """
        from opus_core.database_management.opus_database import OpusDatabase
        
        if create_if_doesnt_exist:
            self.create_database(database_name = database_name)
            
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
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration, get_testable_engines

class Tests(opus_unittest.OpusTestCase):
        
    def get_mysql_server(self):
        server_config = TestDatabaseConfiguration(
            protocol = 'mysql')
        return DatabaseServer(server_config) 
    
    def get_postgres_server(self):
        server_config = TestDatabaseConfiguration(
            protocol = 'postgres')
        return DatabaseServer(server_config) 
    
    def get_mssql_server(self):
        server_config = TestDatabaseConfiguration(
            protocol = 'mssql')
        s = DatabaseServer(server_config)     
        return s

    def get_sqlite_server(self):
        server_config = TestDatabaseConfiguration(
            protocol = 'sqlite')
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
        if 'mysql' in get_testable_engines():
            server = self.get_mysql_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
    #TODO: turn it on when postgres is properly set up
    def MASKtest_postgres_create_drop_and_has_database(self):
        if 'postgres' in get_testable_engines():
            server = self.get_postgres_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
    #TODO: turn it on when mssql is properly set up
    def MASKtest_mssql_create_drop_and_has_database(self):
        if 'mssql' in get_testable_engines():
            if not 'MSSQLDEFAULTDB' in os.environ:
                logger.log_warning('MSSQLDEFAULTDB is not set in the environment variables. Skipping test_mssql_create_drop_and_has_database')
            else:
                server = self.get_mssql_server()
                self.helper_create_drop_and_has_database(server)
                server.close()

    def test_sqlite_create_drop_and_has_database(self):
        if 'sqlite' in get_testable_engines():
            server = self.get_sqlite_server()
            self.helper_create_drop_and_has_database(server)
            server.close()
                                                             
if __name__ == '__main__':
    opus_unittest.main()