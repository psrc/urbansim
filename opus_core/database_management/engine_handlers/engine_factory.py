# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.database_management.engine_handlers.postgres import PostgresServerManager
from opus_core.database_management.engine_handlers.mysql import MySQLServerManager
from opus_core.database_management.engine_handlers.sqlite import SqliteServerManager
from opus_core.database_management.engine_handlers.mssql import MSSQLServerManager

class DatabaseEngineManagerFactory(object):
    @staticmethod
    def get_engine(server_config):
        if server_config.protocol == 'postgres':
            return PostgresServerManager()
        elif server_config.protocol == 'mysql':
            return MySQLServerManager()
        elif server_config.protocol == 'sqlite':
            return SqliteServerManager(server_config.sqlite_db_path)
        elif server_config.protocol == 'mssql':
            return MSSQLServerManager()
        else:
            raise Exception("Unknown protocol: '%s" % server_config.protocol)
