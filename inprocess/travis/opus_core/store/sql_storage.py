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

from numpy import array, dtype

try:
    import sqlalchemy
    from sqlalchemy import create_engine, Table, Column, MetaData
    from sqlalchemy.types import Integer, Float, String, DECIMAL
    
except ImportError:
    sqlalchemy = None
    

from opus_core.store.storage import Storage


class sql_storage(Storage):
    def __init__(self, protocol, username, password, hostname, database_name, port=None):
        """
        protocol: 'sqlite', 'mysql', 'postgres', 'oracle', 'mssql', or 'firebird'
          - A corresponding module must be installed
        """
        if sqlalchemy is None:
            raise ImportError('The sqlalchemy Python module must be installed '
                'before using sql_storage. See http://www.sqlalchemy.org/')
        
        if port is not None:
            port_string = ':%s' % port
        else:
            port_string = ''
        
        connection_string = '%s://%s:%s@%s%s/%s' % (
            protocol,
            username,
            password,
            hostname,
            port_string,
            database_name
            )     
        
        self._engine = create_engine(connection_string)
        self._metadata = MetaData(
            bind = self._engine
        )
        
    def get_storage_location(self):
        return str(self._engine.url)
        
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True, id_name=None):
        table = Table(table_name, self._metadata, autoload=True)
        
        query_results = table.select().execute()
            
        table_data = dict([(column, []) for column in query_results.keys])
                
        for row in query_results:
            for column in query_results.keys:
                table_data[column].append(row[column])
        
        for column in table.columns:
            type = self._get_numpy_dtype_from_sql_alchemy_type(column.type)
            
            table_data[column.name] = array(table_data[column.name], dtype=type)
        
        return table_data
        
        
    def write_table(self, table_name, table_data, overwrite_existing = True):
        table_length, _ = self._get_column_size_and_names(table_data)
        
        columns = []
        for column_name, column_data in table_data.iteritems():
            col_type = self._get_sql_alchemy_type_from_numpy_dtype(column_data.dtype)
            columns.append(Column(column_name, 
                                  col_type))
            if column_data.dtype == 'i':
                table_data[column_name] = [int(cell) for cell in column_data]
            elif column_data.dtype == 'f':
                table_data[column_name] = [float(cell) for cell in column_data]
            
        table = Table(table_name, self._metadata, *columns)
        if overwrite_existing:
            table.drop(checkfirst = True)
        
        connection = self._engine.connect()
        try:
            transaction = connection.begin()
            try:
                try:
                    table.create()
                except Exception, e:
                    raise NameError('Failed to create table, possibly due to an illegal column name.\n(Original error: %s)' % e)
                
                rows_to_insert = []
                for row in range(table_length):
                    row_data = {}
                    for column_name, column_data in table_data.iteritems():
                        row_data[column_name] = column_data[row]
                    rows_to_insert.append(row_data)
                
                try:
                    connection.execute(table.insert(), rows_to_insert)
                    #table.insert().execute(*rows_to_insert)
                except Exception, e:
                    raise ValueError('Failed to insert data into table, possibly due to incorrect data type.\n(Original error: %s)\nData to be inserted: %s' % (e, row_data))
            
                transaction.commit()
                
            except:
                transaction.rollback()
                raise
                
        finally:
            connection.close()

    def get_column_names(self, table_name, lowercase=True):
        table = Table(table_name, self._metadata, autoload=True)
        
        return [column.name 
            for column in table.columns]
    
    def get_table_names(self):
        return [table.name
            for table in self._metadata.table_iterator()]
    
    def _get_sql_alchemy_type_from_numpy_dtype(self, column_dtype):
        mapping = {
            'i':Integer,
            'f':Float,
            'S':String,
            }
        
        return mapping[column_dtype.kind]
        
    def _get_numpy_dtype_from_sql_alchemy_type(self, column_type):
        if isinstance(column_type, Integer) or column_type == Integer:
            return dtype('i')
        
        if isinstance(column_type, Float) or column_type == Float:
            return dtype('f')
        
        if isinstance(column_type, String) or column_type == String:
            return dtype('S')

        raise ValueError('Unrecognized column type: %s' % column_type)
        
    
