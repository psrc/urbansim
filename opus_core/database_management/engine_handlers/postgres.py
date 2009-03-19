# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.database_management.engine_handlers.abstract_engine import AbstractDatabaseEngineManager
from sqlalchemy import types as sqltypes
import os

try: 
    from sqlalchemy.databases import postgres
        
    class PGGeometry(sqltypes.TypeEngine):
        def get_col_spec(self):
            return "geometry"
            
        def convert_bind_param(self, value, engine):
            return value
            
        def convert_result_value(self, value, engine):
            return value

    postgres.ischema_names['geometry'] = PGGeometry
   
    class PGCascadeSchemaDropper(postgres.PGSchemaDropper):
        def visit_table(self, table):
            for column in table.columns:
                if column.default is not None:
                    self.traverse_single(column.default)
            self.append("\nDROP TABLE " +
                        self.preparer.format_table(table) +
                        " CASCADE")
            self.execute()
    
    postgres.dialect.schemadropper = PGCascadeSchemaDropper

except:
    pass

class PostgresServerManager(AbstractDatabaseEngineManager):
    
    def __init__(self):
        self.uses_schemas = True
        
    def _get_default_database(self, get_existing_db = False):
        if get_existing_db:
            base_database = 'postgres'
        elif 'OPUSPROJECTNAME' not in os.environ:
            base_database = 'misc'
        else:
            base_database = os.environ['OPUSPROJECTNAME']
        return base_database
    
    def get_connection_string(self, server_config, database_name = None, get_base_db = False, scrub = False):
        if scrub:
            password = '**********'
        else:
            password = server_config.password
            
        if get_base_db:
            database_name = self._get_default_database(get_existing_db = True)
        else:
            database_name = self._get_default_database()
        
        connect_string = '%s://%s:%s@%s/%s'%(server_config.protocol, 
                                             server_config.user_name, 
                                             password, 
                                             server_config.host_name, 
                                             database_name) 
        return connect_string            
    
    def _create_real_database(self, server, db_name):
        from psycopg2 import extensions
        server.engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
        qry = 'CREATE DATABASE %s;'%db_name.lower()     
        server.execute(qry)
        
    def create_database(self, server, database_name):
        from psycopg2 import extensions
        server.engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
        qry = 'CREATE SCHEMA %s;'%database_name.lower()     
        server.execute(qry)
        
    def _drop_real_database(self, server, database_name):
        from psycopg2 import extensions
        server.engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
        qry = 'DROP DATABASE %s;'%database_name.lower()     
        server.execute(qry)

    def drop_database(self, server, database_name):
        from psycopg2 import extensions
        server.engine.raw_connection().set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
        qry = 'DROP SCHEMA %s CASCADE;'%database_name.lower()     
        server.execute(qry)

    def has_database(self, server, database_name):
        qry = 'SELECT nspname FROM pg_namespace;'
        result = server.execute(qry)
        dbs = [db[0].lower() for db in result.fetchall()]

        return database_name.lower() in dbs
            
    def _has_real_database(self, server, database_name):
        qry = 'SELECT datname FROM pg_database;'
        result = server.execute(qry)
        dbs = [db[0].lower() for db in result.fetchall()]

        return database_name.lower() in dbs 
    
    def create_default_database_if_absent(self, server_config):
        from opus_core.database_management.database_server import DatabaseServer
        server = DatabaseServer(server_config, creating_base_database = True)
        base_db = self._get_default_database()
        if not self._has_real_database(server = server, 
                                       database_name = base_db):
            self._create_real_database(server, db_name = base_db)
            
    def get_tables_in_database(self, metadata):
        tables = AbstractDatabaseEngineManager.get_tables_in_database(self, metadata)
        tables = [t[t.find('.')+1:] for t in tables]
        return tables    