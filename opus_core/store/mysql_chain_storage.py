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

import re

from opus_core.store.storage import Storage
from opus_core.logger import logger
from opus_core.store.mysql_storage import mysql_storage as _mysql_storage


class mysql_chain_storage(Storage):
    def __init__(self, hostname=None, username=None, password=None, 
                 database_name=None, print_status_chunk_size=1000):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._database_name = database_name
        
        self._print_status_chunk_size = print_status_chunk_size
        
        self.__database_name_for_table_name = None

    def get_table_names(self):
        return self._get_table_name_to_database_name_mapping().keys()

    def get_column_names(self, table_name, lowercase=True):
        mysql_storage_for_database = self._get_mysql_storage_for_table(table_name)
        return mysql_storage_for_database.get_column_names(table_name)
        
    def determine_field_names(self, load_resources, attributes='*'):
        in_table_name = load_resources['in_table_name']
        return self.get_column_names(in_table_name)
    
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True, id_name=None):
        mysql_storage_for_database = self._get_mysql_storage_for_table(table_name)
        return mysql_storage_for_database.load_table(table_name, column_names=column_names, lowercase=lowercase, id_name=id_name)

    def _get_mysql_storage_for_table(self, table_name):
        if table_name in self._get_table_name_to_database_name_mapping():
            database_name = self._get_table_name_to_database_name_mapping()[table_name]
            return self._get_mysql_storage_for_database(database_name)
        
        raise LookupError("Table '%s' not found in database chain!"
            % table_name)
        
    def _get_mysql_storage_for_database(self, database_name):
        return _mysql_storage( 
            username = self._username, 
            password = self._password,
            hostname = self._hostname,
            database_name = database_name
            )
        
    def _get_table_name_to_database_name_mapping(self):
        if self.__database_name_for_table_name is None:
            self.__database_name_for_table_name = {}
            self._create_database_name_for_table_name_mapping(self._database_name)
        return self.__database_name_for_table_name
        
    def _create_database_name_for_table_name_mapping(self, database_name):
        from MySQLdb import connect
        
        db = connect(host = self._hostname, 
                     user = self._username, 
                     passwd = self._password, 
                     db = database_name)
        try:
            cursor = db.cursor()
            
            while True: # until there are no more databases to check in this chain
                cursor.execute("USE %s" % database_name)
                cursor.execute("SHOW TABLES;")
                
                rows = cursor.fetchall()
                for row in rows:
                    table_name = row[0]
                    
                    mapping = self._get_table_name_to_database_name_mapping()
                    if table_name not in mapping:
                        mapping[table_name] = database_name
                                           
                try:
                    cursor.execute("SELECT PARENT_DATABASE_URL FROM scenario_information;")
                    
                except:
                    break
                
                rows = cursor.fetchall()
                
                if (not rows[0][0]) or (len(rows[0][0]) < 1) :
                    # no more parents to traverse
                    break
                    
                match = re.search("jdbc:mysql://[^/]*/(.*)", rows[0][0])
                if match == None :
                    raise ValueError("parent database url is not a MySQL JDBC url" )
                    
                database_name = match.group(1)
                
        finally:
            cursor.close()
            db.close()
        

from opus_core.tests import opus_unittest

import os

from sets import Set

from numpy import array

from opus_core.configurations.database_server_configuration import LocalhostDatabaseServerConfiguration
from opus_core.store.mysql_database_server import MysqlDatabaseServer


class TestMysqlChainStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        db_server = MysqlDatabaseServer(LocalhostDatabaseServerConfiguration())
        
        db_server.drop_database('database_a')
        db_server.create_database('database_a')
        database = db_server.get_database('database_a')
        database.DoQuery('CREATE TABLE table_a1 (a INT)')
        database.DoQuery('CREATE TABLE scenario_information (parent_database_url varchar(255))')
        database.DoQuery('INSERT INTO scenario_information (parent_database_url) VALUES ("jdbc:mysql://localhost/database_b")')
        
        db_server.drop_database('database_b')
        db_server.create_database('database_b')
        database = db_server.get_database('database_b')
        database.DoQuery('CREATE TABLE table_b1 (a INT, b INT, c INT)')
        database.DoQuery('INSERT INTO table_b1 (a, b, c) VALUES (100, 200, 300)')
        database.DoQuery('INSERT INTO table_b1 (a, b, c) VALUES (400, 500, 600)')
        database.DoQuery('CREATE TABLE table_b2 (a INT)')
        database.DoQuery('CREATE TABLE scenario_information (parent_database_url varchar(255))')
        database.DoQuery('INSERT INTO scenario_information (parent_database_url) VALUES ("jdbc:mysql://localhost/database_c")')
        
        db_server.drop_database('database_c')
        db_server.create_database('database_c')
        database = db_server.get_database('database_c')
        database.DoQuery('CREATE TABLE table_c1 (a INT)')
        database.DoQuery('CREATE TABLE table_c2 (a INT, b INT)')
        database.DoQuery('INSERT INTO table_c2 (a, b) VALUES (100, 300)')
        database.DoQuery('CREATE TABLE table_b1 (a INT)')
        
        # not in chain
        db_server.drop_database('database_d')
        db_server.create_database('database_d')
        database = db_server.get_database('database_d')
        database.DoQuery('CREATE TABLE table_d1 (a INT)')
        database.DoQuery('INSERT INTO table_d1 (a) VALUES (200)')
        database.DoQuery('CREATE TABLE table_d2 (a INT)')
        database.DoQuery('CREATE TABLE table_d3 (a INT)')
        
        # empty parent_database_url
        db_server.drop_database('database_e')
        db_server.create_database('database_e')
        database = db_server.get_database('database_e')
        database.DoQuery('CREATE TABLE scenario_information (parent_database_url varchar(255))')
        database.DoQuery('INSERT INTO scenario_information (parent_database_url) VALUES ("")')
        
        # empty database
        db_server.drop_database('database_f')
        db_server.create_database('database_f')
    
    def tearDown(self):
        pass
    
    def _get_mysql_chain_storage_for_localhost_database(self, database_name):
        return mysql_chain_storage(
            hostname = 'localhost',
            username = os.environ['MYSQLUSERNAME'],
            password = os.environ['MYSQLPASSWORD'],
            database_name = database_name,
            )
    
    def test__get_mysql_storage_for_database(self):
        chain_storage = mysql_chain_storage(
            hostname = 'mock.hostname',
            username = 'mock.username',
            password = '******',
            database_name = 'database_c',
            )
        
        storage = chain_storage._get_mysql_storage_for_database('database_c')
        self.assertEqual('mock.username: mysql://mock.hostname/database_c', storage.get_storage_location())
        
    def test__get_mysql_storage_for_different_database(self):
        chain_storage = mysql_chain_storage(
            hostname = 'mock.hostname2',
            username = 'mock.username2',
            password = '******2',
            database_name = 'database_c2',
            )
        
        storage = chain_storage._get_mysql_storage_for_database('database_c2')
        self.assertEqual('mock.username2: mysql://mock.hostname2/database_c2', storage.get_storage_location())
    
    def test_get_table_names_no_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        actual_table_names = chain_storage.get_table_names()
        expected_table_names = ['table_c1', 'table_c2', 'table_b1']
        
        self.assertEqual(Set(actual_table_names), Set(expected_table_names))
        self.assertEqual(len(actual_table_names), len(expected_table_names))
        
    def test_get_table_names_no_chain2(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_d')
        
        actual_table_names = chain_storage.get_table_names()
        expected_table_names = ['table_d1', 'table_d2', 'table_d3']
        
        self.assertEqual(Set(actual_table_names), Set(expected_table_names))
        self.assertEqual(len(actual_table_names), len(expected_table_names))
        
    def test_get_table_names_in_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_b')
        
        actual_table_names = chain_storage.get_table_names()
        expected_table_names = ['table_b1', 'table_b2', 'scenario_information', 'table_c1', 'table_c2']
        
        self.assertEqual(Set(actual_table_names), Set(expected_table_names))
        self.assertEqual(len(actual_table_names), len(expected_table_names))
        
    def test_get_table_names_in_chain2(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_a')
        
        actual_table_names = chain_storage.get_table_names()
        expected_table_names = ['table_a1', 'table_b1', 'table_b2', 'scenario_information', 'table_c1', 'table_c2']
        
        self.assertEqual(Set(actual_table_names), Set(expected_table_names))
        self.assertEqual(len(actual_table_names), len(expected_table_names))

    def test_get_column_names_no_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        actual_column_names = chain_storage.get_column_names('table_c1')
        expected_column_names = ['a']
        
        self.assertEqual(Set(actual_column_names), Set(expected_column_names))
        self.assertEqual(len(actual_column_names), len(expected_column_names))
        
    def test_get_column_names_no_chain2(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        actual_column_names = chain_storage.get_column_names('table_c2')
        expected_column_names = ['a', 'b']
        
        self.assertEqual(Set(actual_column_names), Set(expected_column_names))
        self.assertEqual(len(actual_column_names), len(expected_column_names))
        
    def test_get_column_names_with_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_b')
        
        actual_column_names = chain_storage.get_column_names('table_c2')
        expected_column_names = ['a', 'b']
        
        self.assertEqual(Set(actual_column_names), Set(expected_column_names))
        self.assertEqual(len(actual_column_names), len(expected_column_names))
        
    def test_get_column_names_with_chain_correct_table_selected1(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        actual_column_names = chain_storage.get_column_names('table_b1')
        expected_column_names = ['a']
        
        self.assertEqual(Set(actual_column_names), Set(expected_column_names))
        self.assertEqual(len(actual_column_names), len(expected_column_names))
    
    def test_get_column_names_with_chain_correct_table_selected2(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_a')
        
        actual_column_names = chain_storage.get_column_names('table_b1')
        expected_column_names = ['a', 'b', 'c']
        
        self.assertEqual(Set(actual_column_names), Set(expected_column_names))
        self.assertEqual(len(actual_column_names), len(expected_column_names))
        
    def test_get_column_names_raises_exception_if_table_name_is_not_found(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        self.assertRaises(LookupError, chain_storage.get_column_names, 'table_bogus')
        
    def test_get_column_names_raises_exception_if_table_name_is_not_found_due_to_empty_url(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_e')
        
        self.assertRaises(LookupError, chain_storage.get_column_names, 'table_any')
        
        actual_table_names = chain_storage.get_table_names()
        expected_table_names = ['scenario_information']
        
        self.assertEqual(Set(actual_table_names), Set(expected_table_names))
        self.assertEqual(len(actual_table_names), len(expected_table_names))
        
    def test_load_table_no_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_d')
        
        actual_table_names = chain_storage.load_table('table_d1')
        expected_table_names = {'a': array([200], dtype='int32')}
        
        self.assertDictsEqual(actual_table_names, expected_table_names)
        
    def test_load_table_with_chain(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_b')
        
        actual_table_names = chain_storage.load_table('table_c2')
        expected_table_names = {
            'a': array([100], dtype='int32'),
            'b': array([300], dtype='int32'),
        }
        
        self.assertDictsEqual(actual_table_names, expected_table_names)
        
    def test_load_table_with_chain_and_multiple_rows(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_b')
        
        actual_table_names = chain_storage.load_table('table_b1')
        expected_table_names = {
            'a': array([100, 400], dtype='int32'),
            'b': array([200, 500], dtype='int32'),
            'c': array([300, 600], dtype='int32'),
        }
        
        self.assertDictsEqual(actual_table_names, expected_table_names)
        
    def test_load_table_raises_exception_if_table_name_is_not_found(self):
        chain_storage = self._get_mysql_chain_storage_for_localhost_database('database_c')
        
        self.assertRaises(LookupError, chain_storage.get_column_names, 'table_bogus')

    

if __name__ == '__main__':
    opus_unittest.main()
