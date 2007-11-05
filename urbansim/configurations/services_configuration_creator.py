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
from enthought.traits.api import HasStrictTraits, Str, Bool, Int, Float, Trait, ListInt
from opus_core.configuration import Configuration


class ServicesConfigurationCreator(HasStrictTraits):
    host_name = Str('localhost')
    user_name = Trait(None, None, Str)
    db_password = Str('')
    get_host_name_from_environment_variable = Bool(True)
    get_user_name_from_environment_variable = Bool(True)
    get_db_password_from_environment_variable = Bool(True)
    database_name = Str('services')
    
    _model_name = 'services_configuration'
    
    def execute(self):
        if self.get_host_name_from_environment_variable:
            host = os.environ.get('MYSQLHOSTNAME')
        else:
            host = self.host_name
        if self.get_user_name_from_environment_variable:
            user = os.environ.get('MYSQLUSERNAME')
        else:
            user = self.user_name
        if self.get_db_password_from_environment_variable:
            pwd = os.environ.get('MYSQLPASSWORD')
        else:
            pwd = self.db_password
        return Configuration({
            'host_name': host,
            'user_name': user,
            'db_password': pwd,
            'database_name': self.database_name,
            })
            

from opus_core.tests import opus_unittest 


class TestServicesConfigurationCreator(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_defaults(self):
        creator = ServicesConfigurationCreator()
        
        expected = Configuration({
            'host_name': os.environ.get('MYSQLHOSTNAME'),
            'user_name': os.environ.get('MYSQLUSERNAME'),
            'db_password': os.environ.get('MYSQLPASSWORD'),
            'database_name':'services',
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = ServicesConfigurationCreator(
            host_name = 'host_name',
            user_name = 'user_name',
            db_password = 'secret',
            database_name = 'database_name',
            get_host_name_from_environment_variable = False,
            get_user_name_from_environment_variable = False,
            get_db_password_from_environment_variable = False
            )
        expected = Configuration({
            'host_name':'host_name',
            'user_name':'user_name',
            'db_password': 'secret',
            'database_name':'database_name',
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
    def test_with_some_arguments(self):
        creator = ServicesConfigurationCreator(
            host_name = 'host_name',
            user_name = 'user_name',
            db_password = 'secret',
            database_name = 'database_name',
            get_host_name_from_environment_variable = True,
            get_user_name_from_environment_variable = False,
            get_db_password_from_environment_variable = False
            )
        expected = Configuration({
            'host_name': os.environ.get('MYSQLHOSTNAME'),
            'user_name':'user_name',
            'db_password': 'secret',
            'database_name':'database_name',
            })
        
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
           
if __name__ == '__main__':
    opus_unittest.main()