# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.database_management.engine_handlers.abstract_engine import AbstractDatabaseEngineManager

class MySQLServerManager(AbstractDatabaseEngineManager):
    
    def get_connection_string(self, server_config, database_name = None, get_base_db = False, scrub = False):
        if scrub:
            password = '**********'
        else:
            password = server_config.password
            
        if password is not None:
            connect_string = 'mysql://%s:%s@%s'%(server_config.user_name, password, server_config.host_name) 
        else:
            connect_string = 'mysql://%s@%s'%(server_config.user_name, server_config.host_name) 

        if database_name:
            connect_string += '/%s'%(database_name) 

        return connect_string
    
    def create_database(self, server, database_name):
        qry = 'CREATE DATABASE %s;'%database_name
        server.execute(qry)
        
    def drop_database(self, server, database_name):
        qry = 'DROP DATABASE %s;'%database_name
        server.execute(qry)

    def has_database(self, server, database_name):
        qry = 'SHOW DATABASES LIKE "%s"'%database_name
        result = server.execute(qry)
        dbs = [db[0] for db in result.fetchall()]

        return database_name in dbs 
    
    def create_default_database_if_absent(self, server_config):
        pass
    