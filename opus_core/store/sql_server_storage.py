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

from numpy import ravel

from opus_core.logger import logger
from opus_core.store.storage import Storage
from opus_core.store.old.sql_server_storage import sql_server_storage as sql_server_storage_old

try:
    import pymssql as pymssql_module
    
except:
    # If we could not import pymssql, don't fail, but give sql_server_storage 
    # something to check for.
    pymssql_module = None
    
class sql_server_storage(Storage, sql_server_storage_old):
    """
    sql_server_storage provides connectivity for storing Opus 
    table/column data into MS SQL Server. 
    
    write_dataset expects database_name to be the name of an existing 
        database where the out_table_name table does not exist.
        
    load_dataset expects database_name to be the name of an existing
        database, with the in_table_name table exists.
        
    determine_field_names expects database_name to be the name of an 
        existing database where the in_table_name table exists.
    """
    # hook for unit tests
    _pymssql = pymssql_module # If None, pymssql could not be imported
    
    def __init__(self, hostname, username, password, database_name, print_status_chunk_size=1000):
        if self._pymssql is None: # If None, pymssql could not be imported
            raise ImportError('The pymssql Python module must be installed '
                'before using sql_server_storage. See '
                'http://pymssql.sourceforge.net/')
                
        self._hostname = hostname
        self._username = username
        self._password = password
        
        self._database_name = database_name
        
        self._print_status_chunk_size = print_status_chunk_size
        
    def get_storage_location(self):
        return '%s:mssqlserver://%s/%s' % (self._username, self._hostname, self._database_name)

    def get_column_names(self, table_name, lowercase=True):
        logger.start_block("MS SQL Server - reading field names for table '%s'" 
            % table_name)
        
        try:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                try:
                    cursor.execute('SELECT TOP 0 * FROM %s' % table_name)
                except:
                    raise NameError("Could not access table '%s'" % table_name)
                
                return [
                    column_name 
                    for column_name, unused_column_type, unused, unused, unused, unused, unused 
                    in cursor.description
                    ]
                
            finally:
                conn.close()
        finally:
            logger.end_block()

    def write_table(self, table_name, table_data):
        logger.start_block('MS SQL Server - writing')
        
        logger.log_status('Establishing connection...')
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            column_size, column_names = self._get_column_size_and_names(table_data)
            self._create_table(table_name, table_data, cursor)
            logger.start_block('Inserting %s rows of data' % column_size)
            try:
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
                    
                    cursor.execute(query)
                    self._log_insert_status(column_size, i)
                    ### Throw exception if there was a problem!!!
            finally:
                logger.end_block()
                conn.commit()
            
        finally:
            logger.end_block()
            conn.close()
            
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True, id_name=None):
        available_column_names = self.get_column_names(table_name=table_name)

        selected_column_names = \
            self._select_columns(column_names, available_column_names, case_insensitive=lowercase)
       
        if id_name and isinstance(id_name, basestring):
            id_name = [id_name]
            
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            result = {}
            for column_name in selected_column_names:
                query = 'SELECT %s FROM %s' % (column_name, table_name)
                if id_name is not None and len(id_name) > 0:
                    query = '%s ORDER BY %s' % (query, ', '.join(id_name))
                    
                cursor.execute(query)
            
                rows = cursor.fetchall()
                try: #for columns with numeric values
                    result[column_name] = ravel(rows)
                except: #for columns with string values
                    temp = []
                    for row in rows:
                        temp.extend(row)
                    result[column_name] = array(temp)
        finally:
            conn.close()
            
        return result
    
    def get_table_names(self):
        result = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # "AND TABLE_NAME<>'dtproperties'":
            # Bug in SQL Server, see http://support.microsoft.com/kb/832955
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME<>'dtproperties'")
            rows = cursor.fetchall()
            result = [table[0] for table in rows]
        finally:
            conn.close()
        return result
    
    def _get_connection(self):
        return self._pymssql.connect(
           host = self._hostname, 
           user = self._username, 
           password = self._password, 
           database = self._database_name
           )
        
    def _create_table(self, table_name, table_data, cursor):
        # Construct the schema
        columns = []
        char_type_pattern = re.compile('string([0-9]+)')
        for column_name in table_data.keys():
            match = char_type_pattern.match(table_data[column_name].dtype.name)
            if match:
                column_type = 'VARCHAR(%s)' % (int(match.group(1))/8)
            else:
                column_type = \
                    self.__NUMPY_TYPES_TO_SQL_SERVER_TYPES[table_data[column_name].dtype.name]
            columns.append('%s %s' % (column_name, column_type))
        schema = ', '.join(columns)
        query = 'CREATE TABLE %s (%s)' % (table_name, schema)
        try:
            cursor.execute(query)
        except pymssql_module.DatabaseError:
            logger.log_error("Could not create table '%s'" % table_name)
        
    def _log_insert_status(self, column_size, i):
        # print out a log message every once in a while to let
        
        # anyone watching know we're still going.
        if i % self._print_status_chunk_size == 0:
            j = i + self._print_status_chunk_size
            if j > column_size:
                j = column_size
            
            logger.log_status('Inserting records %s through %s...' % (i + 1, j))
        
    __NUMPY_TYPES_TO_SQL_SERVER_TYPES = {
        'int8':'INT',
        'int16':'INT',
        'int24':'INT',
        'int32':'INT',
        'int64':'INT',
        'float32':'FLOAT',
        'float64':'FLOAT',
        }


