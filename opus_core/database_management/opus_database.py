# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys, gc

from opus_core.database_management.engine_handlers.mssql import MSSQLServerManager
from opus_core.database_management.engine_handlers.mysql import MySQLServerManager
from opus_core.database_management.engine_handlers.postgres import PostgresServerManager
from opus_core.database_management.engine_handlers.sqlite import SqliteServerManager



from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.types import Integer, SmallInteger, \
                             Numeric, Float, \
                             VARCHAR, String, CLOB, Text,\
                             Boolean, DateTime
from sqlalchemy import create_engine

class OpusDatabase(object):
    """Represents a connection a database, administered through sqlalchemy."""

    def __init__(self, database_server_configuration, database_name,
                 show_output=False) :
        """ Connects to this database. """
        self.show_output = show_output
        
        self.protocol = database_server_configuration.protocol
        self.host_name = database_server_configuration.host_name
        self.user_name = database_server_configuration.user_name
        self.password = database_server_configuration.password
        
        if self.protocol == 'postgres':
            database_name = database_name.lower()
            self.protocol_manager = PostgresServerManager()
        elif self.protocol == 'mysql':
            self.protocol_manager = MySQLServerManager()
        elif self.protocol == 'sqlite':
            self.protocol_manager = SqliteServerManager(database_server_configuration.sqlite_db_path)
        elif self.protocol == 'mssql':
            self.protocol_manager = MSSQLServerManager()
            
        self.database_name = database_name
        self.database_server_config = database_server_configuration
        
        self.open()
        self.show_output = False

    def get_connection_string(self, scrub = False):
        return self.protocol_manager.get_connection_string(server_config = self.database_server_config,
                                                           database_name = self.database_name,
                                                           scrub = scrub)
    
    def open(self):
        self.protocol_manager.create_default_database_if_absent(self.database_server_config)

        self.engine = create_engine(self.get_connection_string())
        self.metadata = MetaData(
            bind = self.engine
        )  
        
        self.reflect(recurse = False)
    
    def reflect(self, clear = True, recurse = True):
        try:
            if clear:
                self.metadata.clear()
            if self.protocol_manager.uses_schemas:
                self.metadata.reflect(bind = self.engine, schema = self.database_name)
            else:
                self.metadata.reflect(bind = self.engine)
        except:            
            if recurse:
                self.close()
                self.open()
                self.reflect(clear = False, recurse = False)
            else:
                raise
            
    def close(self):
        """Explicitly close the connection, without waiting for object deallocation"""
        try:
            self.engine.dispose()
        except:
            pass
        self.engine = None
        self.metadata = None
        gc.collect()

    def execute(self, *args, **kwargs):
        recurse = kwargs.pop('recurse', False)

        try:
            return self.engine.execute(*args, **kwargs)
        except:
            if recurse:
                self.close()
                self.open()
                kwargs['recurse'] = True
                self.execute(*args, **kwargs)
            else:
                raise
            
    '''Deprecated: DO NOT USE'''
    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Does not return data.
        Args;
            query = an SQL statement
        """
        self.reflect()
        preprocessed_query = convert_to_mysql_datatype(query)
        if self.show_output: _log_sql(preprocessed_query)
        self.execute(preprocessed_query)
        self.reflect(clear = False)

    def GetResultsFromQuery(self, query):
        """
        Returns records from query, as a list, the first element of which is a list of field names

        Args:
            query = query to execute
        """
        self.reflect()
        preprocessed_query = convert_to_mysql_datatype(query)
        if self.show_output: _log_sql(preprocessed_query)
        result = self.execute(preprocessed_query)
        self.reflect(clear = False)
        
        results = result.fetchall()
        resultlist = [list(row) for row in results]
        
        return [[d[0] for d in result.cursor.cursor.description]] + resultlist


    def get_schema_from_table(self, table_name):
        """Returns this table's schema (a dictionary of field_name:field_type).
        """
        self.reflect()
        t = self.get_table(table_name)
        schema = {}
        for col in t.columns:
            schema[str(col.name)] = inverse_type_mapper(col.type)
        
        return schema    

    def get_table(self, table_name):
        self.reflect()
        if not self.protocol_manager.uses_schemas and self.engine.has_table(table_name = table_name):
            t = self.metadata.tables[table_name]
        elif self.protocol_manager.uses_schemas and self.engine.has_table(table_name = table_name, schema=self.database_name):
            t = self.metadata.tables['%s.%s'%(self.database_name, table_name)]
        else:
            raise Exception('Table %s not found in %s'%(table_name, self.database_name))
        return t
            
    def create_table_from_schema(self, table_name, table_schema):
        columns = []
        for col_name, type_val in table_schema.items():
            col = Column(col_name, type_mapper(type_val))
            columns.append(col)
        self.create_table(table_name, columns)
        
    def create_table(self, table_name, columns):
        """Create a table called table_name in the set database with the given
        schema (a dictionary of field_name:field_type).
        Note that table constraints are not added.
        """
        self.reflect()
        if self.table_exists(table_name): return
        
        kwargs = {}
        if self.protocol_manager.uses_schemas:
            kwargs = {'schema':self.database_name}
        
        new_table = Table(
            table_name,
            self.metadata,
            *columns,
            **kwargs      
        )
        
        new_table.create(checkfirst = True)
        return new_table

    def drop_table(self, table_name):
        if self.table_exists(table_name):
            t = self.get_table(table_name)
            t.drop(bind = self.engine)
            self.metadata.remove(t)
                
    def table_exists(self, table_name):
        self.reflect()
        
        if not self.protocol_manager.uses_schemas and \
           self.engine.has_table(table_name = table_name):
            t = self.metadata.tables[table_name]
        elif self.protocol_manager.uses_schemas and \
             self.engine.has_table(table_name = table_name, schema=self.database_name):
            t = self.metadata.tables['%s.%s'%(self.database_name, table_name)]
        else:
            return False
                
        return t.exists()

    def get_tables_in_database(self):
        """Returns a list of the tables in this database chain."""
        self.reflect()
        return self.protocol_manager.get_tables_in_database(metadata = self.metadata)
    
    def get_primary_keys_for_table(self, table):
        self.reflect()
        primary_keys = []
        for col in table.c:
            if col.primary_key:
                primary_keys.append(col)
        return primary_keys
                                            
def type_mapper(type_val):
    filter_data = {"INTEGER" : Integer,
                   "SHORT" : SmallInteger,
                   "FLOAT" : Float,
                   "DOUBLE" : Numeric,
                   "VARCHAR" : VARCHAR(255),
                   "BOOLEAN" : Boolean,
                   "TINYTEXT" : VARCHAR(255),
                   "TEXT" : Text,
                   "MEDIUMTEXT" : Text,
                   "LONGTEXT": Text,
                   "DATETIME": DateTime}
    
    return filter_data[type_val]     

def inverse_type_mapper(type_class):
    filter_data = {Integer: "INTEGER",
                   SmallInteger: "SHORT",
                   Float: "FLOAT",
                   Numeric: "DOUBLE",
                   VARCHAR: "VARCHAR",
                   Boolean: "BOOLEAN",
                   CLOB: "MEDIUMTEXT",
                   DateTime: "DATETIME",
                   String: "VARCHAR"}
    
    try:
        my_type = filter_data[type_class.__class__] 
    except:
        if isinstance(type_class, VARCHAR):
            my_type = "VARCHAR"
        elif isinstance(type_class, CLOB):
            my_type = "MEDIUMTEXT"
        elif isinstance(type_class, Boolean):
            my_type = "BOOLEAN"
        elif isinstance(type_class, SmallInteger):
            my_type = "SHORT"
        elif isinstance(type_class, Float):
            my_type = "DOUBLE"
        elif isinstance(type_class, DateTime):
            my_type = "DATETIME"
        elif isinstance(type_class, Numeric):
            my_type = "DOUBLE"
        elif isinstance(type_class, String):
            my_type = "VARCHAR"
        if isinstance(type_class, Integer):
            my_type = "INTEGER"
    
    return my_type               
        
def convert_to_mysql_datatype(query):
    filter_data = {"INTEGER" : "int(11)",
                   "SHORT" : "smallint(6)",
                   "FLOAT" : "double",
                   "DOUBLE" : "double",
                   "VARCHAR" : "varchar(255)",
                   "BOOLEAN" : "tinyint(4)",
                   "TINYTEXT" : "tinytext",
                   "MEDIUMTEXT" : "mediumtext"}

    for old, new in filter_data.iteritems():
        query = query.replace(old, new)
    return query

########## Logging utility functions from Bjorn's old globals.py #####################
def _log(s) :
    sys.stdout.write(s)
    sys.stdout.write("\n")
    sys.stdout.flush()

def _log_sql(sql_query):
    _log("SQL: " + sql_query)



import os
from opus_core.tests import opus_unittest
from opus_core.logger import logger


from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import _get_installed_database_engines
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class OpusDatabaseTest(opus_unittest.OpusTestCase):
    def setUp(self):        
        db_configs = []
        for engine in _get_installed_database_engines():
            config = TestDatabaseConfiguration(protocol = engine)
            db_configs.append(config)
        
        self.test_db = 'OpusDatabaseTestDatabase'
        test_table = 'test_table'
        
        self.dbs = []
        for config in db_configs:
            try:
                server = DatabaseServer(config)
                if server.has_database(self.test_db):
                    server.drop_database(self.test_db)
                server.create_database(self.test_db)
                self.assertTrue(server.has_database(database_name = self.test_db))
                db = OpusDatabase(database_server_configuration = config, 
                                   database_name = self.test_db)
                self.assertFalse(db.table_exists(test_table))
                self.dbs.append((db,server))
            except:
                import traceback
                traceback.print_exc()
                
                logger.log_warning('Could not start server for protocol %s'%config.protocol)
                
    def tearDown(self):
        for db, server in self.dbs:
            db.close()
            server.drop_database(self.test_db)
            server.close()
    
    def test_create_drop_and_has_table(self):        
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT"                     
        }
        test_table = 'test_table'
        
        for db, server in self.dbs:
            try:
                self.assertFalse(db.table_exists(test_table))
                
                db.create_table_from_schema(test_table, test_table_schema)
                self.assertTrue(db.table_exists(test_table))
                
                db.drop_table(test_table)
                self.assertFalse(db.table_exists(test_table))
            except:
                logger.log_error('Protocol %s'%server.config.protocol)
                raise

    def test_get_table(self):
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT"                     
        }
        test_table = 'test_table'
        
        for db, server in self.dbs:
            try:
                self.assertFalse(db.table_exists(test_table))
                db.create_table_from_schema(test_table, test_table_schema)
                t = db.get_table(test_table)
                self.assertTrue(isinstance(t,Table))
                self.assertTrue(t.name == test_table)
            except:
                logger.log_error('Protocol %s'%server.config.protocol)
                raise
                        
    def test_get_schema_from_table(self):
        import copy
        
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT",
            'col3':"DOUBLE",
            'col4':"VARCHAR",
            'col5':"BOOLEAN",
            'col6':"MEDIUMTEXT",
            'col7':"SHORT"                    
        }
        expected_schema = copy.copy(test_table_schema)  
        expected_schema.update({'col2':'DOUBLE', 'col6':'VARCHAR', 'col7':'INTEGER'})      
        
        test_table = 'test_table'
        
        for db,server in self.dbs:
            try:
                self.assertFalse(db.table_exists(test_table))
                db.create_table_from_schema(test_table, test_table_schema)
                new_schema = db.get_schema_from_table(test_table)
                self.assertEqual(new_schema, expected_schema)
            except:
                logger.log_error('Protocol %s'%server.config.protocol)
                raise
            
    def skip_test_GetResultsFromQuery(self):
        pass
    
    def skip_test_DoQuery(self):
        pass


if __name__ == '__main__':
    opus_unittest.main()