# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, dtype
from opus_core.misc import unique
from opus_core.logger import logger

import sqlalchemy
from sqlalchemy import Table, Column, select, insert
from sqlalchemy.types import Integer, Numeric, Text, Float, Boolean

from opus_core.store.storage import Storage
from opus_core.database_management.opus_database import OpusDatabase
from opus_core.database_management.engine_handlers.postgres import PGGeometry
import re

class sql_storage(Storage):
    def __init__(self,  
                 storage_location):
        """
        protocol: 'sqlite', 'mysql', 'postgres', 'oracle', 'mssql', or 'firebird'
          - A corresponding module must be installed
        """
       
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
        
        table = db.get_table(table_name) #Table(table_name, db.metadata, autoload=True)
            
        available_column_names = self.get_column_names(table_name, lowercase)
        final_cols = self._select_columns(column_names, available_column_names) 
        
        col_data = {}
        selectable_columns = []
        table_data = {}

        for column in table.columns:
            if lowercase:
                col_name = column.name.lower()
            else:
                col_name = column.name
            
            if col_name in final_cols:
                if isinstance(column.type, PGGeometry):
                    logger.log_warning('column %s ignored: Column_type not supported by Python' %col_name)
                    continue
                col_type = self._get_numpy_dtype_from_sql_alchemy_type(column.type)
                col_data[col_name] = (column, col_type)
                table_data[col_name] = []
                selectable_columns.append(column)
                
        if len(selectable_columns) == 0:
            return {}
                
        query = select(
            columns = selectable_columns
        )        
        
        query_results = db.execute(query)
        
        while True:
            row = query_results.fetchone()
            if row is None: break
            for col_name, (column, col_type) in col_data.items():
                table_data[col_name].append(row[column])
                    
        len_all = len(table_data.values()[0])

        problem_rows = set()
        problem_columns = {}
        remove_columns = {}
        for key, column in table_data.items():
            problem_rows_for_column = []
            for i in range(len_all):
                if column[i] is None:
                    problem_rows_for_column.append(i)
            num_problem_rows_for_column = len(problem_rows_for_column)
            # ignore column if it contains more than 50% NULL values
            if num_problem_rows_for_column * 2 > len(column):
                remove_columns[key] = num_problem_rows_for_column
            elif num_problem_rows_for_column > 0:
                problem_columns[key] = num_problem_rows_for_column
                problem_rows.update(problem_rows_for_column)

        len_rm = len(remove_columns)
        if len_rm > 0:
            logger.log_warning('%s of %s columns ignored in %s '
                               'due to NULL values in column(s) (with row count in parens) "%s)"' 
                               % (len_rm, len(table_data.keys()), table_name,
                               '), "'.join('%s" (%s' % (k, remove_columns[k]) for k in sorted(list(remove_columns)))))
            
            
        len_pr = len(problem_rows)
        if len_pr > 0:
            rate_failed = float(len_pr) / len_all
            rate_succeeded = 1.0 - rate_failed
            percentage_succeeded = round(100.0 * rate_succeeded, 2)
            logger.log_warning('%s of %s rows ignored in %s (%s%% successful) '
                               'due to NULL values in column(s) (with row count in parens) "%s)' 
                               % (len_pr, len_all, table_name,
                               percentage_succeeded,
                               '), "'.join('%s" (%s' % (k, problem_columns[k]) for k in sorted(list(problem_columns)))))
        
        if len_pr + len_rm == 0:
            logger.log_note('All rows and columns imported successfully')
            
        for col_name, (column, col_type) in col_data.items():
            if col_name in remove_columns:
                del table_data[col_name]
                continue
            
            try:
                clean_column_data = table_data[col_name]
                if len_pr > 0:
                    # select only those rows that can be loaded (as determined before)
                    clean_column_data = [x for (r, x) in enumerate(clean_column_data)
                                         if r not in problem_rows]
                
                # Unicode is currently NOT supported, but will be returned
                # by the database server.  To avoid import errors with non-ASCII
                # characters in Python 2.6 or earlier, encode as UTF-8
                # explicitly.  Proper Unicode support will require using the 'U'
                # column type -- a rather big change.
                #
                # See http://stackoverflow.com/a/7183618/946850 for details
                # on what will be observed if the following two lines
                # are omitted..
                if col_type.kind == 'S':
                    clean_column_data = [x.encode('utf8') for x in clean_column_data]
                    
                table_data[col_name] = array(clean_column_data, dtype=col_type)
            except:
                logger.log_error("Error occurred when exporting column %s; it may be caused by NULL values." % col_name)
                raise
                   
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

            # TODO this may be problematic: not all columns ending with '_id' and unique are primary keys
            if column_name.endswith('_id') and column_data.size == unique(column_data).size:
                col = Column(column_name,col_type,primary_key = True)
                columns.insert(0,col)
            else: 
                col = Column(column_name,col_type)
                columns.append(col)
                
            if column_data.dtype.kind == 'i':
                table_data[column_name] = [int(cell) for cell in column_data]
            elif column_data.dtype.kind == 'f':
                table_data[column_name] = [float(cell) for cell in column_data]
            elif column_data.dtype.kind == 'S':
                table_data[column_name] = [str(cell) for cell in column_data]
            elif column_data.dtype.kind == 'b':
                table_data[column_name] = [bool(cell) for cell in column_data]
        
        if db.table_exists(table_name):
            db.drop_table(table_name)
