# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

class AbstractDatabaseEngineManager(object):
    
    def __init__(self):
        self.uses_schemas = False
        
    def get_connection_string(self, database_name = None, scrub = False):
        raise Exception('method not implemented')
    
    def create_database(self, engine, database_name):
        raise Exception('method not implemented')
        
    def drop_database(self, engine, database_name):
        raise Exception('method not implemented')
    
    def has_database(self, engine, database_name):
        raise Exception('method not implemented')
    
    def create_default_database_if_absent(self, server_config):
        raise Exception('method not implemented')
    
    def get_tables_in_database(self, metadata):
        return metadata.tables.keys()