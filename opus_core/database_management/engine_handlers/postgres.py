# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.database_management.engine_handlers.abstract_engine import AbstractDatabaseEngineManager
from sqlalchemy import types as sqltypes
import os
from sqlalchemy.exc import ProgrammingError
from opus_core.logger import logger
import re

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
    
    def __init__(self, server_config):
        AbstractDatabaseEngineManager.__init__(self, server_config)
        self.uses_schemas = False
        
    def _get_default_database(self, force_database_name = None):
        if force_database_name is not None:
            return force_database_name
        
        _, database_name = self._split_host_name()

        if database_name is not None:
            if database_name == '':
                base_database = self.server_config.user_name
            else:
                base_database = database_name
        elif 'OPUSPROJECTNAME' not in os.environ:
            base_database = 'misc'
        else:
            base_database = os.environ['OPUSPROJECTNAME']
        return base_database
    
    def _split_host_name(self):
        if self.server_config.host_name is None:
            return '', None
        m = re.match(r'^([^/]+)(?:|/([^/]+))$', self.server_config.host_name)
        return m.group(1), m.group(2)

    def get_connection_string(self, database_name = None, get_base_db = False, scrub = False):
        server_config = self.server_config
        if scrub:
            password = '**********'
        else:
            password = server_config.password
        
        host_name, _ = self._split_host_name()
        if get_base_db:
            database_name = self._get_default_database('postgres')
        else:
            database_name = self._get_default_database(database_name)
        
        connect_string = '%s://%s:%s@%s/%s'%(server_config.protocol, 
                                             server_config.user_name, 
                                             password, 
                                             host_name,
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
            try:
                self._create_real_database(server, db_name = base_db)
            except ProgrammingError, e:
                logger.log_warning('Failed to create default database %s:\n%s' % (base_db, str(e)))
            
    def get_tables_in_database(self, metadata):
        tables = AbstractDatabaseEngineManager.get_tables_in_database(self, metadata)
        tables = [t[t.find('.')+1:] for t in tables]
        return tables    