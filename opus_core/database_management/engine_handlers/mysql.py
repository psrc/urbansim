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

class MySQLServerManager(AbstractDatabaseEngineManager):
    
    def get_connection_string(self, server_config, database_name = None, get_base_db = False, scrub = False):
        if scrub:
            password = '**********'
        else:
            password = server_config.password
            
        connect_string = 'mysql://%s:%s@%s'%(server_config.user_name, password, server_config.host_name) 
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
    