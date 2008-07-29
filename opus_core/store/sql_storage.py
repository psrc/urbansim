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
    from sqlalchemy import Table, Column, select, insert
    from sqlalchemy.types import Integer, Numeric, Text, Float, Boolean    
except ImportError:
    sqlalchemy = None
    
try:
    from sqlalchemy.databases.mysql import MSBigInteger, MSString, MSChar
    from sqlalchemy.databases.mssql import MSString as MicrosoftString
except:
    pass
    

from opus_core.store.storage import Storage
from opus_core.database_management.opus_database import OpusDatabase

class sql_storage(Storage):
    def __init__(self,  
                 storage_location):
        """
        protocol: 'sqlite', 'mysql', 'postgres', 'oracle', 'mssql', or 'firebird'
          - A corresponding module must be installed
        """
        if sqlalchemy is None:
            raise ImportError('The sqlalchemy Python module must be installed '
                'before using sql_storage. See http://www.sqlalchemy.org/')
        
        self.database_name = storage_location.database_name
        self.database_server_config = storage_location.database_server_config
        
        #we cannot store the database directly because it cannot be pickled
        #self._my_db = storage_location
        
    def _get_db(self):
        #db_server = DatabaseServer(self.database_server_config)
        #db = db_server.get_database(self.database_name)
        #db_server.close()
        #return db
        db = OpusDatabase(self.database_server_config, self.database_name)
        return db
    
    def _dispose_db(self, db):
        db.close()
        del db
        
    def get_storage_location(self):
        db = self._get_db()
        storage_location = str(db.engine.url)
        self._dispose_db(db)
        return storage_location
      
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        db = self._get_db()
        
        table = Table(table_name, db.metadata, autoload=True)
            
        available_column_names = self.get_column_names(table_name, lowercase)
        final_cols = self._select_columns(column_names, available_column_names) 
        
        if final_cols == []:
            return {}
        
        col_data = {}
        selectable_columns = []
        table_data = {}

        for column in table.columns:
            if lowercase:
                col_name = column.name.lower()
            else:
                col_name = column.name
            
            if col_name in final_cols:
                col_type = self._get_numpy_dtype_from_sql_alchemy_type(column.type)
                col_data[col_name] = (column, col_type)
                table_data[col_name] = []
                selectable_columns.append(column)
                         
        query = select(
            columns = selectable_columns
        )        
        
        query_results = db.engine.execute(query)
        
        while True:
            row = query_results.fetchone()
            if row is None: break
            for col_name, (column, col_type) in col_data.items():
                table_data[col_name].append(row[column])
                    
        for col_name, (column, col_type) in col_data.items():
            table_data[col_name] = array(table_data[col_name], dtype=col_type)
                   
        self._dispose_db(db)
        return table_data
        
        
    def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
        db = self._get_db()
        chunk_size = 1000
        
        if mode == Storage.APPEND:
            #sqlalchemy has no support for alter table syntax, so just load and reload
            old_data = self.load_table(table_name = table_name)
            old_data.update(table_data)
            table_data = old_data

        table_length, _ = self._get_column_size_and_names(table_data)
        
        columns = []
        for column_name, column_data in table_data.items():
            col_type = self._get_sql_alchemy_type_from_numpy_dtype(column_data.dtype)
            
            if column_name.find('_id') > -1 and len(column_data) == len(set(column_data)):
                col = Column(column_name,col_type,primary_key = True)
                columns.insert(0,col)
            else: 
                col = Column(column_name,col_type)
                columns.append(col)
                
            if column_data.dtype == 'i':
                table_data[column_name] = [int(cell) for cell in column_data]
            elif column_data.dtype == 'f':
                table_data[column_name] = [float(cell) for cell in column_data]
        
        if db.table_exists(table_name):
            table = db.get_table(table_name)
            table.drop(checkfirst = True)
            db.metadata.remove(table)
        table = Table(table_name, db.metadata, *columns)
        
        connection = db.engine.connect()
        try:
            try:
                table.create()
            except Exception, e:
                raise NameError('Failed to create table, possibly due to an illegal column name.\n(Original error: %s)' % e)

            transaction = connection.begin()
            try:                
                last_row = -1
                while last_row < table_length -1:
                    rows_to_insert = []
                    for row in range(last_row + 1, min(last_row + 1 + chunk_size, table_length)):
                        row_data = {}
                        for column_name in table_data.keys():
                            row_data[column_name] = table_data[column_name][row]
                        rows_to_insert.append(row_data)
                    last_row = row
                    connection.execute(table.insert(), rows_to_insert)
        
                transaction.commit()
            except:
                transaction.rollback()
                raise 
                
        finally:
            connection.close()
            self._dispose_db(db)

    def get_column_names(self, table_name, lowercase=True):
        db = self._get_db()
        if table_name not in db.metadata.tables:
            raise
        
        table = db.metadata.tables[table_name]
        
        if lowercase:
            col_names = [column.name.lower() for column in table.columns]
        else:
            col_names = [column.name for column in table.columns]
            
        self._dispose_db(db)
        return col_names
    
    def get_table_names(self):
        db = self._get_db()
        tables = [table.name for table in db.metadata.table_iterator()]
        self._dispose_db(db)
        
        # MSSQL hacking by Jesse
        # The three items in mssql_system_tables are tables (and views) created in
        # every MSSQL database.  A user should never need to cache or otherwise
        # work with these tables in OPUS (as far as I know), so I am filtering them 
        # out here.
        if self.database_server_config.protocol == 'mssql':
            mssql_system_tables = [u'sysconstraints', u'dtproperties', u'syssegments']
            for i in mssql_system_tables:
                if i in tables:
                    tables.remove(i)
        
        return tables
    
    def _get_sql_alchemy_type_from_numpy_dtype(self, column_dtype):
        mapping = {
            'i':Integer,
            'f':Float,
            'S':Text,
            'b':Boolean
            }
        
        return mapping[column_dtype.kind]
        
    def _get_numpy_dtype_from_sql_alchemy_type(self, column_type):

        try:
            if isinstance(column_type, MSBigInteger):
                return dtype('int64')
            if isinstance(column_type, MSString):
                return dtype('S')
            if isinstance(column_type, MSChar):
                return dtype('S')
        except: pass
        
        if isinstance(column_type, Integer):
            return dtype('i')
        
        if isinstance(column_type, Numeric):
            return dtype('f')
        
        if isinstance(column_type, Text):
            return dtype('S')
        
        if isinstance(column_type, Boolean):
            return dtype('b')
        
        if isinstance(column_type, MicrosoftString):
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
    from opus_core.database_management.database_server import DatabaseServer
    from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
    
    class SQLStorageTest(TestStorageInterface):
        """
        Uses MySQL and sqlite for these tests.
        """
        def setUp(self):
            self.database_name = 'test_database'
            self.protocol = 'mysql'
            
            config = DatabaseServerConfiguration()
            self.username = config.user_name
            self.hostname = config.host_name
            self.password = config.password 
            
            self.db_server = DatabaseServer(config)
            
            self.db_server.drop_database(self.database_name)
            self.db_server.create_database(self.database_name)

            # Use MySQL to test this.
            db = self.db_server.get_database(self.database_name)
            self.storage = sql_storage(
                storage_location = db
                )
            
        def tearDown(self):
            del self.storage
            self.db_server.drop_database(self.database_name)
            
            self.db_server.close()
        
