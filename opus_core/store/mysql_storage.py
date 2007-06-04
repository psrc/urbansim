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

from opus_core.logger import logger
from opus_core.store.storage import Storage
from opus_core.store.old.mysql_storage import mysql_storage as mysql_storage_old


# If we could not import MySQLdb, don't fail, but give mysql_storage 
# something to check for.
try:
    from MySQLdb import connect as _mysqldb_connect
    from MySQLdb.constants import FIELD_TYPE
except: 
    _mysqldb_connect = None
    

class mysql_storage(Storage, mysql_storage_old):    
    _connection = None
    
    def __init__(self, hostname=None, username=None, password=None, 
                 database_name=None, print_status_chunk_size=1000, storage_location=None):
        if _mysqldb_connect is None: # If None, mysqldb could not be imported
            raise ImportError('The mysqldb Python module must be installed '
                'before using mysql_storage. See '
                'http://mysql-python.sourceforge.net/')
        
        ### Connection reconstruction information
        self._hostname = hostname
        self._username = username
        self._password = password
        self._database_name = database_name
        
        self._print_status_chunk_size = print_status_chunk_size
        
        ### TODO: Eliminate this once the new storage interface is completely integrated with the system.
        if storage_location is not None:
            mysql_storage_old.__init__(self, storage_location, print_status_chunk_size)
            
            self._database_name = self._db
        
    def get_storage_location(self):
        return '%s: mysql://%s/%s' % (self._username, self._hostname, self._database_name)

    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True, id_name=None):
        available_column_names = self.get_column_names(table_name=table_name)
        
        if id_name:
            column_names = self._select_columns(column_names, available_column_names, case_insensitive=lowercase)
            if isinstance(id_name, basestring):
                id_name = [id_name]
        else:
            column_names = available_column_names
        
        temp = {}
        for col in range(len(column_names)):
            temp[col] = []
            
        conn = self._get_connection()
        result = {}
        try:
            query = 'SELECT %s FROM %s' % (', '.join(column_names), table_name)
            
            if id_name is not None and len(id_name) > 0:
                query = '%s ORDER BY %s' % (query, ', '.join(id_name))
            
            cursor = conn.cursor()
            cursor.execute(query)
            
            column_type_map = dict([(column_name, self._numpy_type_for_mysql_type(column_type))
                                    for column_name, column_type, _, _, _, _, _
                                    in cursor.description])
            
            rows = cursor.fetchall()

            for row in rows:
                for col in range(len(column_names)):
                    temp[col].append(row[col])
            
            for col in range(len(column_names)):
                column_name = column_names[col]
                values = temp[col]
                
                self._assert_no_nones(table_name, column_name, values)
            
                dtype = column_type_map[column_name]
                
                result[column_name] = array(values, dtype=dtype)
                    
        finally:
            conn.close()
            
        return result
    
    def write_table(self, table_name, table_data):
        logger.start_block('MYSQL - writing')
        
        logger.log_status('Establishing connection...')
        try:        
            column_size, column_names = self._get_column_size_and_names(table_data)
            
            conn = self._get_connection()
            try:
                logger.start_block('Inserting %s rows of data' % column_size)
                try:
                    self._create_table(table_name, table_data, conn)
                    
                    # Insert row by row
                    for i in xrange(column_size):
                        # Get the row data
                        row_data = []
                        for column_name in column_names:
                            value = str(table_data[column_name][i])
                            
                            if table_data[column_name].dtype.char == 'S':
                                value = "'%s'" % value
                                
                            row_data.append(value)
                        
                        row_insert_values = ','.join(row_data)
        
                        query = ('INSERT INTO %s (%s) VALUES (%s)' 
                            % (table_name, ', '.join(column_names), row_insert_values))
                        
                        conn.query(query)
                        self._log_insert_status(column_size, i)
                        ### Throw exception if there was a problem!!!
                finally:
                    logger.end_block()
            
            finally:
                conn.close()

        finally:
            logger.end_block()
            
    def get_column_names(self, table_name, lowercase=True):
        table_names = self._get_first_column_for_query('show fields from %s' % table_name)
        if lowercase:
            table_names = self._lower_case(table_names)
        return table_names
    
    def get_table_names(self):
        return self._get_first_column_for_query('show tables')
    
    def _get_first_column_for_query(self, query):
        conn = self._get_connection()
        conn.query(query)
        r = conn.store_result()
        result = []
        
        row = r.fetch_row()
        while row:
            result.append(row[0])
            row = r.fetch_row()
            
        return [row[0] for row in result]
    
    def _get_connection(self):
        if self._connection==None or self._connection.open==0:
            self._connection = _mysqldb_connect(
                host=self._hostname, 
                user=self._username, 
                passwd=self._password, 
                db=self._database_name
                )
        return self._connection
    
    def _create_table(self, table_name, table_data, conn):
        # Construct the schema
        columns = []
        char_type_pattern = re.compile('string([0-9]+)')
        for column_name in table_data.keys():
            match = char_type_pattern.match(table_data[column_name].dtype.name)
            if match:
                column_type = 'VARCHAR(%s)' % (int(match.group(1))/8)
            else:
                column_type = self.__NUMPY_TYPES_TO_MYSQL_TYPES[table_data[column_name].dtype.name]
            columns.append('%s %s' % (column_name, column_type))
        schema = ', '.join(columns)
        query = 'CREATE TABLE %s (%s)' % (table_name, schema)
        try:
            conn.query(query)
        except:
            logger.log_error("Could not create table '%s'" % table_name)
            
    def _log_insert_status(self, column_size, i):
        
        # print out a log message every once in a while to let
        
        # anyone watching know we're still going.
        if i % self._print_status_chunk_size == 0:
            j = i + self._print_status_chunk_size
            if j > column_size:
                j = column_size
            
            logger.log_status('Inserting records %s through %s...' % (i + 1, j))
            
    __NUMPY_TYPES_TO_MYSQL_TYPES = {
        'int8':'TINYINT',
        'int16':'SMALLINT',
        'int24':'MEDIUMINT',
        'int32':'INT',
        'int64':'BIGINT',
        'float32':'FLOAT',
        'float64':'DOUBLE',
        }
        
    def _numpy_type_for_mysql_type(self, mysql_type):
        """Return numpy type for this MySQL field type."""

        return {
            FIELD_TYPE.DECIMAL: 'float64', # probably won't work.
            FIELD_TYPE.TINY: 'int8',
            FIELD_TYPE.SHORT: 'int16',
            FIELD_TYPE.LONG: 'int32',
            FIELD_TYPE.FLOAT: 'float32',
            FIELD_TYPE.DOUBLE: 'float64',
            FIELD_TYPE.LONGLONG: 'int64',
            FIELD_TYPE.INT24: 'int32', # There is no int24/i3 numpy type.
            FIELD_TYPE.TINY_BLOB: 'a',
            FIELD_TYPE.MEDIUM_BLOB: 'a',
            FIELD_TYPE.LONG_BLOB: 'a',
            FIELD_TYPE.BLOB: 'a',
            FIELD_TYPE.VAR_STRING: 'a',
            FIELD_TYPE.STRING: 'a',
            }[mysql_type]
    
    
