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

from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration


class DatabaseServerConfigurationForTests(DatabaseServerConfiguration):
    """A pre-configured database server configuration referring to localhost."""
    def __init__(self):
        DatabaseServerConfiguration.__init__(self, 
            host_name = os.environ['MYSQLHOSTNAMEFORTESTS'],
            user_name = os.environ['MYSQLUSERNAME'],
            password = os.environ['MYSQLPASSWORD']
            )