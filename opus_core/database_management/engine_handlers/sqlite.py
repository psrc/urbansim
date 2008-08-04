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
import os, fnmatch

class SqliteServerManager(AbstractDatabaseEngineManager):
    
    def __init__(self):
        self.server_path = os.path.join(os.environ['OPUS_HOME'], 'local_databases')
        self.schema_path = os.path.join(self.server_path, self._get_default_database())
        self.os = None
        try:
            self.os = os.uname[0]
        except:
            self.os = 'Windows'
        
        
    def _get_default_database(self):
        if 'OPUSPROJECTNAME' not in os.environ:
            base_database = 'misc'
        else:
            base_database = os.environ['OPUSPROJECTNAME']
        return base_database
    
        
    def _get_database_path(self, database_name):
        return os.path.join(self.schema_path, 
                            database_name + '.txt')

    def get_connection_string(self, server_config, database_name = None, scrub = False):
          
        if not database_name:
            connect_string = 'sqlite://'
        else:
            database_path = self._get_database_path(database_name = database_name)      
            if self.os in ['Darwin']:
                slashes = '////'
            elif self.os in ['Linux', 'Windows']:
                slashes = '///'
            else:
                slashes = '///'
                
            connect_string = 'sqlite:%s%s'%(slashes, database_path)
        
        return connect_string
    
    def create_database(self, server, database_name):
        database_path = self._get_database_path(database_name = database_name) 
        f = open(database_path,'w')
        f.write('')
        f.close()
        
    def drop_database(self, server, database_name):
        database_path = self._get_database_path(database_name = database_name) 
        os.remove(database_path)   

    def has_database(self, server, database_name):
        dbs = [f[:-4] for f in os.listdir(self.schema_path) if fnmatch.fnmatch(f,'*.txt')]
        return database_name in dbs 
    
    def create_default_database_if_absent(self, server_config):
        if not os.path.exists(self.server_path):
            os.mkdir(self.server_path)
        if not os.path.exists(self.schema_path):
            os.mkdir(self.schema_path)
        