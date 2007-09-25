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

import copy

from opus_core.store.old.storage import Storage

class mysql_storage(Storage):
    Query = {}
    Query["all_fields_from_one_table"] = "select * from $$."
    Query["selected_fields_from_one_table"] = ["select ", ", ", " from $$."]
    Query["selected_fields_from_one_table_by_time"] = ["select ", ", ", " from $$.", "where year="]
    Query["all_fields_from_one_table_order_by"] = ["select * from $$.", " order by "]
    Query["selected_fields_from_one_table_order_by"] = ["select ", ", ", " from $$.", " order by "]
    Query["show_fields_from_table"] = "show fields from $$."
    Query["selected_fields_from_one_table_by_time_order_by"] = ["select ", ", ", " from $$.", " where year=", " order by "]

    def __init__(self, storage_location, write_chunk_size=1000):
        self.database_connection = storage_location

        ### Connection reconstruction information
        self._hostname = self.database_connection.hostname
        self._username = self.database_connection.username
        self._password = self.database_connection.password
        self._db = self.database_connection.database_name

        self.write_chunk_size = write_chunk_size

    def write_dataset(self, write_resources):
        if 'values' not in write_resources:
            return

        write_resources.check_obligatory_keys(['out_table_name'])

        drop_table_flag = write_resources.get('drop_table_flag', False)
        out_table_name = write_resources['out_table_name']
        valuetypes = write_resources.get('valuetypes', {})
        id_name = write_resources.get('id_name', None)
        values = write_resources['values']

        return self._write_dataset(out_table_name=out_table_name, values=values,
            valuetypes=valuetypes, drop_table=drop_table_flag, id_name=id_name)

    def _write_dataset(self, out_table_name, values, valuetypes={},
            drop_table=False, id_name=None):
        """
        Entry 'out_table_name' specifies the table name.
        'values' is a dictionary where keys are the attribute names and values
            are value arrays of the corresponding attributes.
        'valuetypes' is a dictionary where keys are the attribute names and
            values are character strings determining (in mysql syntax) the types
            of the corresponding attributes ('integer', 'double', 'text', ...).
        'drop_table' (True or False) determines if content of the table (in
            case it exists) should be deleted or not. If the entry is missing,
            the existing table is not deleted.
        """
        columnnames_type_pairlist = []
        for attr in values.keys():
            if valuetypes.has_key(attr.upper()):
                type = valuetypes[attr.upper()]
            elif valuetypes.has_key(attr.lower()):
                type = valuetypes[attr.lower()]
            else:
                if values[attr].dtype.char == 'S':
                    type = 'TEXT'
                else:
                    type = self.get_database_connection().get_mysql_type_from_numpy(values[attr].dtype.char)

            columnnames_type_pairlist.append((attr, type))

        if drop_table:
            self.get_database_connection().drop_table(out_table_name)

        self.get_database_connection().CreateTable(out_table_name, columnnames_type_pairlist, id_name)

        total_rows = values[values.keys()[0]].size

        chunks = (total_rows / self.write_chunk_size) + 1
        total_row_count = 0
        for chunk in range(chunks):
            chunk_row_count = 0
            inputlist = [values.keys()]
            while chunk_row_count < self.write_chunk_size and total_row_count < total_rows:
                sublist = []
                for attr in values.keys():
                    sublist.append(values[attr][total_row_count])
                inputlist.append(sublist)
                chunk_row_count = chunk_row_count + 1
                total_row_count = total_row_count + 1
            self.get_database_connection().DoMultiInsertsFromResultListInto(out_table_name, inputlist)

    def make_query(self, type, arglist):
        if type == "all_fields_from_one_table":
            return self.Query[type] +  arglist
        if type == "all_fields_from_one_table_order_by":
            return self.Query[type][0] + " " + arglist[0]  + self.Query[type][1] + self.Query[type][2] + arglist[1]
        elif type == "selected_fields_from_one_table":
            query = self.Query[type][0] +  arglist[0] [0]
            if len(arglist[0]) > 1:
                for arg in arglist[0][1:len(arglist[0])]:
                    query = query  + self.Query[type][1] + arg
            query = query + self.Query[type][2] + arglist[1]
        elif type == "selected_fields_from_one_table_by_year":
            query = self.Query[type][0] +  arglist[0][0]
            if len(arglist[0]) > 1:
                for arg in arglist[0][1:len(arglist[0])]:
                    query = query  + self.Query[type][1] + arg
            query = query + self.Query[type][2] + arglist[1] + self.Query[type][3] + arglist[2]
        elif type == "selected_fields_from_one_table_order_by":
            query = self.Query[type][0]  + arglist[0][0]
            if len(arglist[0]) > 1:
                for arg in arglist[0][1:len(arglist[0])]:
                    query = query + self.Query[type][1] + arg
            query = query + self.Query[type][2]  + arglist[1] + self.Query[type][3] + arglist[2][0]
            if len(arglist[2]) > 1: #multiple keys
                for arg in arglist[2][1:len(arglist[2])]:
                    query = query + self.Query[type][1] + arg
        elif type == "selected_fields_from_one_table_by_time_order_by":
            query = self.Query[type][0]  + arglist[0][0]
            if len(arglist[0]) > 1:
                for arg in arglist[0][1:len(arglist[0])]:
                    query = query + self.Query[type][1] + arg
            query = query + self.Query[type][2]  + arglist[1] + self.Query[type][3] + arglist[2] + \
                  self.Query[type][4] + arglist[3][0]
            if len(arglist[3]) > 1: #multiple keys
                for arg in arglist[3][1:len(arglist[3])]:
                    query = query + self.Query[type][1] + arg
        elif type == "show_fields_from_table":
            return self.Query[type] + arglist
        else:
            raise StandardError, "Uknown query!"
        return query

    def has_table(self, table):
        return self.get_database_connection().has_table(table)

    def get_database_connection(self):
        try:
            self.database_connection

        except: # Support for pickling/unpickling
            raise

        return self.database_connection


    def __getstate__(self): # Support for pickling/unpickling
        state = copy.copy(self.__dict__)

        try: del state['database_connection'] # Can't pickle this guy.
        except KeyError: pass

        return state


