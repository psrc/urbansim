# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.database_management.engine_handlers.abstract_engine import AbstractDatabaseEngineManager
import os

class MSSQLServerManager(AbstractDatabaseEngineManager):
    def __init__(self, server_config):
        AbstractDatabaseEngineManager.__init__(self, server_config)
    
    def _get_default_database(self):
        if 'MSSQLDEFAULTDB' not in os.environ:
            raise Exception('To connect to a Microsoft SQL Server, a default database to connect to must be specified in the environment variables under MSSQLDEFAULTDB')
        self.base_database = os.environ['MSSQLDEFAULTDB']
    
    def get_connection_string(self, database_name = None, get_base_db = False, scrub = False):
        server_config = self.server_config
        if scrub:
            password = '**********'
        else:
            password = server_config.password
            
        if not database_name:
            database_name = self._get_default_database()
            
        if password is not None:        
            connect_string = '%s://%s:%s@%s/%s'%(server_config.protocol, 
                                                 server_config.user_name, 
                                                 password, 
                                                 server_config.host_name, 
                                                 database_name) 
        else:
            connect_string = '%s://%s@%s/%s'%(server_config.protocol, 
                                                 server_config.user_name, 
                                                 server_config.host_name, 
                                                 database_name) 

        return connect_string            
    
    def create_database(self, server, database_name):
        qry = 'CREATE DATABASE %s;'%database_name
        server.execute(qry)
        
    def drop_database(self, server, database_name):
        qry = 'DROP DATABASE %s;'%database_name
        server.execute(qry)   
        
    def has_database(self, server, database_name):
        import pyodbc
        conn = 'DRIVER={SQL Server};SERVER=%(server)s;DATABASE=%(database)s;UID=%(UID)s;PWD=%(PWD)s'% \
                           {'UID':server.user_name, 
                           'PWD':server.password,
                           'server':server.host_name, 
                           'database':self._get_default_database()}
        c = pyodbc.connect(conn)
        
        dbs = [d[0] for d in c.execute('EXEC sp_databases').fetchall()]
        c.close()
        del c
        
        return database_name in dbs 
    
    def create_default_database_if_absent(self, server_config):
        pass
    
    def get_tables_in_database(self, metadata):
        tables = AbstractDatabaseEngineManager.get_tables_in_database(self, metadata)
        # MSSQL hacking by Jesse
        # The three items in mssql_system_tables are tables (and views) created in
        # every MSSQL database.  A user should never need to cache or otherwise
        # work with these tables in OPUS (as far as I know), so I am filtering them 
        # out here.
        mssql_system_tables = [u'sysconstraints', u'dtproperties', u'syssegments']
        for i in mssql_system_tables:
            if i in tables:
                tables.remove(i)        
        return tables
    