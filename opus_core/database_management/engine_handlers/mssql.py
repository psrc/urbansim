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

class MSSQLServerManager(AbstractDatabaseEngineManager):
    
    def _get_default_database(self):
        if 'MSSQLDEFAULTDB' not in os.environ:
            raise Exception('To connect to a Microsoft SQL Server, a default database to connect to must be specified in the environment variables under MSSQLDEFAULTDB')
        self.base_database = os.environ['MSSQLDEFAULTDB']
    
    def get_connection_string(self, server_config, database_name = None, get_base_db = False, scrub = False):
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
    