from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

from numpy import array
    
class TestSqlServerStorage(TestStorageInterface):
    class mock_pymssql(object):
        def __init__(self):
            self._last_connection = None
            
        _parameters = {
            'hostname':None,
            'username':None,
            'password':None,
            'database_name':None,
            }
        def connect(self, host, user, password, database):
            self._parameters = {
                'hostname':host, 
                'username':user, 
                'password':password, 
                'database_name':database,
                }
            self._last_connection = self._mock_connection()
            return self._last_connection
            
        class _mock_connection(object):
            def __init__(self):
                self._cursor = None
                self._committed = False
                self._committed_last = False
                self._closed = False
                
            def cursor(self):
                if self._closed:
                    raise pymssql_module.OperationalError('invalid connection')
                
                if self._cursor is None:
                    self._cursor = self._mock_cursor(self)
                
                return self._cursor

            def commit(self):
                self._committed = True
                self._committed_last = True

            def close(self):
                self._closed = True

            class _mock_cursor(object):
                def __init__(self, parent):
                    self._parent = parent
                    self._executed_queries = []
                
                def execute(self, query):
                    if self._parent._closed:
                        raise pymssql_module.OperationalError('internal error')
                    
                    self._parent._committed_last = False
                    self._executed_queries.append(query)
                    query = query.lower()
                    
                    if query == 'select top 0 * from foo':
                        self.description = [
                            ('attribute1', 0, None, None, None, None, None), 
                            ('attribute2', 0, None, None, None, None, None)
                            ]
                        
                    if query == 'select top 0 * from foobar':
                        self.description = [
                            ('attribute3', 0, None, None, None, None, None), 
                            ('attribute4', 0, None, None, None, None, None)
                            ]
                            
                    if query == 'select top 0 * from idonotexist':
                        raise pymssql_module.DatabaseError()
                        
                    if query == 'select top 0 * from table_for_load_tests':
                        self.description = [
                            ('keyid', 0, None, None, None, None, None), 
                            ('works', 0, None, None, None, None, None)
                            ]
                        
                    if query == 'select keyid from table_for_load_tests':
                        self.result = ((1,),(2,),(3,),(4,),(5,))
                        self.description = [
                            ('keyid', 0, None, None, None, None, None), 
                            ]
                        
                    if query == 'select works from table_for_load_tests':
                        self.result = ((1,),(1,),(-1,),(0,),(0,))
                        self.description = [
                            ('works', 0, None, None, None, None, None), 
                            ]
                            
                    if query == 'select top 0 * from different_table_name_for_load_tests':
                        self.description = [
                            ('keyid', 0, None, None, None, None, None), 
                            ('works', 0, None, None, None, None, None)
                            ]
                        
                    if query == 'select keyid from different_table_name_for_load_tests':
                        self.result = ((1,),(2,),(3,),(4,),(5,))
                        self.description = [
                            ('keyid', 0, None, None, None, None, None), 
                            ]
                        
                    if query == 'select works from different_table_name_for_load_tests':
                        self.result = ((1,),(1,),(-1,),(0,),(0,))
                        self.description = [
                            ('works', 0, None, None, None, None, None), 
                            ]
                            
                    if query == 'select keyid from table_for_load_tests_uppercase':
                        self.result = ((1,),(2,),(3,),(4,),(5,))
                        self.description = [
                            ('KEYID', 0, None, None, None, None, None), 
                            ]
                            
                    if query == 'select top 0 * from table_for_load_tests_uppercase':
                        self.description = [
                            ('KEYID', 0, None, None, None, None, None), 
                            ]
                        
                    if query == 'select city_name from table_for_load_strings':
                        self.result = (('Unknown',),('Eugene',),('Springfield',))
                        self.description = [
                            ('city_name', 0, None, None, None, None, None), 
                            ]
                        
                    if query == 'select top 0 * from table_for_load_strings':
                        self.description = [
                            ('city_name', 0, None, None, None, None, None), 
                            ]
                        
                    if query == "select table_name from information_schema.tables where table_type='base table' and table_name<>'dtproperties'":
                        self.result = (('table1',),('table2',),('table7',))
                            
                def fetchall(self):
                    return self.result
                    
    def setUp(self):
        self.pymssql_module = sql_server_storage._pymssql
        
        sql_server_storage._pymssql = self.mock_pymssql()
        
        self.storage = sql_server_storage(
            hostname = r'HOSTNAME\MOCK',
            username = 'mock_username',
            password = 'mock_password',
            database_name = 'mock_database',
            )
        
    def tearDown(self):
        sql_server_storage._pymssql = self.pymssql_module
                
    def assertConnectionHasCorrectParameters(self):
        actual_parameters = self.storage._pymssql._parameters
        self.assertEqual(actual_parameters['hostname'], r'HOSTNAME\MOCK')
        self.assertEqual(actual_parameters['username'], 'mock_username')
        self.assertEqual(actual_parameters['password'], 'mock_password')
        self.assertEqual(actual_parameters['database_name'], 'mock_database')

    def test_write_table(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = {
                'A': array([1]),
                }
            )
        self.assertConnectionHasCorrectParameters()
        mock_conn = self.storage._pymssql._last_connection
        self.assert_(mock_conn._committed_last)
        self.assert_(mock_conn._closed)
        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "CREATE TABLE foo (A INT)",
            "INSERT INTO foo (A) VALUES (1)",
            ]
        self.assertEqual(expected_queries, actual_queries)
        
    def test_write_table_more_than_one_column(self):
        self.storage.write_table(
            table_name = 'bar',
            table_data = {
                'B': array([1.1,2.2,3.3]),
                'C': array(['a', 'ab', 'abc']),
                }
            )
        self.assertConnectionHasCorrectParameters()    
        mock_conn = self.storage._pymssql._last_connection
        actual_queries = mock_conn._cursor._executed_queries
        possible_expected_queries = [
            ["CREATE TABLE bar (B FLOAT, C VARCHAR(3))", "CREATE TABLE bar (C VARCHAR(3), B FLOAT)"],
            ["INSERT INTO bar (B, C) VALUES (1.1,'a')", 
                "INSERT INTO bar (C, B) VALUES ('a',1.1)"],
            ["INSERT INTO bar (B, C) VALUES (2.2,'ab')", 
                "INSERT INTO bar (C, B) VALUES ('ab',2.2)"],
            ["INSERT INTO bar (B, C) VALUES (3.3,'abc')", 
                "INSERT INTO bar (C, B) VALUES ('abc',3.3)"],
            ]
        self.assertEqual(len(actual_queries), len(possible_expected_queries))
        for actual_query, possible_queries in zip(actual_queries, possible_expected_queries):
            self.assert_(actual_query in possible_queries)

    def test_get_column_names(self):
        expected_field_names = ['attribute1', 'attribute2'] 
        actual_field_names = self.storage.get_column_names(table_name='foo')
        self.assertConnectionHasCorrectParameters()
        mock_conn = self.storage._pymssql._last_connection
        self.assert_(not mock_conn._committed)
        self.assert_(mock_conn._closed)
        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT TOP 0 * FROM foo",
            ]
        self.assertEqual(expected_queries, actual_queries)
        self.assertEqual(actual_field_names, expected_field_names)
        
    def test_get_column_names_different_table(self):
        expected_field_names = ['attribute3', 'attribute4'] 
        actual_field_names = self.storage.get_column_names(table_name='foobar')
        mock_conn = self.storage._pymssql._last_connection
        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT TOP 0 * FROM foobar",
            ]
        self.assertEqual(expected_queries, actual_queries)
        self.assert_(mock_conn._closed)
        self.assertEqual(actual_field_names, expected_field_names)
        
    def test_get_column_names_nonexisting_table(self):
        self.assertRaises(NameError, self.storage.get_column_names, table_name='idonotexist')

    def test_load_table(self):
        actual = self.storage.load_table(
            table_name = 'table_for_load_tests',
            column_names = ['keyid'],
            lowercase = True,
            )
        expected = {
            'keyid': array([1, 2, 3, 4, 5])
            }
        self.assertDictsEqual(expected, actual)
        
        self.assertConnectionHasCorrectParameters()
        
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT keyid FROM table_for_load_tests",
            ]
        self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_list_of_one_column(self):
        values = self.storage.load_table(table_name='table_for_load_tests', 
                                           column_names = ['keyid']
                                           )
        expected = {
            'keyid': array([1,2,3,4,5]),
            }
        self.assertDictsEqual(expected, values)
        
        self.assertConnectionHasCorrectParameters()
        
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT keyid FROM table_for_load_tests",
            ]
        self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_list_of_two_columns(self):
        values = self.storage.load_table(table_name='table_for_load_tests', 
                                         column_names = ['keyid', 'works']
                                         )
        expected = {
            'keyid': array([1,2,3,4,5]),
            'works': array([1,1,-1,0,0]),
            }
        self.assertDictsEqual(expected, values)
        
        self.assertConnectionHasCorrectParameters()
        
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT keyid FROM table_for_load_tests",
            "SELECT works FROM table_for_load_tests",
            ]
        self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_one_column_not_in_list(self):
        values = self.storage.load_table(table_name='table_for_load_tests', 
                                         column_names = ['keyid']
                                         )
        expected = {
            'keyid': array([1,2,3,4,5]),
            }
        self.assertDictsEqual(expected, values)
        
        self.assertConnectionHasCorrectParameters()
        
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT keyid FROM table_for_load_tests",
            ]
        self.assertEqual(expected_queries, actual_queries)

    def test_load_table_all_columns(self):
            values = self.storage.load_table('table_for_load_tests')
            expected = {
                'keyid': array([1,2,3,4,5]),
                'works': array([1,1,-1,0,0]),
                }
            self.assertDictsEqual(expected, values)
            
            self.assertConnectionHasCorrectParameters()
            
            mock_conn = self.storage._pymssql._last_connection
    
            actual_queries = mock_conn._cursor._executed_queries
            expected_queries = [
                "SELECT keyid FROM table_for_load_tests",
                "SELECT works FROM table_for_load_tests",
                ]
            self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_different_table_name(self):
            values = self.storage.load_table('different_table_name_for_load_tests')
            expected = {
                'keyid': array([1,2,3,4,5]),
                'works': array([1,1,-1,0,0]),
                }
            self.assertDictsEqual(expected, values)
            
            self.assertConnectionHasCorrectParameters()
            
            mock_conn = self.storage._pymssql._last_connection
    
            actual_queries = mock_conn._cursor._executed_queries
            expected_queries = [
                "SELECT keyid FROM different_table_name_for_load_tests",
                "SELECT works FROM different_table_name_for_load_tests",
                ]
            self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_lowercase(self):
            values = self.storage.load_table(table_name='table_for_load_tests', 
                                             column_names=['KEYID'])
            expected = {
                'KEYID': array([1,2,3,4,5]),
                }
            self.assertDictsEqual(expected, values)
            
            self.assertConnectionHasCorrectParameters()
            
            mock_conn = self.storage._pymssql._last_connection
    
            actual_queries = mock_conn._cursor._executed_queries
            expected_queries = [
                "SELECT KEYID FROM table_for_load_tests",
                ]

            self.assertEqual(expected_queries, actual_queries)
            
    def test_load_table_uppercase(self):
        values = self.storage.load_table(table_name='table_for_load_tests_uppercase', 
                                         column_names='KEYID', 
                                         lowercase=False,
                                         )
        expected = {
            'KEYID': array([1,2,3,4,5]),
            }
        self.assertDictsEqual(expected, values)
        
        self.assertConnectionHasCorrectParameters()
        
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT KEYID FROM table_for_load_tests_uppercase",
            ]
        self.assertEqual(expected_queries, actual_queries)
        
    def test_load_table_strings(self):
            values = self.storage.load_table(table_name='table_for_load_strings', 
                                             column_names=['city_name'])
            expected = {
                'city_name': array(['Unknown', 'Eugene', 'Springfield']),
                }
            self.assertDictsEqual(expected, values)
            
            self.assertConnectionHasCorrectParameters()
            
            mock_conn = self.storage._pymssql._last_connection
    
            actual_queries = mock_conn._cursor._executed_queries
            expected_queries = [
                "SELECT city_name FROM table_for_load_strings",
                ]

            self.assertEqual(expected_queries, actual_queries)
            
    def test_get_table_names(self):
        expected = ['table1', 'table2', 'table7']
        expected.sort()
        actual = self.storage.get_table_names()
        actual.sort()
        self.assertEquals(expected, actual)
            
        
if __name__ == '__main__':
    opus_unittest.main()