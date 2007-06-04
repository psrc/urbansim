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
from copy import copy

from enthought.traits import Str

from opus_core.configurations.abstract_configuration import AbstractConfiguration
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration


class DatabaseConfiguration(DatabaseServerConfiguration):
    """A DatabaseConfiguration provides the configuration information for a 
    MySQL database, using Traits.  The default values for host_name, user_name, 
    and password are found by looking in the appropriate system variables; if
    the system environment vars are absent some reasonable alternative is 
    used."""

#===============================================================================
#   New Traits
#===============================================================================
    database_name = Str

#===============================================================================
#   Functionality
#===============================================================================

    def __init__(self, database_name, host_name=None, user_name=None, 
            password=None):
                
        self.database_name = database_name

        DatabaseServerConfiguration.__init__(self,
            host_name = host_name,
            user_name = user_name,
            password = password,
            )

#===============================================================================
#   Events
#===============================================================================
    def _database_name_changed(self, new_name):
        pass
        
        
import pickle
from opus_core.tests import opus_unittest


class DatabaseConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_traits(self):
        expected_host_name = os.environ.get('MYSQLHOSTNAME','localhost')
        expected_user_name = os.environ.get('MYSQLUSERNAME','')
        expected_password = os.environ.get('MYSQLPASSWORD','')
        expected_database_name = 'database'

        config = DatabaseConfiguration(
            host_name = expected_host_name,
            user_name = expected_user_name,
            password = expected_password,
            database_name = expected_database_name,
            )
                
        self.assertEqual(
            config.host_name, 
            expected_host_name, 
            "Not getting the value of the environment variable for "
                "MYSQLHOSTNAME."
            )
        self.assertEqual(
            config.user_name, 
            expected_user_name, 
            "Not getting the value of the environment variable for "
                "MYSQLUSERNAME."
            )
        self.assertEqual(
            config.password, 
            expected_password, 
            "Not getting the value of the environment variable for "
                "MYSQLPASSWORD."
            )
        self.assertEqual(
            config.database_name, 
            expected_database_name, 
            "Not getting the expected value of the database."
            )

        expected_host_name = 'host.example.com'
        expected_user_name = 'fred'
        expected_password = 'secretpassword'
        expected_database_name = '%s2' % expected_database_name
        
        config.host_name = expected_host_name
        config.user_name = expected_user_name
        config.password = expected_password
        config.database_name = expected_database_name
        
        self.assertEqual(
            config.host_name, 
            expected_host_name, 
            msg = "Not getting the set host name.")
        self.assertEqual(
            config.user_name, 
            expected_user_name, 
            msg = "Not getting the set user name.")
        self.assertEqual(
            config.password, 
            expected_password, 
            msg = "Not getting the set password.")
        self.assertEqual(
            config.database_name, 
            expected_database_name, 
            msg = "Not getting the set database_name.")
        
        s = pickle.dumps( config )
        unpickled = pickle.loads( s )
        
        self.assertEqual(
            unpickled.host_name, 
            expected_host_name, 
            "Lost host name in pickled version.")
        self.assertEqual(
            unpickled.user_name, 
            expected_user_name,
            "Lost user name in pickled version.")
        self.assertEqual(
            unpickled.password, 
            expected_password,
            "Lost password in pickled version.")
        self.assertEqual(
            unpickled.database_name, 
            expected_database_name,
            "Lost database name in pickled version.")


if __name__=='__main__':
    opus_unittest.main()