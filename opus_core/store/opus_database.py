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

import os, sys, re, shutil, time
import pickle, traceback

from numpy import array
from numpy import rec

from opus_core.logger import logger
from opus_core.misc import reverse_dictionary
from opus_core.exception.mysqldb_import_exception import MySqlDbImportException
from opus_core.exception.cant_connect_to_mysql_exception import CantConnectToMySqlException


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

    def __init__(self, hostname=None, username=None, password=None, database_name=None,
                 show_output=False) :
        """ Returns a connection to this database.
        If database does not exist, it first creates it.
        'database' is a required parameter; if
        left as None, failure is certain, but it is named nonetheless so that the signature is flexible. """
        self.show_output = show_output
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        try:
            from MySQLdb import connect
            from MySQLdb import OperationalError
        except ImportError, e:
            raise MySqlDbImportException(e)
        try:
            self.db = connect(host=self.hostname, user=self.username, passwd=self.password, db=database_name)
        except OperationalError, e:
            raise CantConnectToMySqlException(e)
        self.cursor = self.db.cursor()

    def close(self):
        """Explicitly close the connection, without waiting for object deallocation"""
        self.cursor.close()
        self.db.close()

    def database_name_for(self, table_name):
        return self.database_name

    def database_and_table_for( self, table_name ):
        database_name = self.database_name_for(table_name)
        if database_name is None:
            raise LookupError("Table '%s' not found in database chain!"
                % table_name)
        else:
            return '%s.%s' % (database_name, table_name)

    def find_and_fill_in_table_names(self, sql_string):
        """Find all instances of '$$' in the input sql_string and replace them with the correct database
            name for where that table lives"""
        return re.sub(r'(\$\$).(\w+)',
            lambda match: self.database_and_table_for(match.group(2)),
            sql_string)

    def DoQuery(self, query):
        """
        Executes an SQL statement that changes data in some way.
        Before executing the statement, it substitutes for an term of the form
        "$$.table_name" the correct database for where the table is stored.
        Does not return data.
        Args;
            query = an SQL statement, possibly containing $$.table_name terms
        """
        cursor = self.db.cursor()
        preprocessed_query = self.find_and_fill_in_table_names(query)
        preprocessed_query = self.convert_to_mysql_datatype(preprocessed_query)
        _log_sql(preprocessed_query, self.show_output)
        cursor.execute(preprocessed_query)

    def DoQueries(self, sql_statements):
        """Iterate through a string of multiple (more than one) mysql statements
        and execute each statement as a query.
        Does not return data.
        Args:
            sql_statements = triple-quoted string of multiple sql statements
                             (separated by a semicolon, of course)
        """
        statements = sql_statements.split(";")
        for query in statements :
            query = query.strip()
            if query:
                cursor = self.db.cursor()
                preprocessed_query = self.find_and_fill_in_table_names(query)
                preprocessed_query = self.convert_to_mysql_datatype(preprocessed_query)
                _log_sql(preprocessed_query, self.show_output)
                cursor.execute(preprocessed_query)

    def GetResultsFromQuery(self, query):
        """
        Returns records from query, as a list, the first element of which is a list of field names
                Before executing the statement, it substitutes for an term of the form
        "$$.table_name" the correct database for where the table is stored.
        Args:
            query = query to execute, possibly containing $$.table_name terms
        """
        cursor = self.db.cursor()
        preprocessed_query = self.find_and_fill_in_table_names(query)
        _log_sql(preprocessed_query, self.show_output)
        cursor.execute(preprocessed_query)
        resultlist = list(map(lambda x: list(x), cursor.fetchall()))

        return [map(lambda x: x[0], cursor.description)] + resultlist

    def get_results_from_query(self, query):
        return self.GetResultsFromQuery(query)[1:]

    def get_results_from_query_as_tuple_list(self, query):
        """
        Returns records from query, as a list of tuples.
        Before executing the statement, it substitutes for an term of the form
        "$$.table_name" the correct database for where the table is stored.
        Args:
            query = query to execute, possibly containing $$.table_name terms
        """
        cursor = self.db.cursor()
        preprocessed_query = self.find_and_fill_in_table_names(query)
        _log_sql(preprocessed_query, self.show_output)
        cursor.execute(preprocessed_query)
        return list(cursor.fetchall())

    def GetResultsFromQueries(self, sql_statements):
        """Iterate through a string of multiple (more than one) mysql statements
        and execute each statement as a query.
        Returns a list, where each element is a list itself that encapsulates two more lists, the first
        list contains the sql command executed, and the second list contains result(s)
        Args:
            sql_statements = triple-quoted string of multiple sql statements
                             (separated by a semicolon, of course)
        """
        resultslist = []
        statements = sql_statements.split(";")
        for query in statements :
            query = query.strip()
            if query:
                cursor = self.db.cursor()
                preprocessed_query = self.find_and_fill_in_table_names(query)
                _log_sql(preprocessed_query, self.show_output)
                cursor.execute(preprocessed_query)
                resultslist.append([map(lambda x: x[0], cursor.description)] + map(lambda x: list(x), cursor.fetchall()))

        return resultslist

    def get_schema_from_table(self, table_name):
        """Returns this table's schema (a dictionary of field_name:field_type).
        """
        results = self.get_results_from_query('describe %s' % table_name)
        result_list = list(map(lambda x: list(x), results))
        schema = {}
        for row in result_list:
            schema[row[0]] = row[1]
        return schema

    def DoMultiInsertsFromResultListInto(self, table_name, result_list):
        """
        Performs the insertion into table_name of the results returned in the
        format as from a GetResultsFromQuery call.
        """
        cursor = self.db.cursor()

        # Get string specifying column names
        col_str = ','.join(result_list[0])

        multi_insert_count = 0
        total_count = 1
        values_str = ""
        for row in result_list[1:]:
            multi_insert_count += 1
            total_count += 1

            # Remove the list's enclosing square brackets
            filtered_row = str(row)[1:-1]

            # Remove trailing "L" on Python longs
            python_longs = re.findall(r"\dL", filtered_row)
            for python_long in python_longs: # python_long looks like '42L' or 42L', so drop the L
                filtered_row = re.sub(python_long, re.sub(r"L", "", python_long), filtered_row)

            # Replace "None" with "NULL"
            filetered_row = re.sub(r"None", "NULL", filtered_row)
            values_str += '(%s)' % filetered_row

            # Gather 100 insertions before actually doing the insert.
            if multi_insert_count < 100 and total_count < len(result_list):
                values_str += ", "
            else:
                sql = "INSERT INTO %s (%s) VALUES %s" % (table_name, col_str, values_str)
                cursor.execute(sql)
                multi_insert_count = 0
                values_str = ""

    def get_tables_in_database(self):
        """Returns a list of the tables in this database chain."""
        table_names = []
        cursor = self.db.cursor()
        sql = "show tables;"
        _log_sql(sql, self.show_output)
        cursor.execute(sql)
        tables = cursor.fetchall()
        for table in tables:
            table_names.append(table[0])
        return table_names

    def drop_tables(self, tables) :
        """Drop every table in this list"""
        for table in tables :
            self.drop_table(table)

    def drop_table(self, table) :
        """Drop this table from this database."""
        cursor = self.db.cursor()
        sql = "DROP TABLE IF EXISTS " + table + ";"
        _log_sql(sql, self.show_output)
        cursor.execute(sql)

    def create_table(self, table_name, table_schema):
        """Create a table called table_name in the set database with the given
        schema (a dictionary of field_name:field_type).
        """

        field_definitions = []
        for key, value in table_schema.iteritems():
            field_definitions.append(key + " " + value)
        self.DoQuery("CREATE TABLE IF NOT EXISTS %s (%s);" % (table_name,
                                                              ",".join(field_definitions)))

    def drop_database(self, database):
        cursor = self.db.cursor()
        sql = "DROP DATABASE IF EXISTS " + database + ";"
        _log_sql(sql, self.show_output)
        cursor.execute(sql)

    def copy_db_to(self, new_database_name, new_host=None, new_user=None, new_pass=None):
        """A simple copy utility that reads and writes row by row."""
        if new_host == None:
            new_host = self.hostname
        if new_user == None:
            new_user = self.username
        if new_pass == None:
            new_pass = self.password
        cursor = self.db.cursor()
        new_connection = OpusDatabase(hostname = new_host,
                                      username = new_user,
                                      password = new_pass,
                                      database_name = new_database_name)
        table_names = self.get_tables_in_database()
        for table_name in table_names:
            timenow = time.time()
            new_connection.DoQuery("CREATE TABLE " + table_name + \
                " SELECT * FROM " + self.database_name + "." + table_name)
            logger.log_status("Time to copy table " + table_name + " = " + str(time.time() - timenow))

    def table_exists(self, table_name):
        cursor = self.db.cursor()
        exists_sql = "SHOW TABLES LIKE '%s';" % table_name
        cursor.execute(exists_sql)
        c = cursor.fetchall()

        # if there is something in the results, the table exists
        return (len(c) > 0)


