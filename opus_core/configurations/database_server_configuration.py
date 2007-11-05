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

from enthought.traits.api import Str
from enthought.traits.api import Bool
from enthought.traits.api import Password

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
    
    get_user_name_from_environment_variable = Bool
    get_host_name_from_environment_variable = Bool
    get_password_from_environment_variable = Bool


#===============================================================================
#   Functionality
#===============================================================================

    def __init__(self, host_name=None, user_name=None, password=None,
                 get_host_name_from_environment_variable=None,
                 get_user_name_from_environment_variable=None,
                 get_password_from_environment_variable=None):
        
        self.env_host_name = os.environ.get('MYSQLHOSTNAME','localhost')
        if host_name is None or get_host_name_from_environment_variable:
            self.host_name = self.env_host_name
        else:
            self.host_name = host_name
        if get_host_name_from_environment_variable is None:
            self.get_host_name_from_environment_variable = host_name is None
        else:
            self.get_host_name_from_environment_variable = get_host_name_from_environment_variable

        self.env_user_name = os.environ.get('MYSQLUSERNAME','')
        if user_name is None or get_user_name_from_environment_variable:
            self.user_name = self.env_user_name
        else:
            self.user_name = user_name
        if get_user_name_from_environment_variable is None:
            self.get_user_name_from_environment_variable = user_name is None
        else:
            self.get_user_name_from_environment_variable = get_user_name_from_environment_variable

        self.env_password = os.environ.get('MYSQLPASSWORD','')
        if password is None or get_password_from_environment_variable:
            self.password = self.env_password
        else:
            self.password = password
        if get_password_from_environment_variable is None:
            self.get_password_from_environment_variable = password is None
        else:
            self.get_password_from_environment_variable = get_password_from_environment_variable

#===============================================================================
#   Events
#===============================================================================

    def _host_name_changed(self, value):
        if value != self.env_host_name:
            self.get_host_name_from_environment_variable = False  

    def _user_name_changed(self, value):
        if value != self.env_user_name:
            self.get_user_name_from_environment_variable = False
        
    def _password_changed(self, value):
        if value != self.env_password:
            self.get_password_from_environment_variable = False

    def _get_user_name_from_environment_variable_changed(self, use_env):
        if use_env:
            self.user_name = self.env_user_name

    def _get_host_name_from_environment_variable_changed(self, use_env):
        if use_env:            
            self.host_name = self.env_host_name

    def _get_password_from_environment_variable_changed(self, use_env):
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
        
        # additional tests for get_host_name_from_environment_variable,
        # get_user_name_from_environment_variable, 
        # and get_password_from_environment_variable
        c2 = DatabaseServerConfiguration(host_name='h', user_name='fred', password='secret',
                 get_host_name_from_environment_variable=False,
                 get_user_name_from_environment_variable=False,
                 get_password_from_environment_variable=False)
        self.assertEqual(c2.host_name, 'h')
        self.assertEqual(c2.user_name, 'fred')
        self.assertEqual(c2.password, 'secret')
        
        c3 = DatabaseServerConfiguration(host_name='h', user_name='fred', password='secret',
                 get_host_name_from_environment_variable=True,
                 get_user_name_from_environment_variable=True,
                 get_password_from_environment_variable=True)
        self.assertEqual(c3.host_name, os.environ['MYSQLHOSTNAME'])
        self.assertEqual(c3.user_name, os.environ['MYSQLUSERNAME'])
        self.assertEqual(c3.password, os.environ['MYSQLPASSWORD'])
        
        c4 = DatabaseServerConfiguration()
        self.assertEqual(c4.host_name, os.environ['MYSQLHOSTNAME'])
        self.assertEqual(c4.user_name, os.environ['MYSQLUSERNAME'])
        self.assertEqual(c4.password, os.environ['MYSQLPASSWORD'])


if __name__=='__main__':
    opus_unittest.main()