#            table = db.get_table(table_name)
#            table.drop(checkfirst = True)
#            db.metadata.remove(table)
#        table = Table(table_name, db.metadata, *columns)
        
        connection = db.engine.connect()
        try:
            try:
                table = db.create_table(table_name, columns = columns)
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
        table = db.get_table(table_name = table_name)
        
        if lowercase:
            col_names = [column.name.lower() for column in table.columns]
        else:
            col_names = [column.name for column in table.columns]
            
        self._dispose_db(db)
        return col_names

    def get_column_type_str(self, column_type, uppercase=True):
        import re
        if hasattr( column_type, "__visit_name__" ):  # sqlalchemy 0.6.0
            column_type_str = column_type.__visit_name__
        elif hasattr( column_type, "get_col_spec" ):  # sqlalchemy 0.5.8
            try:
                column_type_str = column_type.get_col_spec()
            except:
                column_type_str = str(column_type)
            column_type_str = re.sub('\(.*\)', '', column_type_str)
                
        else:
            column_type_str = str(column_type)

        if uppercase and column_type_str != str(column_type):
            column_type_str = column_type_str.upper()
            
        return column_type_str   
    
    def get_table_names(self):
        db = self._get_db()
        tables = db.get_tables_in_database()
        self._dispose_db(db)
        
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
        specified_type_mapping = {
                    'BIGINT': dtype('i8'), 
                    'SMALLINT': dtype('i'),
                    'TINYINT': dtype('i'),
                    'INTEGER': dtype('i'),
                    'NUMERIC': dtype('f'),
                    'FLOAT': dtype('f'),
                    'DOUBLE': dtype('f8'),
                    
                    'CHAR': dtype('S'),
                    'VARCHAR': dtype('S'),
                    'TEXT': dtype('S'),
                    'MEDIUMTEXT': dtype('S'),
                    'STRING': dtype('S'),
                    'UNICODE': dtype('U'),
                    
                    'BOOLEAN': dtype('b'),
                 }
        ## if a sqlalchemy type is specified in the type mapping above
        column_type_str = self.get_column_type_str(column_type, uppercase=True)
        if specified_type_mapping.has_key(column_type_str):
            return specified_type_mapping[column_type_str]
        
        ## resort to default class instance checking 
        if isinstance(column_type, Integer):
            default_type = dtype('i')
        elif isinstance(column_type, Float):
            default_type = dtype('f')
        elif isinstance(column_type, Numeric):
            default_type = dtype('f')
        elif isinstance(column_type, Text):
            default_type = dtype('S')
        elif isinstance(column_type, Boolean):
            default_type = dtype('b')
        else:
            raise TypeError, 'Unrecognized column type: %s' % column_type_str
        
        return default_type
    
if sqlalchemy is None:
    if __name__ == '__main__':
        logger.log_warning('Skipping sql_storage unit tests -- could not import the sqlalchemy module.')
    