########## Functions migrated from Hana's version of MultiDB 5/27/05 ##################

    def get_dictionary_from_query(self, query, replace_nulls_with=0.0):
        replace_nulls_with = 0.0

        cursor = self.db.cursor()

        preprocessed_query = self.find_and_fill_in_table_names(query)

        _log_sql(preprocessed_query, self.show_output)
        cursor.execute(preprocessed_query)

        resultlist = list(map(lambda x: list(x), cursor.fetchall()))
        column_names = map(lambda x: x[0], cursor.description)
        types = map(lambda x: x[1], cursor.description)

        return self._make_dictionary(resultlist, column_names, types, replace_nulls_with)

    def _make_dictionary(self, resultlist, column_names, mysql_types, replace_nulls_with=0.0):
        numpy_types = map(lambda mysql_type: self._numpy_type_for_mysql_type(mysql_type), mysql_types)

        result = {}
        for i in range(len(column_names)):
            attribute_name = column_names[i]
            attribute_type = numpy_types[i]

            col = []
            for row in resultlist:
                col.append(row[i])

            dealing_with_strings = attribute_type.startswith('a')

            no_none_col = col[:]
            for i in range(len(no_none_col)):
                if no_none_col[i] is None:
                    if dealing_with_strings:
                        no_none_col[i] = str(replace_nulls_with)
                    else:
                        no_none_col[i] = replace_nulls_with

            if dealing_with_strings:
                result[attribute_name] = array(no_none_col)
            else:
                result[attribute_name] = array(no_none_col, dtype=attribute_type)

        return result

    def GetRecordArrayFromQuery(self, query, replace_nulls_with, lowercase=0):
        """
        Returns records from query, as a numpy record
        Args:
            query = query to execute
            replace_nulls_with = value that Null entries are replaced with
        """
        cursor = self.db.cursor()
        preprocessed_query = self.find_and_fill_in_table_names(query)
        _log_sql(preprocessed_query, self.show_output)
        cursor.execute(preprocessed_query)
        resultlist = list(map(lambda x: list(x), cursor.fetchall()))
        column_names = map(lambda x: x[0], cursor.description)
        mysql_types = map(lambda x: x[1], cursor.description)
        if not resultlist:
            logger.log_warning('Zero records returned for query "%s"' % query)
            return self._column_names_and_types(column_names, mysql_types, lowercase)
        return self._record_array_from_list(resultlist, column_names, mysql_types, replace_nulls_with, lowercase)

    def TryWithoutExitGetRecordArrayFromQuery(self, query, replace_nulls_with, lowercase=0):
        """GetRecordArrayFromQuery enclosed in try but do not exit if no success."""
        try:
            return self.GetRecordArrayFromQuery(query, replace_nulls_with, lowercase)
        except:
            return -1

    def ExtractFieldNames(self, cursor):
        """
        Returns the field names from an already-executed cursor.
        Arg:
            cursor = a cursor object
        """
        fieldnames = []
        for row in cursor.description:
            fieldnames.append(row[0])

        return fieldnames

    def CreateTable(self, table_name, columnname_type_pairlist, index = None):
        column_definition = "("
        for icol in range(len(columnname_type_pairlist))[:-1]:
            columnname, type = columnname_type_pairlist[icol]
            column_definition = column_definition + columnname + " " + type + ", "
        columnname, type = columnname_type_pairlist[-1]
        column_definition = column_definition + columnname + " " + type
        if index <> None:
            column_definition = column_definition + ", INDEX ("
            for ind in index[:-1]:
                column_definition = column_definition + ind + ", "
            column_definition = column_definition + index[-1] + ")"
        column_definition = column_definition + ")"
        query = "CREATE TABLE IF NOT EXISTS " + table_name + " " + column_definition
        query = self.convert_to_mysql_datatype(query)
        self.DoQuery(query)

    def DeleteTable(self, table_name):
        query = "DELETE FROM " + table_name
        self.DoQuery(query)

    def convert_to_mysql_datatype(self, query):
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

    def _numpy_type_for_mysql_type(self, mysql_type):
        """Return numpy type for this MySQL field type."""
        from MySQLdb.constants import FIELD_TYPE

        return {
            FIELD_TYPE.DECIMAL: 'float64', # probably won't work.
            FIELD_TYPE.TINY: 'int8',
            FIELD_TYPE.SHORT: 'int16',
            FIELD_TYPE.LONG: 'int32',
            FIELD_TYPE.FLOAT: 'float32',
            FIELD_TYPE.DOUBLE: 'float64',
            #FIELD_TYPE.NULL = 6
            #FIELD_TYPE.TIMESTAMP = 7
            FIELD_TYPE.LONGLONG: 'int64',
            FIELD_TYPE.INT24: 'int32', # There is no int24/i3 numpy type.
            #FIELD_TYPE.DATE = 10
            #FIELD_TYPE.TIME = 11
            #FIELD_TYPE.DATETIME = 12
            #FIELD_TYPE.YEAR = 13
            #FIELD_TYPE.NEWDATE = 14
            #FIELD_TYPE.NEWDECIMAL: 'float64',  # TODO: This field does not exist in Python 2.3.5
            #FIELD_TYPE.ENUM = 247
            #FIELD_TYPE.SET = 248
            FIELD_TYPE.TINY_BLOB: 'a255',
            FIELD_TYPE.MEDIUM_BLOB: 'a255',
            FIELD_TYPE.LONG_BLOB: 'a255',
            FIELD_TYPE.BLOB: 'a255',
            FIELD_TYPE.VAR_STRING: 'a255',
            FIELD_TYPE.STRING: 'a255',
            #FIELD_TYPE.GEOMETRY = 255
            }[mysql_type]

    _numpy_type_to_mysql_type_map = {
        "?": "TINYINT(1)",
        "b": "TINYINT", #int8
        "h": "SMALLINT", #int16
        "l": "INT", #int32
        "i": "INT",
        "q": "BIGINT", # int64
        "f": "FLOAT", # float32
        "d": "DOUBLE", #float64
        "g": "DOUBLE",
        }


    def get_mysql_type_from_numpy(self, numpy_type):
        return self._numpy_type_to_mysql_type_map[str(numpy_type)]

    def _record_array_from_list(self, reclist, column_names, mysql_types, replace_nulls_with, lowercase=0):
        """
        Convert a list of DB records (returned by GetResultsFromQuery)
        into a record array defined in numpy.
        Field names are given by the first item in the list.
        If lowercase > 0 the record names are converted to lower case.
        """
        def replace_None_with_value(element, value, type):
            if element == None:
                if type.startswith('a') and (not isinstance(value, str)):
                    value = ''
                return value
            else:
                return element

        def replace_None_with_value_for_row(row, value, types):
            return map(lambda element, type: replace_None_with_value(element, value, type),
                       row, types)

        if lowercase > 0:
            column_names = map(lambda element: element.lower(),column_names)
        types = map(lambda mysql_type: self._numpy_type_for_mysql_type(mysql_type), mysql_types)
        for i in range(len(types)):
            if types[i].startswith('a'):
                rec_length = [len(rec[i]) for rec in reclist if rec[i] is not None]
                if rec_length:
                    max_len = max(rec_length)
                else:
                    max_len = 1
                types[i] = 'a' + str(max_len)
        formats = ','.join(types)
        recarray = rec.array( map( lambda sublist:
                                       replace_None_with_value_for_row(sublist, replace_nulls_with, types),
                                       reclist),
                                  names=column_names,
                                  formats=formats)
        return recarray

    def _column_names_and_types(self, column_names, mysql_types, lowercase=0):
        """
        Return a dictionary mapping column names to their types.
        If lowercase > 0 the record names are converted to lower case.
        """
        if lowercase > 0:
            column_names = map(lambda element: element.lower(),column_names)
        types = map(lambda mysql_type: self._numpy_type_for_mysql_type(mysql_type), mysql_types)
        column_name_types = {}
        for i in range(len(column_names)):
            column_name_types[column_names[i]] = types[i]
        return column_name_types

