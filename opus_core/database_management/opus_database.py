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

import sys

from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration 

from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.types import Integer, SmallInteger, \
                             Numeric, Float, \
                             VARCHAR, String, CLOB, \
                             Boolean, DateTime
from sqlalchemy import create_engine

### TODO: Add unit tests.
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
        self.database_name = database_name
        self.database_server_config = database_server_configuration
        
        self.open()
        self.show_output = False

    def get_connection_string(self):
        return '%s://%s:%s@%s/%s'%(self.protocol, self.user_name, self.password, self.host_name, self.database_name) 
    
    def open(self):
        self.engine = create_engine(self.get_connection_string())
        self.metadata = MetaData(
            bind = self.engine,
            reflect = True
        )  
        
        
    def close(self):
        """Explicitly close the connection, without waiting for object deallocation"""
        self.engine.dispose()
        self.engine = None
        self.metadata = None
        
    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Does not return data.
        Args;
            query = an SQL statement
        """
        engine = self.engine
        preprocessed_query = convert_to_mysql_datatype(query)
        _log_sql(preprocessed_query, self.show_output)
        engine.execute(preprocessed_query)
        self.metadata.reflect()

    def GetResultsFromQuery(self, query):
        """
        Returns records from query, as a list, the first element of which is a list of field names

        Args:
            query = query to execute
        """
        engine = self.engine
        preprocessed_query = convert_to_mysql_datatype(query)
        _log_sql(preprocessed_query, self.show_output)
        result = engine.execute(preprocessed_query)
        self.metadata.reflect()
        
        results = result.fetchall()
        resultlist = [list(row) for row in results]
        
        return [[d[0] for d in result.cursor.cursor.description]] + resultlist


    def get_schema_from_table(self, table_name):
        """Returns this table's schema (a dictionary of field_name:field_type).
        """
        t = self.get_table(table_name)
        schema = {}
        for col in t.columns:
            schema[col.name] = inverse_type_mapper(col.type)
        
        return schema    

    def get_table(self, table_name):
        if self.table_exists(table_name):
            return self.metadata.tables[table_name]
        raise 'Table %s not found in %s'%(table_name, self.database_name)
    
    def create_table(self, table_name, table_schema):
        """Create a table called table_name in the set database with the given
        schema (a dictionary of field_name:field_type).
        Note that table constraints are not added.
        """

        if self.table_exists(table_name): return
        
        columns = []
        for col_name, type_val in table_schema.items():
            col = Column(col_name, type_mapper(type_val))
            columns.append(col)
            
        new_table = Table(
            table_name,
            self.metadata,
            *columns                  
        )
        
        new_table.create(checkfirst = True)
        self.metadata.reflect()

    def drop_table(self, table_name):
        if self.table_exists(table_name):
            t = self.metadata.tables[table_name]
            t.drop(bind = self.engine)
            self.metadata.reflect()
                
    def table_exists(self, table_name):
        self.metadata.reflect()
        if not table_name in self.metadata.tables:
            return False
        t = self.metadata.tables[table_name]
        return t.exists()

    def get_tables_in_database(self):
        """Returns a list of the tables in this database chain."""
        return self.metadata.tables.keys()
    
    def get_primary_keys_for_table(self, table):
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
                   "TEXT" : CLOB,
                   "MEDIUMTEXT" : CLOB,
                   "LONGTEXT": CLOB,
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
            my_type = "FLOAT"
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
                   "FLOAT" : "float",
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

def _log_sql(sql_query, show_output=False):
    if show_output == True:
        _log("SQL: " + sql_query)



import os
from numpy import int32, int64
from opus_core.tests import opus_unittest
from opus_core.logger import logger


from opus_core.database_management.database_server import DatabaseServer

class OpusDatabaseTest(opus_unittest.OpusTestCase):
    def setUp(self):
        
        config = DatabaseServerConfiguration(protocol = 'mysql',
                                             test = True)
        self.test_db = 'OpusDatabaseTestDatabase'
        self.server = DatabaseServer(config)
        if self.server.has_database(self.test_db):
            self.server.drop_database(self.test_db)
        self.server.create_database(self.test_db)
        self.db = OpusDatabase(database_server_configuration = config, 
                               database_name = self.test_db)
        
    def tearDown(self):
        self.server.drop_database(self.test_db)
        self.server.close()
    
    def test_create_drop_and_has_table(self):        
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT"                     
        }
        test_table = 'test_table'
        
        self.assertFalse(self.db.table_exists(test_table))
        
        self.db.create_table(test_table, test_table_schema)
        self.assertTrue(self.db.table_exists(test_table))
        
        self.db.drop_table(test_table)
        self.assertFalse(self.db.table_exists(test_table))

    def test_get_table(self):
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT"                     
        }
        test_table = 'test_table'
        self.assertFalse(self.db.table_exists(test_table))
        self.db.create_table(test_table, test_table_schema)
        t = self.db.get_table(test_table)
        self.assertTrue(isinstance(t,Table))
        self.assertTrue(t.name == test_table)
            
    def test_get_schema_from_table(self):
        
        test_table_schema = {
            'col1':"INTEGER",
            'col2':"FLOAT",
            'col3':"DOUBLE",
            'col4':"VARCHAR",
            'col5':"BOOLEAN",
            'col6':"MEDIUMTEXT",
            'col7':"SHORT"                    
        }
        
        test_table = 'test_table'
        self.assertFalse(self.db.table_exists(test_table))
        self.db.create_table(test_table, test_table_schema)
        new_schema = self.db.get_schema_from_table(test_table)
        self.assertEqual(test_table_schema, new_schema)

    def test_GetResultsFromQuery(self):
        pass
    
    def test_DoQuery(self):
        pass

    


if __name__ == '__main__':
    opus_unittest.main()