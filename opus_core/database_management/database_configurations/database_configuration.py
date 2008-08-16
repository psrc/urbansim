#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

import os
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration

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
                 test = False,
                 use_environment_variables = None):
  
        DatabaseServerConfiguration.__init__(self,
            protocol = protocol,
            host_name = host_name,
            user_name = user_name,
            password = password,
            test = test,
            use_environment_variables = use_environment_variables
            )      

        self.database_name = database_name
        
    def __repr__(self):
        return '%s://%s:%s@%s/%s'%(self.protocol, 
                                   self.user_name, 
                                   self.password, 
                                   self.host_name, 
                                   self.database_name) 