if _mysqldb_connect is None:
    logger.log_warning('Tests for mysql_storage skipped because the MySQLdb '
        'module could not be loaded.')
else:
    from opus_core.tests import opus_unittest
    
    import os
    
    from sets import Set
    
    from opus_core.store.storage import TestStorageInterface
    from opus_core.configurations.database_server_configuration import LocalhostDatabaseServerConfiguration
    from opus_core.store.mysql_database_server import MysqlDatabaseServer
    
    from numpy import array
    
    class TestMysqlStorage(TestStorageInterface):
        def setUp(self):
            self.storage = mysql_storage(
                hostname = r'HOSTNAME\MOCK',
                username = 'mock_username',
                password = 'mock_password',
                database_name = 'mock_database',
                )
            
    # TODO: uncomment this test once have faster way to run the assert.
    #    def test_load_table_with_nulls(self):
    #        self.assertRaises(ValueError, self.storage.load_table, 'some_table_with_nulls')
    
    class FunctionalTestsForMysqlStorage(opus_unittest.TestCase):
        def setUp(self):
            db_server = MysqlDatabaseServer(LocalhostDatabaseServerConfiguration())
            
            db_server.drop_database('database_a')
            db_server.create_database('database_a')
            
            database = db_server.get_database('database_a')
            
            database.DoQuery('CREATE TABLE table_a1 (a INT)')
            database.DoQuery('INSERT INTO table_a1 (a) VALUES (100)')
            
            database.DoQuery('CREATE TABLE table_a2 (id INT, a INT)')
            database.DoQuery('INSERT INTO table_a2 (id, a) VALUES (2,200),(3,300),(1,100)')
            
            database.DoQuery('CREATE TABLE table_a3 (id1 INT, id2 INT, a INT)')
            database.DoQuery('INSERT INTO table_a3 (id1, id2, a) VALUES (2,5,300),(1,10,200),(2,10,400),(1,5,100)')
            
            database.DoQuery('CREATE TABLE table_a4 (tinyint_col TINYINT, int_col INT, bigint_col BIGINT)')
            database.DoQuery('INSERT INTO table_a4 (tinyint_col, int_col, bigint_col) VALUES (1,2,3)')
        
        def tearDown(self):
            db_server = MysqlDatabaseServer(LocalhostDatabaseServerConfiguration())
            
            db_server.drop_database('database_a')
        
        def _get_mysql_storage_for_localhost_database(self, database_name):
            localhost_database_server_configuration = LocalhostDatabaseServerConfiguration()
            return mysql_storage(
                hostname = localhost_database_server_configuration.host_name,
                username = localhost_database_server_configuration.user_name,
                password = localhost_database_server_configuration.password,
                database_name = database_name,
                )
            
        def test_get_column_names(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_column_names = storage.get_column_names(table_name='table_a1', lowercase=True)
            expected_column_names = ['a']
            
            self.assertEqual(Set(actual_column_names), Set(expected_column_names))
            self.assertEqual(len(actual_column_names), len(expected_column_names))
            
            actual_column_names = storage.get_column_names(table_name='table_a3', lowercase=True)
            expected_column_names = ['a', 'id1', 'id2']
            
            self.assertEqual(Set(actual_column_names), Set(expected_column_names))
            self.assertEqual(len(actual_column_names), len(expected_column_names))
            
        def test_write_table(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            expected_values = {
                'id': array([1,2,3,4], dtype='int32'),
                'col1': array([6,2,4,8], dtype='float32'),
                'col2': array(['a','b','c','d']),
                }
                    
            storage.write_table('unique_table', expected_values)
            actual_values = storage.load_table('unique_table')
            
            self.assertDictsEqual(expected_values, actual_values)
        
        def test_get_table_names(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            expected_table_names = ['table_a1', 'table_a2', 'table_a3', 'table_a4']
            actual_table_names = storage.get_table_names()
            
            self.assertEqual(Set(actual_table_names), Set(expected_table_names))
            self.assertEqual(len(actual_table_names), len(expected_table_names))
        
        def test__get_mysql_storage_for_database_gets_correct_value(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a1') # steak sauce
            expected_values = {
                'a': array([100], dtype='int32'),
                }
            self.assertDictsEqual(expected_values, actual_values)
            
        def test__get_mysql_storage_for_database_with_string_for_id_name(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a2', id_name='id')
            expected_values = {
                'id': array([1,2,3], dtype='int32'),
                'a': array([100,200,300], dtype='int32'),
                }
            self.assertDictsEqual(expected_values, actual_values)
            
        def test__get_mysql_storage_for_database_with_list_with_single_id_for_id_name(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a2', id_name=['id'])
            expected_values = {
                'id': array([1,2,3], dtype='int32'),
                'a': array([100,200,300], dtype='int32'),
                }
            self.assertDictsEqual(expected_values, actual_values)
            
        def test__get_mysql_storage_for_database_with_list_with_more_than_one_id_for_id_name(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a3', id_name=['id1','id2'])
            expected_values = {
                'id1': array([1,1,2,2], dtype='int32'),
                'id2': array([5,10,5,10], dtype='int32'),
                'a': array([100,200,300,400], dtype='int32'),
                }
            self.assertDictsEqual(expected_values, actual_values)
            
        def test__get_mysql_storage_for_database_with_empty_list_for_id_name(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a2', id_name=[])
            expected_values = {
                'id': array([2,3,1], dtype='int32'),
                'a': array([200,300,100], dtype='int32'),
                }
            self.assertDictsEqual(expected_values, actual_values)
            
        def test_input_types_equal_output_types(self):
            storage = self._get_mysql_storage_for_localhost_database('database_a')
            
            actual_values = storage.load_table('table_a4', id_name=[])
            expected_values = {
                'tinyint_col': array([1], dtype='int8'),
                'int_col': array([2], dtype='int32'),
                'bigint_col': array([3], dtype='int64'),
                }
            self.assertDictsEqual(expected_values, actual_values)
    
            
    if __name__ == '__main__':
        opus_unittest.main()