########## Logging utility functions from Bjorn's old globals.py #####################
def _log(s) :
    sys.stdout.write(s)
    sys.stdout.write("\n")
    sys.stdout.flush()

def _log_sql(sql_query, show_output=False):
    if show_output == True:
        _log("SQL: " + sql_query)



from opus_core.tests import opus_unittest

import os

from opus_core.logger import logger


class OpusDatabaseTest(opus_unittest.OpusTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_returns_dictionary_of_attribute_names_and_numpy_data_on__make_dictionary(self):
        from MySQLdb.constants import FIELD_TYPE

        db = OpusDatabase.__new__(OpusDatabase) # HACK around needing an actual connection

        resultlist = [[1,'a'],[2,'b'], [3,'c']]
        column_names = ['id', 'attr1']
        mysql_types = [FIELD_TYPE.TINY, FIELD_TYPE.STRING]

        expected_result = {
            'id':array([1,2,3], dtype='i1'),
            'attr1':array(['a','b','c']),
            }
        actual_result = db._make_dictionary(resultlist, column_names, mysql_types)

        self.assertDictsEqual(actual_result, expected_result)

        resultlist = [[4,6L],[5,7L]]
        column_names = ['id2', 'attr2']
        mysql_types = [FIELD_TYPE.LONG, FIELD_TYPE.LONGLONG]

        expected_result = {
            'id2':array([4,5]),
            'attr2':array([6L,7L]),
            }
        actual_result = db._make_dictionary(resultlist, column_names, mysql_types)

        self.assertDictsEqual(actual_result, expected_result)



if __name__ == '__main__':
    opus_unittest.main()