else:
    from opus_core.tests import opus_unittest
    import os
    from opus_core.store.storage import TestStorageInterface
    from opus_core.database_management.database_server import DatabaseServer
    from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration, get_testable_engines
    
    class SQLStorageTest(TestStorageInterface):
        """
        Uses MySQL and sqlite for these tests.
        """
        def setUp(self):

            db_configs = []
            for engine in get_testable_engines():
                config = TestDatabaseConfiguration(protocol = engine)
                db_configs.append(config)
            
            self.database_name = 'test_database'
            self.dbs = []
            for config in db_configs:
                try:
                    server = DatabaseServer(config)
                    if server.has_database(self.database_name):
                        server.drop_database(self.database_name)
                    server.create_database(self.database_name)
                    self.assertTrue(server.has_database(database_name = self.database_name))
                    db = OpusDatabase(database_server_configuration = config, 
                                       database_name = self.database_name)
                    storage = sql_storage(
                                    storage_location = db
                                    )
                    self.dbs.append((db,server,storage))
                    self.storage = storage
                except:
                    import traceback
                    traceback.print_exc()
                    
                    print 'WARNING: could not start server for protocol %s'%config.protocol
            
            
        def tearDown(self):
            for db, server, storage in self.dbs:
                db.close()
                server.drop_database(self.database_name)
                server.close()
            
        def test_get_storage_location_returns_database_url_built_from_the_constructor_arguments_not_including_port(self):
            import urllib
            for db, server, storage in self.dbs:
                if db.protocol != 'sqlite':
                    if db.protocol == 'postgres':
                        host_and_db = ''
                        if db.host_name is None:
                            pass
                        elif re.match('.*/.*', db.host_name):
                            host_and_db = db.host_name
                        else:
                            host_and_db = '%s/misc' % db.host_name
                        expected_url = '%s://%s:%s@%s'%(db.protocol,
                                   db.user_name, 
                                   db.password, 
                                   host_and_db)
                    else:
                        expected_url = '%s://%s:%s@%s/%s'%("postgresql", #db.protocol,
                                   db.user_name, 
                                   db.password, 
                                   db.host_name, 
                                   db.database_name)
                    actual_url = storage.get_storage_location()
                    # It seems to have random cases where get_storage_location() returns quoted URL
                    actual_url = urllib.unquote(actual_url)
                    urls_are_equal = expected_url==actual_url
                    # Careful!  Don't put the URLs in the assertion, so if there is a failure they don't get printed in the CruiseControl log
                    self.assert_(urls_are_equal, "expected and actual URLs not equal for protocol %s" % db.protocol)

       
        def test_write_table_creates_a_table_with_the_given_table_name_and_data(self):
            for db, server, storage in self.dbs:
                try:
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'my_id': array([1,2,3]),
                            'a': array([4,5,6]),
                            }
                        )
                        
                    expected_results = [(long(1),long(4)), (long(2),long(5)), (long(3),long(6))]
                                        
                    tbl = db.get_table('test_write_table')
                    s = select([tbl.c.my_id, tbl.c.a], order_by = tbl.c.my_id)
                    results = db.execute(s).fetchall()
        
                    self.assertEqual(expected_results, results)
                except:
                    db.drop_table('test_write_table')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
                    
        def test_write_table_creates_a_table_with_the_given_table_name_and_data_of_different_types(self):
            for db, server, storage in self.dbs:
                try:
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'int_data': array([2,1]),
                            'float_data': array([2.2,1.1]),
                            'string_data': array(['foo', 'bar']),
                            'boolean_data': array([True, False]),
                            }
                        )
                        
