# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

class ServicesDatabaseConfiguration(DatabaseConfiguration):

    def __init__(self, 
                 protocol = None,
                 host_name = None,
                 user_name = None,
                 password = None,
                 database_name = None,
                 database_configuration = None):
        if database_name is None:
            database_name = 'services'
        DatabaseConfiguration.__init__(self,
                              protocol = protocol,
                              host_name = host_name,
                              user_name = user_name,
                              password = password,
                              database_name = database_name,
                              database_configuration = database_configuration)
        
    def _database_configuration_node(self):
        return 'services_database_server'   
    
if __name__ == '__main__':
    config = ServicesDatabaseConfiguration()
#   print config