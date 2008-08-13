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
from opus_core.configuration import Configuration


class ServicesConfigurationCreator(object):    
    _model_name = 'services_configuration'
    
    def __init__(self,
                host_name = 'localhost',
                user_name = None,
                db_password = '',
                use_environment_variables = True,
                database_name = 'services'):
        self.host_name = host_name
        self.user_name = user_name
        self.db_password = db_password
        self.use_environment_variables = use_environment_variables
        self.database_name = database_name
        
    def execute(self):
        if self.use_environment_variables:
            host = os.environ.get('MYSQLHOSTNAME')
            user = os.environ.get('MYSQLUSERNAME')
            pwd = os.environ.get('MYSQLPASSWORD')
        else:
            host = self.host_name
            user = self.user_name
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
            'database_name':'services'})
        result = creator.execute()
        self.assertDictsEqual(result, expected)
        
    def test_with_arguments(self):
        creator = ServicesConfigurationCreator(
            host_name = 'host_name',
            user_name = 'user_name',
            db_password = 'secret',
            database_name = 'database_name',
            use_environment_variables = False
            )
        expected = Configuration({
            'host_name':'host_name',
            'user_name':'user_name',
            'db_password': 'secret',
            'database_name':'database_name'})
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
    def test_with_arguments_use_env_vars(self):
        # supply arguments, but use environment variables anyway
        creator = ServicesConfigurationCreator(
            host_name = 'host_name',
            user_name = 'user_name',
            db_password = 'secret',
            database_name = 'database_name',
            use_environment_variables = True
            )
        expected = Configuration({
            'host_name': os.environ.get('MYSQLHOSTNAME'),
            'user_name': os.environ.get('MYSQLUSERNAME'),
            'db_password': os.environ.get('MYSQLPASSWORD'),
            'database_name':'database_name'})
        result = creator.execute()
        self.assertDictsEqual(result, expected)
            
           
if __name__ == '__main__':
    opus_unittest.main()