if sqlalchemy is None:
    if __name__ == '__main__':
        from opus_core.logger import logger 
        logger.log_warning('Skipping sql_storage unit tests -- could not import the sqlalchemy module.')
    
else:
    from opus_core.tests import opus_unittest
    
    import os
    
    from sets import Set

    from opus_core.store.storage import TestStorageInterface
    from opus_core.store.mysql_database_server import MysqlDatabaseServer
    from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration

    class SQLStorageTest(TestStorageInterface):
        """
        Uses MySQL and sqlite for these tests.
        """
        def setUp(self):
            self.database_name = 'test_database'
            protocol = 'mysql'
            
            config = DatabaseServerConfiguration()

            self.db_server = MysqlDatabaseServer(config)
            
            self.db_server.drop_database(self.database_name)
            self.db_server.create_database(self.database_name)

            # Use MySQL to test this.
            self.storage = sql_storage(
                protocol = protocol,
                username = config.user_name,
                password = config.password,
                hostname = config.host_name,
                database_name = self.database_name,
                )
            
        def tearDown(self):
            del self.storage
            self.db_server.drop_database(self.database_name)
            
            self.db_server.close()
        
        def test_get_storage_location_returns_database_url_built_from_the_constructor_arguments_not_including_port(self):
            storage = sql_storage(
                protocol = 'mysql',
                username = 'username',
                password = 'password',
                hostname = 'hostname',
                database_name = 'database_name',
                )
                
            expected_url = 'mysql://username:password@hostname/database_name'
            actual_url = storage.get_storage_location()
            
            self.assertEqual(expected_url, actual_url)
            
        def test_get_storage_location_returns_database_url_built_from_the_constructor_arguments_including_port(self):
            storage = sql_storage(
                protocol = 'sqlite',
                username = 'username',
                password = 'password',
                hostname = 'hostname',
                database_name = 'database_name',
                port = 9999,
                )
                
            expected_url = 'sqlite://username:password@hostname:9999/database_name'
            actual_url = storage.get_storage_location()
            
            self.assertEqual(expected_url, actual_url)
            
        def test_write_table_creates_a_table_with_the_given_table_name_and_data(self):
            from MySQLdb import ProgrammingError, OperationalError
                   
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )
                
            expected_results = [['id', 'a'], [1,4], [2,5], [3,6]]
            
            #Verify the data through a MysqlDatabaseServer database connection
            db = self.db_server.get_database(self.database_name)
            
            try:
                db.DoQuery('SELECT * FROM test_write_table')
                
            except ProgrammingError, (error_code, _):
                if error_code == 1146:
                    self.fail('write_table() did not create a table with the expected name (test_write_table).')
                else:
                    raise
                
            try:
                results = db.GetResultsFromQuery('SELECT id, a FROM test_write_table ORDER BY id')
                
            except OperationalError, (error_code, error_message):
                if error_code == 1054:
                    self.fail('write_table() did not create all of the expected columns: %s' % error_message)
                else:
                    raise
                
            self.assertEqual(expected_results, results)
        
        def test_write_table_creates_a_table_with_the_given_table_name_and_data_of_different_types(self):
            from MySQLdb import ProgrammingError, OperationalError
                   
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'int_data': array([2,1]),
                    'float_data': array([2.2,1.1]),
                    'string_data': array(['foo', 'bar'])
                    }
                )
                
            expected_results = [['int_data', 'float_data', 'string_data'], [1,1.1,'bar'], [2,2.2,'foo']]
            
            # Verify the data through a MysqlDatabaseServer database connection
            db = self.db_server.get_database(self.database_name)
            
            try:
                db.DoQuery('SELECT * FROM test_write_table')
                
            except ProgrammingError, (error_code, _):
                if error_code == 1146:
                    self.fail('write_table() did not create a table with the expected name (test_write_table).')
                else:
                    raise
                
            try:
                results = db.GetResultsFromQuery('SELECT int_data, float_data, string_data FROM test_write_table ORDER BY int_data')
                
            except OperationalError, (error_code, error_message):
                if error_code == 1054:
                    self.fail('write_table() did not create all of the expected columns: %s' % error_message)
                else:
                    raise
                
            self.assertEqual(expected_results, results)
            
        def test_get_sql_alchemy_type_from_numpy_dtype(self):
            expected_sql_alchemy_type = Integer
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('i'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
            expected_sql_alchemy_type = Float
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('f'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
            expected_sql_alchemy_type = String
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('S'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
        def test_get_numpy_dtype_from_sql_alchemy_type(self):
            expected_numpy_type = dtype('i')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(Integer)
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
            expected_numpy_type = dtype('f')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(Float)
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
            expected_numpy_type = dtype('S')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(String)
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
        
        def test_get_table_names_added_through_write_table(self):
            self.storage.write_table('table1', {'a':array([1])})
            self.storage.write_table('table2', {'a':array([1])})
            self.storage.write_table('table3', {'a':array([1])})
                
            expected_table_names = ['table1', 'table2', 'table3']
            actual_table_names = self.storage.get_table_names()
                
            self.assertEqual(Set(expected_table_names), Set(actual_table_names))
            self.assertEqual(len(expected_table_names), len(actual_table_names))
            
#        def test_get_table_names_already_in_database(self):
#            db = self.db_server.get_database(self.database_name)
#            
#            db.DoQuery('CREATE TABLE foo (a INT)')
#            db.DoQuery('INSERT INTO foo (a) VALUES (1)')
#            
#            db.DoQuery('CREATE TABLE bar (a INT)')
#            db.DoQuery('INSERT INTO bar (a) VALUES (1)')
#            
#            db.DoQuery('CREATE TABLE baz (a INT)')
#            db.DoQuery('INSERT INTO baz (a) VALUES (1)')
#                
#            expected_table_names = ['baz', 'bar', 'foo']
#            actual_table_names = self.storage.get_table_names()
#                
#            self.assertEqual(Set(expected_table_names), Set(actual_table_names))
#            self.assertEqual(len(expected_table_names), len(actual_table_names))
            
        def test_get_column_names(self):
            self.storage.write_table(
                table_name = 'foo', 
                table_data = {
                    'bee': array([1]),
                    'baz': array([1]),
                    'foobeebaz': array([1])
                    }
                )
            
            db = self.db_server.get_database(self.database_name)
            
            db.DoQuery('CREATE TABLE bar (foo INT, boo INT, fooboobar INT)')
            db.DoQuery('INSERT INTO bar (foo, boo, fooboobar) VALUES (1,1,1)')
                
            expected_table_names = ['bee', 'baz', 'foobeebaz']
            actual_table_names = self.storage.get_column_names('foo')
                
            self.assertEqual(Set(expected_table_names), Set(actual_table_names))
            self.assertEqual(len(expected_table_names), len(actual_table_names))
            
            expected_table_names = ['foo', 'boo', 'fooboobar']
            actual_table_names = self.storage.get_column_names('bar')
                
            self.assertEqual(Set(expected_table_names), Set(actual_table_names))
            self.assertEqual(len(expected_table_names), len(actual_table_names))
            
        def test_load_table_returns_a_table_with_the_given_table_name_and_data(self):
            db = self.db_server.get_database(self.database_name)
            
            db.DoQuery('CREATE TABLE foo (a INT, b INT, c INT)')
            db.DoQuery('INSERT INTO foo (a, b, c) VALUES (1,2,3)')
            
            expected_data = {
                'a': array([1], dtype='i'),
                'b': array([2], dtype='i'),
                'c': array([3], dtype='i'),
                }
            
            actual_data = self.storage.load_table('foo')
            
            self.assertDictsEqual(expected_data, actual_data)
            
        def test_load_table_returns_a_table_with_different_table_name_and_data(self):
            db = self.db_server.get_database(self.database_name)
            
            db.DoQuery('CREATE TABLE bar (d INT, e FLOAT, f TEXT)')
            db.DoQuery('INSERT INTO bar (d, e, f) VALUES (4,5.5,"6")')
            
            expected_data = {
                'd': array([4], dtype='i'),
                'e': array([5.5], dtype='f'),
                'f': array(['6'], dtype='S'),
                }
            
            actual_data = self.storage.load_table('bar')
            
            self.assertDictsEqual(expected_data, actual_data)
            
    
    if __name__ == '__main__':
        opus_unittest.main()