#                    # new version of sqlit doesn't seem to need this special treatment anymore
#                    if db.database_server_config.protocol == 'sqlite':
#                        from decimal import Decimal
#                        
#                        expected_results = [(1,Decimal(str(1.1)),'bar'), (2,Decimal(str(2.2)),'foo')]
#                    else:
#                        expected_results = [(long(1),1.1,'bar'), (long(2),2.2,'foo')]
                    expected_results = [(long(1),1.1,'bar',False), (long(2),2.2,'foo',True)]
                    # Verify the data through a DatabaseServer database connection        
                    tbl = db.get_table('test_write_table')
                    s = select([tbl.c.int_data, tbl.c.float_data, tbl.c.string_data, tbl.c.boolean_data], order_by = tbl.c.int_data)
                    results = db.execute(s).fetchall()
                    
                    self.assertEqual(expected_results, results)
                except:
                    db.drop_table('test_write_table')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
                
        def test_write_table_properly_creates_primary_key(self):  
            for db, server, storage in self.dbs:
                try:
                 
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'my_id': array([1,2,3]),
                            'a': array([4,5,6]),
                            }
                        )
                    
                    tbl = db.get_table('test_write_table')
                    self.assertTrue(tbl.c.my_id.primary_key)
                                        
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'my_id': array([1,1,2,3]),
                            'a': array([4,5,6,7]),
                            }
                        )
                    
                    tbl = db.get_table('test_write_table')
                    self.assertFalse(tbl.c.my_id.primary_key)
        
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'id': array([1,2,3]),
                            'a': array([4,5,6]),
                            }
                        )
                    
                    tbl = db.get_table('test_write_table')
                    self.assertFalse(tbl.c.id.primary_key)
                except:
                    db.drop_table('test_write_table')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise

        def test_write_table_overwrite(self):
            for db, server, storage in self.dbs:
                try:

                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'my_id': array([1,2,3]),
                            'a': array([4,5,6]),
                            }
                        )
        
                    storage.write_table(
                        table_name = 'test_write_table', 
                        table_data = {
                            'my_id': array([1,2,3]),
                            'a': array([4,5,6]),
                            }
                        )                
                    expected_results = [(long(1),long(4)), (long(2),long(5)), (long(3),long(6))]
                    
                    #Verify the data through a DatabaseServer database connection
                    tbl = db.get_table('test_write_table')
                    s = select([tbl.c.my_id, tbl.c.a], order_by = tbl.c.my_id)
                    results = db.execute(s).fetchall()
        
                    self.assertEqual(expected_results, results)
                except:
                    db.drop_table('test_write_table')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise                        
        def test_get_sql_alchemy_type_from_numpy_dtype(self):
            for db, server, storage in self.dbs:
                try:

                    expected_sql_alchemy_type = Integer
                    actual_sql_alchemy_type = storage._get_sql_alchemy_type_from_numpy_dtype(dtype('i'))
                    self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
                    
                    expected_sql_alchemy_type = Float
                    actual_sql_alchemy_type = storage._get_sql_alchemy_type_from_numpy_dtype(dtype('f'))
                    self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
                    
                    expected_sql_alchemy_type = Text
                    actual_sql_alchemy_type = storage._get_sql_alchemy_type_from_numpy_dtype(dtype('S'))
                    self.assertEqual(expected_sql_alchemy_type, actual_sql_alchemy_type)
                except:
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
                
        def test_get_numpy_dtype_from_sql_alchemy_type(self):
            for db, server, storage in self.dbs:
                try:

                    expected_numpy_type = dtype('i')
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(Integer())
                    self.assertEqual(expected_numpy_type, actual_numpy_type)
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(server.engine.dialect.type_descriptor(Integer))
                    self.assertEqual(expected_numpy_type, actual_numpy_type)

                    
                    expected_numpy_type = dtype('f')
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(Float())
                    self.assertEqual(expected_numpy_type, actual_numpy_type)
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(server.engine.dialect.type_descriptor(Float))
                    self.assertEqual(expected_numpy_type, actual_numpy_type)
                    
                    expected_numpy_type = dtype('S')
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(Text())
                    self.assertEqual(expected_numpy_type, actual_numpy_type)
                    actual_numpy_type = storage._get_numpy_dtype_from_sql_alchemy_type(server.engine.dialect.type_descriptor(Text))
                    self.assertEqual(expected_numpy_type, actual_numpy_type)
                    
                except:
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise            
        
        def test_get_table_names_added_through_write_table(self):
            for db, server, storage in self.dbs:
                try:

                    storage.write_table('table1', {'a':array([1])})
                    storage.write_table('table2', {'a':array([1])})
                    storage.write_table('table3', {'a':array([1])})
                    
                    expected_table_names = ['table1', 'table2', 'table3']
                    
                    actual_table_names = storage.get_table_names()
                        
                    self.assertEqual(set(expected_table_names), set(actual_table_names))
                    self.assertEqual(len(expected_table_names), len(actual_table_names))
                except:
                    db.drop_table('table1')
                    db.drop_table('table2')
                    db.drop_table('table3')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
            
        def test_get_column_names(self):
            for db, server, storage in self.dbs:
                try:

                    storage.write_table(
                        table_name = 'foo', 
                        table_data = {
                            'bee': array([1]),
                            'baz': array([1]),
                            'foobeebaz': array([1])
                            }
                        )
                    
                    schema = {
                        'foo': 'INTEGER',
                        'boo': 'INTEGER',
                        'fooboobar': 'INTEGER'
                    }
                    db.create_table_from_schema(table_name = 'bar', table_schema = schema)
                                        
                    tbl = db.get_table('bar')        
                    i = tbl.insert(values = {'foo':1, 'boo':1, 'fooboobar':1})
                    db.execute(i)
                        
                    expected_table_names = ['bee', 'baz', 'foobeebaz']
                    actual_table_names = storage.get_column_names('foo')
                        
                    self.assertEqual(set(expected_table_names), set(actual_table_names))
                    self.assertEqual(len(expected_table_names), len(actual_table_names))
                    
                    expected_table_names = ['foo', 'boo', 'fooboobar']
                    actual_table_names = storage.get_column_names('bar')
                        
                    self.assertEqual(set(expected_table_names), set(actual_table_names))
                    self.assertEqual(len(expected_table_names), len(actual_table_names))
                except:
                    db.drop_table('foo')
                    db.drop_table('bar')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
            
        def test_load_table_returns_a_table_with_the_given_table_name_and_data(self):
            for db, server, storage in self.dbs:
                try:

                    schema = {
                        'a': 'INTEGER',
                        'b': 'INTEGER',
                        'c': 'INTEGER'
                    }
                    db.create_table_from_schema(table_name = 'foo', table_schema = schema)
                                                    
                    tbl = db.get_table('foo')        
                    i = tbl.insert(values = {'a':1, 'b':2, 'c':3})
                    db.execute(i)
        
                    expected_data = {
                        'a': array([1], dtype='i'),
                        'b': array([2], dtype='i'),
                        'c': array([3], dtype='i'),
                        }
                    
                    actual_data = storage.load_table('foo')
                    
                    self.assertDictsEqual(expected_data, actual_data)
                except:
                    db.drop_table('foo')

                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
            
        def test_load_table_returns_a_table_with_different_table_name_and_data(self):
            for db, server, storage in self.dbs:
                try:

                    schema = {
                        'd': 'INTEGER',
                        'e': 'FLOAT',
                        'f': 'TEXT'
                    }
                    db.create_table_from_schema(table_name = 'bar', table_schema = schema)
                            
                    tbl = db.get_table('bar')        
                    i = tbl.insert(values = {'d':4, 'e':5.5, 'f':"6"})
                    db.execute(i)
                          
                    expected_data = {
                        'd': array([4], dtype='i'),
                        'e': array([5.5], dtype='f'),
                        'f': array(['6'], dtype='S'),
                        }
                    
                    actual_data = storage.load_table('bar')
                    
                    self.assertDictsEqual(expected_data, actual_data)
                except:
                    db.drop_table('bar')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise

        def test_load_empty_table(self):
            for db, server, storage in self.dbs:
                try:

                    schema = {
                        'd': 'INTEGER',
                        'e': 'FLOAT',
                        'f': 'TEXT',
                        'g': 'INTEGER',
                    }
                    db.create_table_from_schema(table_name = 'bar', table_schema = schema)
                            
                    tbl = db.get_table('bar') #@UnusedVariable
                          
                    expected_data = {
                        'd': array([], dtype='i'),
                        'e': array([], dtype='f'),
                        'f': array([], dtype='S'),
                        'g': array([], dtype='i'),
                        }
                    
                    actual_data = storage.load_table('bar')
                    
                    self.assertDictsEqual(expected_data, actual_data)
                except:
                    db.drop_table('bar')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise

        def test_load_table_ignores_rows_with_null_values(self):
            for db, server, storage in self.dbs:
                try:

                    schema = {
                        'd': 'INTEGER',
                        'e': 'FLOAT',
                        'f': 'TEXT',
                        'g': 'INTEGER',
                    }
                    db.create_table_from_schema(table_name = 'bar', table_schema = schema)
                            
                    tbl = db.get_table('bar')        
                    i = tbl.insert(values = {'d':4, 'e':5.5, 'f':"6", 'g':None})
                    db.execute(i)
                    i = tbl.insert(values = {'d':7, 'e':8.75, 'f':None, 'g':None})
                    db.execute(i)
                    i = tbl.insert(values = {'d':1, 'e':2.25, 'f':"3", 'g':None})
                    db.execute(i)
                          
                    expected_data = {
                        'd': array([4, 1], dtype='i'),
                        'e': array([5.5, 2.25], dtype='f'),
                        'f': array(['6', '3'], dtype='S'),
                        }
                    
                    actual_data = storage.load_table('bar')
                    
                    self.assertDictsEqual(expected_data, actual_data)
                except:
                    db.drop_table('bar')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise

        def test_load_table_returns_nothing_when_no_cols_specified(self):
            for db, server, storage in self.dbs:
                try:
                    schema = {
                        'd': 'INTEGER',
                        'e': 'FLOAT',
                        'f': 'TEXT'
                    }
                    db.create_table_from_schema(table_name = 'bar', table_schema = schema)
                                        
                    tbl = db.get_table('bar')        
                    i = tbl.insert(values = {'d':4, 'e':5.5, 'f':"6"})
                    db.execute(i)
        
                    expected_data = {}
                    
                    actual_data = storage.load_table('bar', column_names = [])
                    
                    self.assertDictsEqual(expected_data, actual_data)            
                except:
                    db.drop_table('bar')
                    print 'ERROR: protocol %s'%server.config.protocol
                    raise
                    
    if __name__ == '__main__':
        opus_unittest.main()
