# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from xml.etree.cElementTree import ElementTree

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

def get_default_database_engine():
    installed_dbs = _get_installed_database_engines()
    if 'sqlite' in installed_dbs:
        return 'sqlite'
    elif 'mysql' in installed_dbs:
        return 'mysql'
    elif 'postgres' in installed_dbs:
        return 'postgres'
    elif 'mssql' in installed_dbs:
        return 'mssql'
    else:
        raise Exception('Cannot find an appropriate database management system to use')
        
class DatabaseServerConfiguration(object):
    """A DatabaseServerConfiguration provides the connection information 
    for a sql database server."""

    PROTOCOL_TAG = 'protocol'
    HOST_NAME_TAG = 'host_name'
    USER_NAME_TAG = 'user_name'
    PASSWORD_TAG = 'password'
    
    def __init__(self, 
                 protocol = None, 
                 host_name = None, 
                 user_name = None, 
                 password = None,
                 database_configuration = None,
                 test = False,
                 database_server_configuration_file_path = None,
                 sqlite_db_path = None):
        
        if database_server_configuration_file_path is None:
            database_server_configuration_file_path = os.path.join(os.environ['OPUS_HOME'], 'settings', 'database_server_configurations.xml')

        if (protocol is None or test) and host_name is None and user_name is None and password is None:
            if not os.path.exists(database_server_configuration_file_path):
                raise Exception('You do not have a file %s storing information about your database server configurations. Cannot load database.'%database_server_configuration_file_path)
            if database_configuration is None:
                db_node = self._database_configuration_node()
            else:
                db_node = database_configuration
            database_configuration = ElementTree(file = database_server_configuration_file_path).getroot().find(db_node)
            if database_configuration is None:
                raise Exception('Could not find an entry in %s for %s. Cannot load database.'%(database_server_configuration_file_path, db_node))
            self.protocol = database_configuration.find(self.PROTOCOL_TAG).text
            self.host_name = database_configuration.find(self.HOST_NAME_TAG).text
            self.user_name = database_configuration.find(self.USER_NAME_TAG).text
            self.password = database_configuration.find(self.PASSWORD_TAG).text
    
        else:
            if protocol is None:
                self.protocol = get_default_database_engine()
            else:
                self.protocol = protocol.lower()
                 
            if host_name is None:
                self.host_name = 'localhost'
            else:
                self.host_name = host_name
    
            if user_name is None:
                self.user_name = ''
            else:
                self.user_name = user_name
    
            if password is None:
                self.password = ''
            else:
                self.password = password
                
        # If the password is the empty string or None, check if it is defined in the environment variable
        # SQLPASSWORD - if so, use that.
        if (self.password is None or self.password=='') and 'SQLPASSWORD' in os.environ:
            self.password = os.environ['SQLPASSWORD']

        self.sqlite_db_path = sqlite_db_path
                
    def __repr__(self):
        return '%s://%s:%s@%s'%(self.protocol, self.user_name, self.password, self.host_name) 

    def _database_configuration_node(self):
        raise Exception('You need to provide real parameters to the server configuration object.')   
    
from opus_core.tests import opus_unittest
class DatabaseServerConfigurationTests(opus_unittest.OpusTestCase):

    def test_attributes(self):
        from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
        
        c1 = TestDatabaseConfiguration(protocol='prot', host_name='h', user_name='fred', 
            password='secret')
        self.assertEqual(c1.protocol, 'prot')
        self.assertEqual(c1.host_name, 'h')
        self.assertEqual(c1.user_name, 'fred')
        self.assertEqual(c1.password, 'secret')

        c3 = TestDatabaseConfiguration(protocol = 'mysql', user_name = 'fred')
        self.assertEqual(c3.protocol, 'mysql')
        self.assertEqual(c3.host_name, 'localhost')
        self.assertEqual(c3.user_name, 'fred')
        self.assertEqual(c3.password, os.environ.get('SQLPASSWORD', ''))


    def test_exceptions(self):
        self.assertRaises(Exception, DatabaseServerConfiguration)        

        
        
if __name__=='__main__':
    opus_unittest.main()
