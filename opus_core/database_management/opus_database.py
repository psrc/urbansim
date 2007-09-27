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

import sys, re

from numpy import array
from numpy import rec

from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration 

from sqlalchemy.schema import MetaData, Column, Table
from sqlalchemy.types import Integer, SmallInteger, \
                             Numeric, Float, \
                             VARCHAR, TEXT, String, CHAR, CLOB, \
                             Boolean 
from sqlalchemy import create_engine

### TODO: Add unit tests.
class OpusDatabase(object):
    """Base class for OPUS databases.

    This class supports 'database chaining', where tables in a database shadow
    tables in a 'parent' database (specified in the database's scenario_information table).
    This provides a mechanism for version control in databases, and allows simulations
    to use data from specific versions of tables - which makes it easier to update tables
    without changing what existing runs see.  Queries including a $$. as the table name,
    e.g. "select * from $$.jobs", are pre-processed to replace the $$ with the name of the
    database containing the table.
    """

    def __init__(self, database_server_configuration, database_name,
                 show_output=False) :
        """ Connects to this database. """
        self.show_output = show_output
        
        self.protocol = database_server_configuration.protocol
        self.host_name = database_server_configuration.host_name
        self.user_name = database_server_configuration.user_name
        self.password = database_server_configuration.password
        self.database_name = database_name
        
        self.engine = create_engine(self.get_connection_string())
        self.metadata = MetaData(
            bind = self.engine,
            reflect = True
        )  
        
        self.show_output = False

    def get_connection_string(self):
        return '%s://%s:%s@%s/%s'%(self.protocol, self.user_name, self.password, self.host_name, self.database_name) 
    
    def close(self):
        """Explicitly close the connection, without waiting for object deallocation"""
        self.engine.dispose()
        
    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Before executing the statement, it substitutes for an term of the form
        "$$.table_name" the correct database for where the table is stored.
        Does not return data.
        Args;
            query = an SQL statement, possibly containing $$.table_name terms
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
            query = query to execute, possibly containing $$.table_name terms
        """
        engine = self.engine
        preprocessed_query = convert_to_mysql_datatype(query)
        _log_sql(preprocessed_query, self.show_output)
        result = engine.execute(preprocessed_query)
        self.metadata.reflect()
        
        results = result.fetchall()
        resultlist = list(map(lambda x: list(x), results))
        print 'resultlist = list comprehension: ', resultlist == [list(row) for row in results]
        print 'descriptionlist = list comprehension: ', [map(lambda x: x[0], result.cursor.cursor.description)] == [d[0] for d in result.cursor.cursor.description]
        return [map(lambda x: x[0], result.cursor.cursor.description)] + resultlist


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

    def drop_table(self, table_name):
        if self.table_exists(table_name):
            t = self.metadata.tables[table_name]
            t.drop(bind = self.engine)
                
    def table_exists(self, table_name):
        if not table_name in self.metadata.tables:
            return False
        t = self.metadata.tables[table_name]
        return t.exists()

    '''this method is unused right now...'''
    def get_results_from_query(self, query):
        return self.GetResultsFromQuery(query)[1:]

    def get_tables_in_database(self):
        """Returns a list of the tables in this database chain."""
        return self.metadata.tables.keys()
                                            
def type_mapper(type_val):
    filter_data = {"INTEGER" : Integer,
                   "SHORT" : SmallInteger,
                   "FLOAT" : Float,
                   "DOUBLE" : Numeric,
                   "VARCHAR" : VARCHAR(255),
                   "BOOLEAN" : Boolean,
                   "TINYTEXT" : VARCHAR(255),
                   "MEDIUMTEXT" : CLOB}
    
    return filter_data[type_val]     

def inverse_type_mapper(type_class):
    filter_data = {Integer: "INTEGER",
                   SmallInteger: "SHORT",
                   Float: "FLOAT",
                   Numeric: "DOUBLE",
                   VARCHAR: "VARCHAR",
                   Boolean: "BOOLEAN",
                   CLOB: "MEDIUMTEXT"}
    
    return filter_data[type_class.__class__]                
        
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

    '''need to replace this one...'''
#    def DoQueries(self, sql_statements):
#        """Iterate through a string of multiple (more than one) mysql statements
#        and execute each statement as a query.
#        Does not return data.
#        Args:
#            sql_statements = triple-quoted string of multiple sql statements
#                             (separated by a semicolon, of course)
#        """
#        statements = sql_statements.split(";")
#        for query in statements :
#            query = query.strip()
#            if query:
#                cursor = self.db.cursor()
#                preprocessed_query = self.convert_to_mysql_datatype(preprocessed_query)
#                _log_sql(preprocessed_query, self.show_output)
#                cursor.execute(preprocessed_query)

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