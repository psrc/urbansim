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

from opus_core.database_management.engine_handlers.abstract_engine import AbstractDatabaseEngineManager
import os

class PostgresServerManager(AbstractDatabaseEngineManager):
    
    def _get_default_database(self):
        if 'OPUSPROJECTNAME' not in os.environ:
            base_database = 'postgres'
        else:
            base_database = os.environ['OPUSPROJECTNAME']
        return base_database
    
    def get_connection_string(self, server_config, database_name = None, scrub = False):
        if scrub:
            password = '**********'
        else:
            password = server_config.password
            
        if not database_name:
            database_name = self._get_default_database()
        
        connect_string = '%s://%s:%s@%s/%s'%(server_config.protocol, 
                                             server_config.user_name, 
                                             password, 
                                             server_config.host_name, 
                                             database_name) 
        return connect_string            
    
    def create_database(self, server, database_name):
        qry = 'END;CREATE DATABASE %s;'%database_name.lower()     
        server.engine.execute(qry)
        
    def drop_database(self, server, database_name):
        qry = 'END;DROP DATABASE %s;'%database_name.lower()     
        server.engine.execute(qry)

    def has_database(self, server, database_name):
        qry = 'SELECT datname FROM pg_database;'
        result = server.engine.execute(qry)
        dbs = [db[0].lower() for db in result.fetchall()]

        return database_name.lower() in dbs 
    
    def create_default_database_if_absent(self, server_config):
        pass
    