#        def test_get_storage_location_returns_database_url_built_from_the_constructor_arguments_not_including_port(self):
#                
#            expected_url = '%s://%s:%s@%s/%s'%(self.protocol,self.username, self.password, self.hostname, self.database_name)
#            actual_url = self.storage.get_storage_location()
#            
#            self.assertEqual(expected_url, actual_url)

       
        def test_write_table_creates_a_table_with_the_given_table_name_and_data(self):
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'my_id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )
                
            expected_results = [(long(1),long(4)), (long(2),long(5)), (long(3),long(6))]
            
            db = self.db_server.get_database(self.database_name)
            
            tbl = db.get_table('test_write_table')
            s = select([tbl.c.my_id, tbl.c.a], order_by = tbl.c.my_id)
            results = db.engine.execute(s).fetchall()

            self.assertEqual(expected_results, results)
        
        def test_write_table_creates_a_table_with_the_given_table_name_and_data_of_different_types(self):
            
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'int_data': array([2,1]),
                    'float_data': array([2.2,1.1]),
                    'string_data': array(['foo', 'bar'])
                    }
                )
                
                            
            expected_results = [(long(1),1.1,'bar'), (long(2),2.2,'foo')]
            
            # Verify the data through a DatabaseServer database connection
            db = self.db_server.get_database(self.database_name)

            tbl = db.get_table('test_write_table')
            s = select([tbl.c.int_data, tbl.c.float_data, tbl.c.string_data], order_by = tbl.c.int_data)
            results = db.engine.execute(s).fetchall()

            self.assertEqual(expected_results, results)

        def test_write_table_properly_creates_primary_key(self):                   
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'my_id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )
            
            db = self.db_server.get_database(self.database_name)
            tbl = db.get_table('test_write_table')
            self.assertTrue(tbl.c.my_id.primary_key)
            
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'my_id': array([1,1,2,3]),
                    'a': array([4,5,6,7]),
                    }
                )
            
            db = self.db_server.get_database(self.database_name)
            tbl = db.get_table('test_write_table')
            self.assertFalse(tbl.c.my_id.primary_key)

            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )
            
            db = self.db_server.get_database(self.database_name)
            tbl = db.get_table('test_write_table')
            self.assertFalse(tbl.c.id.primary_key)


        def test_write_table_overwrite(self):
                   
            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'my_id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )

            self.storage.write_table(
                table_name = 'test_write_table', 
                table_data = {
                    'my_id': array([1,2,3]),
                    'a': array([4,5,6]),
                    }
                )                
            expected_results = [(long(1),long(4)), (long(2),long(5)), (long(3),long(6))]
            
            #Verify the data through a DatabaseServer database connection
            db = self.db_server.get_database(self.database_name)
            
            tbl = db.get_table('test_write_table')
            s = select([tbl.c.my_id, tbl.c.a], order_by = tbl.c.my_id)
            results = db.engine.execute(s).fetchall()

            self.assertEqual(expected_results, results)
                        
        def test_get_sql_alchemy_type_from_numpy_dtype(self):
            expected_sql_alchemy_type = Integer
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('i'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
            expected_sql_alchemy_type = Float
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('f'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
            expected_sql_alchemy_type = Text
            actual_sql_alchemy_type = self.storage._get_sql_alchemy_type_from_numpy_dtype(dtype('S'))
            self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
            
        def test_get_numpy_dtype_from_sql_alchemy_type(self):
            expected_numpy_type = dtype('i')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(Integer())
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
            expected_numpy_type = dtype('f')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(Float())
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
            expected_numpy_type = dtype('S')
            actual_numpy_type = self.storage._get_numpy_dtype_from_sql_alchemy_type(Text())
            self.assertEqual(expected_numpy_type, actual_numpy_type)
            
        
        def test_get_table_names_added_through_write_table(self):
            self.storage.write_table('table1', {'a':array([1])})
            self.storage.write_table('table2', {'a':array([1])})
            self.storage.write_table('table3', {'a':array([1])})
                
            expected_table_names = ['table1', 'table2', 'table3']
            actual_table_names = self.storage.get_table_names()
                
            self.assertEqual(Set(expected_table_names), Set(actual_table_names))
            self.assertEqual(len(expected_table_names), len(actual_table_names))
            
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
            
            db.engine.execute('CREATE TABLE bar (foo INT, boo INT, fooboobar INT)')
            
            tbl = db.get_table('bar')        
            i = tbl.insert(values = {'foo':1, 'boo':1, 'fooboobar':1})
            db.engine.execute(i)
                
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
            
            db.engine.execute('CREATE TABLE foo (a INT, b INT, c INT)')
                        
            tbl = db.get_table('foo')        
            i = tbl.insert(values = {'a':1, 'b':2, 'c':3})
            db.engine.execute(i)

            expected_data = {
                'a': array([1], dtype='i'),
                'b': array([2], dtype='i'),
                'c': array([3], dtype='i'),
                }
            
            actual_data = self.storage.load_table('foo')
            
            self.assertDictsEqual(expected_data, actual_data)
            
        def test_load_table_returns_a_table_with_different_table_name_and_data(self):
            db = self.db_server.get_database(self.database_name)
            
            db.engine.execute('CREATE TABLE bar (d INT, e FLOAT, f TEXT)')

            tbl = db.get_table('bar')        
            i = tbl.insert(values = {'d':4, 'e':5.5, 'f':"6"})
            db.engine.execute(i)
                  
            expected_data = {
                'd': array([4], dtype='i'),
                'e': array([5.5], dtype='f'),
                'f': array(['6'], dtype='S'),
                }
            
            actual_data = self.storage.load_table('bar')
            
            self.assertDictsEqual(expected_data, actual_data)

        def test_load_table_returns_nothing_when_no_cols_specified(self):
            db = self.db_server.get_database(self.database_name)
            
            db.engine.execute('CREATE TABLE bar (d INT, e FLOAT, f TEXT)')
            
            tbl = db.get_table('bar')        
            i = tbl.insert(values = {'d':4, 'e':5.5, 'f':"6"})
            db.engine.execute(i)

            expected_data = {}
            
            actual_data = self.storage.load_table('bar', column_names = [])
            
            self.assertDictsEqual(expected_data, actual_data)            
    
    if __name__ == '__main__':
        opus_unittest.main()