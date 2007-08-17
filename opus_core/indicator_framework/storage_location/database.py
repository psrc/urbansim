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

import os

class Database(object):
    """A Database provides the connection information for a sql storage location.  
    The default values for host_name, 
    user_name, and password are found by looking in the appropriate system 
    variables; if the system environment vars are absent some reasonable 
    alternative is used."""

    def __init__(self, 
                 protocol, 
                 database_name,
                 host_name = None, 
                 user_name = None, 
                 password = None):
        
        self.protocol = protocol 
        self.database_name = database_name
        
        if host_name is None:
            self.host_name = os.environ.get('%sHOSTNAME'%protocol.upper(),'localhost')
        else:
            self.host_name = host_name
        
        if user_name is None:
            self.user_name = os.environ.get('%sUSERNAME'%protocol.upper(),'')
        else:
            self.user_name = user_name
        
        if password is None:
            self.env_password = os.environ.get('%sPASSWORD'%protocol.upper(),'')
        else:
            self.password = password
