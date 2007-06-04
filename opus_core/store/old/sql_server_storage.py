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
from opus_core.store.old.storage import Storage

try:
    import pymssql as pymssql_module
    
except:
    # If we could not import pymssql, don't fail, but give sql_server_storage 
    # something to check for.
    pymssql_module = None
    
class sql_server_storage(Storage):
    """
    sql_server_storage provides connectivity for storing Opus 
    table/attribute data into MS SQL Server. 
    
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

    def determine_field_names(self, load_resources):
        in_table_name = load_resources['in_table_name']
        
        return self._determine_field_names(in_table_name=in_table_name)

    def _determine_field_names(self, in_table_name):
        logger.start_block("MS SQL Server - reading field names for table '%s'" 
            % in_table_name)
        
        try:
            conn = self._get_connection()
            try:
                cursor = conn.cursor()
                
                try:
                    cursor.execute('SELECT TOP 0 * FROM %s' % in_table_name)
                except:
                    raise NameError("Could not access table '%s'" % in_table_name)
                
                return [
                    column_name 
                    for column_name, column_type, none1, none2, none3, none4, none5 in cursor.description
                    ]
                
            finally:
                conn.close()
        finally:
            logger.end_block()

    def write_dataset(self, write_resources):
        out_table_name = write_resources['out_table_name']
        values = write_resources['values']
        
        self._write_dataset(
            out_table_name = out_table_name,
            values = values,
            )

    def _write_dataset(self, out_table_name, values):
        logger.start_block('MS SQL Server - writing')
        
        logger.log_status('Establishing connection...')
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            column_names = values.keys()
            
            # Check that every column has the same number of items
            column_size = None
            for column_name in column_names:
                next_column_size = values[column_name].size
                
                if column_size is None:
                    column_size = next_column_size
                    
                if not next_column_size == column_size:
                    raise ValueError('Data in each column must be of the same length.')
                    
            if column_size is None:
                raise ValueError('No data to write!')
            
            # Construct the schema
            attributes = []
            char_type_pattern = re.compile('string([0-9]+)')
            for attribute_name in column_names:
                match = char_type_pattern.match(values[attribute_name].dtype.name)
                if match:
                    attribute_type = 'VARCHAR(%s)' % (int(match.group(1))/8)
                    
                else:
                    attribute_type = self.__NUMPY_TYPES_TO_SQL_SERVER_TYPES_OLD[values[attribute_name].dtype.char]
                attributes.append('%s %s' % (attribute_name, attribute_type))
                
            schema = ', '.join(attributes)
            
            query = 'CREATE TABLE %s (%s)' % (out_table_name, schema)
            
            try:
                cursor.execute(query)
            except pymssql_module.DatabaseError:
                logger.log_error("Could not create table '%s'" % out_table_name)
                raise
            
            logger.start_block('Inserting %s rows of data' % column_size)
            try:
                # Insert row by row
                i = 0
                while i < column_size:
                    # Get the row data
                    row_data = []
                    for attribute_name in column_names:
                        value = str(values[attribute_name][i])
                        
                        if values[attribute_name].dtype.char == 'S':
                            value = "'%s'" % value
                            
                        row_data.append(value)
                    
                    row_insert_values = ','.join(row_data)
    
                    query = ('INSERT INTO %s (%s) VALUES (%s)' 
                        % (out_table_name, ', '.join(column_names), row_insert_values))
                    
                    # print out a log message every once in a while to let
                    # anyone watching know we're still going.
                    if i % self._print_status_chunk_size == 0:
                        j = i + self._print_status_chunk_size
                        if j > column_size:
                            j = column_size
                        logger.log_status('Inserting records %s through %s...' % (i+1, j))
                        
                    cursor.execute(query)
                    conn.commit() ### TODO: Remove this!!!
                    
                    i += 1
                    ### Throw exception if there was a problem!!!
            finally:
                logger.end_block()
            
            conn.commit() ### Move this into above try just before finally!!!
            
        finally:
            logger.end_block()
            conn.close()
            
    def _get_connection(self):
        return self._pymssql.connect(
           host = self._hostname, 
           user = self._username, 
           password = self._password, 
           database = self._database_name
           )
        
    __NUMPY_TYPES_TO_SQL_SERVER_TYPES_OLD = {
        '?': 'TINYINT(1)',
        'b': 'TINYINT',
        'h': 'SMALLINT',
        'i': 'INT',
        'l': 'INT',
        'q': 'BIGINT',
        'p': 'INT',
        'B': 'TINYINT UNSIGNED',
        'H': 'SMALLINT UNSIGNED',
        'I': 'INT UNSIGNED',
        'L': 'INT UNSIGNED',
        'Q': 'BIGINT UNSIGNED',
        'P': 'INT UNSIGNED',
        'f': 'FLOAT',
        'd': 'FLOAT',
        'g': 'REAL',
        'S': 'VARCHAR(255)',
        'U': 'VARCHAR(255)',
        }



from opus_core.tests import opus_unittest

from numpy import array
    
from opus_core.resources import Resources


class TestSqlServerStorage(opus_unittest.OpusTestCase):
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

    def test__write_dataset(self):
        # test no table
        self.assertRaises(ValueError, self.storage._write_dataset,
            out_table_name = 'error_table',
            values = {}
            )
            
        self.assertConnectionHasCorrectParameters()
            
        # test jagged table
        self.assertRaises(ValueError, self.storage._write_dataset,
            out_table_name = 'error_table',
            values = {
                'a': array([1,2,3,4,5,6,7,8,9,0]),
                'b': array([1]),
                }
            )
        
        self.storage._write_dataset(
            out_table_name = 'foo',
            values = {
                'A': array([1]),
                }
            )
            
        mock_conn = self.storage._pymssql._last_connection

        self.assert_(mock_conn._committed_last)
        
        self.assert_(mock_conn._closed)

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "CREATE TABLE foo (A INT)",
            "INSERT INTO foo (A) VALUES (1)",
            ]
        self.assertEqual(expected_queries, actual_queries)
        
        self.storage._write_dataset(
            out_table_name = 'bar',
            values = {
                'B': array([1.1,2.2,3.3]),
                'C': array(['a', 'ab', 'abc']),
                }
            )
            
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
            print actual_query
            self.assert_(actual_query in possible_queries)
            
    def test__write_dataset_again(self):
        self.storage._write_dataset(
            out_table_name = 'foo',
            values = {
                'A': array(['abcdef']),
                }
            )
            
        mock_conn = self.storage._pymssql._last_connection

        self.assert_(mock_conn._committed_last)
        
        self.assert_(mock_conn._closed)

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "CREATE TABLE foo (A VARCHAR(6))",
            "INSERT INTO foo (A) VALUES ('abcdef')",
            ]
        self.assertEqual(expected_queries, actual_queries)

    def test_write_dataset(self):
        self.storage.write_dataset(Resources({
            'out_table_name': 'foo',
            'values': {
                'A': array([1]),
                }
            }))
            
        self.assertConnectionHasCorrectParameters()
            
        mock_conn = self.storage._pymssql._last_connection

        self.assert_(mock_conn._committed_last)
        
        self.assert_(mock_conn._closed)
        
    def test__determine_field_names(self):
        expected_field_names = ['attribute1', 'attribute2'] 
        actual_field_names = self.storage._determine_field_names(in_table_name='foo')
            
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
        
        # Check again with a different table name and attribute names.
        expected_field_names = ['attribute3', 'attribute4'] 
        actual_field_names = self.storage._determine_field_names(in_table_name='foobar')
    
        mock_conn = self.storage._pymssql._last_connection

        actual_queries = mock_conn._cursor._executed_queries
        expected_queries = [
            "SELECT TOP 0 * FROM foobar",
            ]
        self.assertEqual(expected_queries, actual_queries)
        
        self.assert_(mock_conn._closed)
    
        self.assertEqual(actual_field_names, expected_field_names)
        
        # What if we ask for a table that does not exist?
        self.assertRaises(NameError, self.storage._determine_field_names, in_table_name='idonotexist')

    
    def test_determine_field_names(self):
        expected_field_names = ['attribute3', 'attribute4'] 
        actual_field_names = self.storage.determine_field_names(Resources({
            'in_table_name':'foobar',
            }))
            
        self.assertConnectionHasCorrectParameters()
        
        self.assertEqual(actual_field_names, expected_field_names)
        
        expected_field_names = ['attribute1', 'attribute2'] 
        actual_field_names = self.storage.determine_field_names(Resources({
            'in_table_name':'foo',
            }))
        self.assertEqual(actual_field_names, expected_field_names)
        
        self.assertRaises(NameError, self.storage.determine_field_names, Resources({
            'in_table_name':'idonotexist',
            }))
        
if __name__ == '__main__':
    opus_unittest.main()