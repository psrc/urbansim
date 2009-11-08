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
from enthought.traits import Bool
from enthought.traits import Password

from opus_core.configurations.abstract_configuration import AbstractConfiguration

class DatabaseServerConfiguration(AbstractConfiguration):
    """A DatabaseServerConfiguration provides the configuration information for  
    a MySQL database, using Traits.  The default values for host_name, 
    user_name, and password are found by looking in the appropriate system 
    variables; if the system environment vars are absent some reasonable 
    alternative is used."""

#===============================================================================
#   Traits
#===============================================================================

    host_name = Str
    user_name = Str
    password = Password
    
    use_environment_variable_for_user_name = Bool
    use_environment_variable_for_host_name = Bool
    use_environment_variable_for_password = Bool


#===============================================================================
#   Functionality
#===============================================================================

    def __init__(self, host_name=None, user_name=None, password=None):
        self.env_host_name = os.environ.get('MYSQLHOSTNAME','localhost')
        if host_name is None:
            self.host_name = self.env_host_name # Redundant --
            self.use_environment_variable_for_host_name = True # because of this
                    # -- but whatever.
        else:
            self.host_name = host_name
        
        self.env_user_name = os.environ.get('MYSQLUSERNAME','')
        if user_name is None:
            self.user_name = self.env_user_name # Ditto.
            self.use_environment_variable_for_user_name = True
        else:
            self.user_name = user_name
        
        self.env_password = os.environ.get('MYSQLPASSWORD','')
        if password is None:
            self.env_password = self.env_password # Ditto.
            self.use_environment_variable_for_password = True
        else:
            self.password = password
        

#===============================================================================
#   Events
#===============================================================================

    def _host_name_changed(self, value):
        if value != self.env_host_name:
            self.use_environment_variable_for_host_name = False  

    def _user_name_changed(self, value):
        if value != self.env_user_name:
            self.use_environment_variable_for_user_name = False
        
    def _password_changed(self, value):
        if value != self.env_password:
            self.use_environment_variable_for_password = False

    def _use_environment_variable_for_user_name_changed(self, use_env):
        if use_env:
            self.user_name = self.env_user_name

    def _use_environment_variable_for_host_name_changed(self, use_env):
        if use_env:            
            self.host_name = self.env_host_name

    def _use_environment_variable_for_password_changed(self, use_env):
        if use_env:
            self.password = self.env_password
    

class LocalhostDatabaseServerConfiguration(DatabaseServerConfiguration):
    """A pre-configured database server configuration referring to localhost."""
    def __init__(self):
        DatabaseServerConfiguration.__init__(self, 
                                             host_name='localhost',
                                             user_name=os.environ['MYSQLUSERNAME'],
                                             password=os.environ['MYSQLPASSWORD'])

import pickle
from opus_core.tests import opus_unittest


class DatabaseServerConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_traits(self):
        # Check that have the data to do this unit test.
        if 'MYSQLUSERNAME' not in os.environ or 'MYSQLHOSTNAME' not in os.environ:
            print "Skipping tests in file '%s', since MYSQLUSERNAME or MYSQLHOSTNAME not defined in environment variables." % __file__
            return
        
        config = LocalhostDatabaseServerConfiguration()
                
        self.assertEqual(config.host_name, 'localhost', 
            "Not getting the value of the environment variable for "
                "MYSQLHOSTNAME."
            )
        self.assertEqual(config.user_name, os.environ['MYSQLUSERNAME'], 
            "Not getting the value of the environment variable for "
                "MYSQLUSERNAME."
            )
        self.assertEqual(config.password, os.environ['MYSQLPASSWORD'], 
            "Not getting the value of the environment variable for "
                "MYSQLPASSWORD."
            )

        expected_host_name = 'host.example.com'
        expected_user_name = 'fred'
        expected_password = 'secretpassword'
        
        config.host_name = expected_host_name
        config.user_name = expected_user_name
        config.password = expected_password
        
        self.assertEqual( config.host_name, expected_host_name, 
            msg = "Not getting the set host name.")
        self.assertEqual( config.user_name, expected_user_name, 
            msg = "Not getting the set user name.")
        self.assertEqual( config.password, expected_password, 
            msg = "Not getting the set password.")
        
        s = pickle.dumps( config )
        unpickled = pickle.loads( s )
        
        self.assertEqual(unpickled.host_name, expected_host_name, 
            "Lost host name in pickled version.")
        self.assertEqual(unpickled.user_name, expected_user_name,
            "Lost user name in pickled version.")
        self.assertEqual(unpickled.password, expected_password,
            "Lost password in pickled version.")


if __name__=='__main__':
    opus_unittest.main()
