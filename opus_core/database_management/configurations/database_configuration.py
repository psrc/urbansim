# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

class DatabaseConfiguration(DatabaseServerConfiguration):
    """A DatabaseConfiguration provides the connection information 
    for a sql database server and database.
    If use_environment_variables is True, the
    values for protocol, host_name, user_name, and password are found by looking in 
    the appropriate environment variables; if use_environment_variables is
    False, these values are set to the parameters to the __init__ method.  
    For backwards compatibility, use_environment_variables can also be None.
    In that case, the value of e.g. host_name is either the argument provided if
    the argument is not None, or the environment variable if it is."""

    def __init__(self, 
                 protocol = None, 
                 host_name = None, 
                 user_name = None, 
                 password = None,
                 database_name = None,
                 database_configuration = None,
                 test = False,
                 blob_compression = False):
  
        DatabaseServerConfiguration.__init__(self,
            protocol = protocol,
            host_name = host_name,
            user_name = user_name,
            password = password,
            database_configuration = database_configuration,
            test = test,
            blob_compression = blob_compression
            )      

        self.database_name = database_name
        
    def __repr__(self):
        return '%s://%s:%s@%s/%s'%(self.protocol, 
                                   self.user_name, 
                                   self.password, 
                                   self.host_name, 
                                   self.database_name) 
        
