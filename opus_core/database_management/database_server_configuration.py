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

def _get_installed_database_engines():
    engines = []
    try:
        import MySQLdb
        engines.append('mysql')
    except:
        pass

    try:
        import psycopg2
        engines.append('postgres')
    except:
        pass

    try:
        import pyodbc
        engines.append('mssql')
    except:
        pass

    try:
        import sqlite3
        engines.append('sqlite')
    except:
        pass
    
    return engines

class DatabaseServerConfiguration(object):
    """A DatabaseServerConfiguration provides the connection information 
    for a sql database server.  If use_environment_variables is True, the
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
                 test = False,
                 use_environment_variables = None):
        if use_environment_variables is True:
            self.protocol = os.environ.get('DEFAULT_URBANSIM_DB_ENGINE', self._get_default_database_engine()).lower()
            if self.protocol is None:
                
                self.protocol = self._get_default_database_engine()
            if test:
                self.host_name = os.environ.get('%sHOSTNAMEFORTESTS'%self.protocol.upper(),'localhost')
            else:
                self.host_name = os.environ.get('%sHOSTNAME'%self.protocol.upper(),'localhost')
            self.user_name = os.environ.get('%sUSERNAME'%self.protocol.upper(),'')
            self.password = os.environ.get('%sPASSWORD'%self.protocol.upper(),'') 
        elif use_environment_variables is False:
            self.protocol = protocol.lower()
            self.host_name = host_name
            self.user_name = user_name
            self.password = password
        elif use_environment_variables is None:
            if protocol is None:
                self.protocol = os.environ.get('DEFAULT_URBANSIM_DB_ENGINE', self._get_default_database_engine()).lower()
            else:
                self.protocol = protocol.lower() 
            if host_name is None:
                if test:
                    self.host_name = os.environ.get('%sHOSTNAMEFORTESTS'%self.protocol.upper(),'localhost')
                else:
                    self.host_name = os.environ.get('%sHOSTNAME'%self.protocol.upper(),'localhost')
            else:
                self.host_name = host_name
            if user_name is None:
                self.user_name = os.environ.get('%sUSERNAME'%self.protocol.upper(),'')
            else:
                self.user_name = user_name
            if password is None:
                self.password = os.environ.get('%sPASSWORD'%self.protocol.upper(),'')
            else:
                self.password = password
        else:
            raise ValueError, 'unexpected type for use_environment_variables'
        
    def _get_default_database_engine(self):
        installed_dbs = _get_installed_database_engines()
        if 'mysql' in installed_dbs:
            return 'mysql'
        elif 'sqlite' in installed_dbs:
            return 'sqlite'
        elif 'postgres' in installed_dbs:
            return 'postgres'
        elif 'mssql' in installed_dbs:
            return 'mssql'
        else:
            raise Exception('Cannot find an appropriate database management system to use')
                
    def __repr__(self):
        return '%s://%s:%s@%s'%(self.protocol, self.user_name, self.password, self.host_name) 
    
from opus_core.tests import opus_unittest
class DatabaseServerConfigurationTests(opus_unittest.OpusTestCase):

    def test_attributes(self):
        # Check that have the data to do this unit test.
        for v in ['MYSQLUSERNAME', 'MYSQLHOSTNAME', 'MYSQLPASSWORD']:
            if v not in os.environ :
                print "Skipping tests in file '%s', since %s not defined in environment variables." % (__file__, v)
                return
        
        c1 = DatabaseServerConfiguration(protocol='prot', host_name='h', user_name='fred', 
            password='secret', test=True, use_environment_variables=False)
        self.assertEqual(c1.protocol, 'prot')
        self.assertEqual(c1.host_name, 'h')
        self.assertEqual(c1.user_name, 'fred')
        self.assertEqual(c1.password, 'secret')
        
        c2 = DatabaseServerConfiguration(protocol='MYSQL', host_name='h', user_name='fred', 
            password='secret', test=False, use_environment_variables=True)
        self.assertEqual(c2.protocol, 'mysql')
#        self.assertEqual(c2.host_name, os.environ['MYSQLHOSTNAME'])
#        self.assertEqual(c2.user_name, os.environ['MYSQLUSERNAME'])
#        self.assertEqual(c2.password, os.environ['MYSQLPASSWORD'])
        
        c3 = DatabaseServerConfiguration(protocol='MYSQL', user_name='fred')
        self.assertEqual(c3.protocol, 'mysql')
        self.assertEqual(c3.host_name, os.environ['MYSQLHOSTNAME'])
        self.assertEqual(c3.user_name, 'fred')
        self.assertEqual(c3.password, os.environ['MYSQLPASSWORD'])

        c4 = DatabaseServerConfiguration(protocol = 'mysql')
        self.assertEqual(c4.protocol, 'mysql')
        self.assertEqual(c4.host_name, os.environ['MYSQLHOSTNAME'])
        self.assertEqual(c4.user_name, os.environ['MYSQLUSERNAME'])
        self.assertEqual(c4.password, os.environ['MYSQLPASSWORD'])

if __name__=='__main__':
    opus_unittest.main()