from opus_core.tests import opus_unittest

import os

from opus_core.misc import get_host_name
from opus_core.logger import logger
from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.tests.utils.database_server_configuration_for_tests import DatabaseServerConfigurationForTests
from opus_core.misc import does_test_database_server_exist


if does_test_database_server_exist(module_name=__name__):
    class TestMysqlStorage(opus_unittest.OpusTestCase):
        def setUp(self):
            # for the Macintosh, the hostname may have embedded '-' characters, which will upset MySQL 
            # when used as part of a database name
            h = get_host_name().replace('-', '_')
            self.database_name = 'test_mysql_storage_%s' % h
            try:
                self.db_server = self.get_database_server_for_host('localhost')
            except:
                try:
                    self.db_server = self.get_database_server_for_host(os.environ['MYSQLHOSTNAME'])
                except:
                    self.db_server = None
                    return
            self.db_server.drop_database(self.database_name)
            self.db_server.create_database(self.database_name)

        def get_database_server_for_host(self, hostname):
            """
            Return a database server to this host, using the environment variable's for
            username and password.
            """
            return MysqlDatabaseServer(DatabaseServerConfigurationForTests())

        def tearDown(self):
            if (self.db_server is not None) and self.db_server.has_database(self.database_name):
                self.db_server.drop_database(self.database_name)

        def test_expressions_may_have_square_brackets(self):
            if self.db_server is None:
                logger.log_status('Skipping test_expressions_may_have_square_brackets, since there is no available MySQL database server.')
                return

            db_con = self.db_server.get_database(self.database_name)

            table_name = 'exprs'
            db_con.create_table(table_name=table_name, table_schema = {'a':'INT','expr':'TEXT',})
            db_con.DoQuery('insert into %s (a,expr) values (10,"a[b]")' % table_name)

            result = db_con.GetResultsFromQuery('select a,expr from %s' % table_name)
            self.assertEqual(result[1][0], 10)
            self.assertEqual(result[1][1], 'a[b]')
            db_con.drop_table(table_name)

            db_con.create_table(table_name=table_name, table_schema = {'a':'INT','expr':'TEXT',})
            inputs = [['a','expr'],[10,'a[b]'],[20,'hello']]
            db_con.DoMultiInsertsFromResultListInto(table_name, inputs)

            result = db_con.GetResultsFromQuery('select a,expr from %s' % table_name)
            self.assertEqual(result[1][0], 10)
            self.assertEqual(result[1][1], 'a[b]')
            self.assertEqual(result[2][0], 20)
            self.assertEqual(result[2][1], 'hello')

            db_con.close()

if __name__ == '__main__':
    opus_unittest.main()