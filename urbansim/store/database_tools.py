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

import os 

from opus_core.store.opus_database import OpusDatabase
from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration


class DB_defaults(object):
    db='database_tools_temp_db'
    host_name=os.environ.get('MYSQLHOSTNAMEFORTESTS', 'localhost')
    user_name=os.environ['MYSQLUSERNAME']
    password =os.environ['MYSQLPASSWORD']

class DatabaseTools(object):
    """Provides utility functions for creating and manipulating MySQL databases. 
    Intended for creating "small" tables with just enough data to input to a unit test.
    """
    def create_db(self, 
                  name=DB_defaults.db, 
                  hostname=DB_defaults.host_name, 
                  username=DB_defaults.user_name, 
                  password=DB_defaults.password):
        """ Create test database connection with the given parameters. 
        If no arguments are given, then the defaults (in DB_defaults above) 
        will be used. Returns the connection.
        """
        db_server_config = DatabaseServerConfiguration(
            host_name = hostname,
            user_name = username,
            password = password,
            )
        db_server = MysqlDatabaseServer(db_server_config)
        db_server.create_database(name)
        self.database = db_server.get_database(name)
        return self.database
    
    def create_table(self,table_name, table_fields):
        """Create a table called table_name in the set database with the given 
        field names and types, found as a corresponding field_name:field_type 
        pair in the table_fields dictionary
        """
        
        names_of_fields_list = []
        for key, value in table_fields.iteritems():
            names_of_fields_list.append(key + " " + value)
        names_of_fields = ",".join(names_of_fields_list)
        self.database.DoQuery("CREATE TABLE IF NOT EXISTS %s (%s);" % (table_name, 
                                                                       names_of_fields))

    def create_sql_for_populate_table(self, table_name, table_fields, data, unique_field=None):
        if len(data) == 0:
            return
        next_id = 1
        values_of_fields_list = []
        
        for number_dict, field_names_and_values_dict in data:
            keylist = field_names_and_values_dict.keys()
            
            if number_dict:
                number_of = number_dict["number_of"]
            
            if unique_field:
                names_of_fields = ",".join(keylist) + "," + unique_field
            else:
                names_of_fields = ",".join(keylist)
            
            def field_value(self, key):
                value = field_names_and_values_dict[key]
                if value == None:
                    return 'null'
                else:
                    return str(value)
            values_of_fields = ",".join( map(lambda key: field_value(self, key), keylist))
            
            if number_dict:
                if unique_field:
                    for unique_id in range(next_id, next_id + number_of):
                        values_of_fields_list.append("(" + values_of_fields + "," + 
                                                     str(unique_id) + ")")
                    next_id = next_id + number_of
                else: 
                    for tally in range(0, number_of):
                        values_of_fields_list.append("(" + values_of_fields + ")")
            else:
                values_of_fields_list.append("(" + values_of_fields + ")")

        sql_insert = """INSERT INTO %s (%s) VALUES %s;""" \
                     % (table_name, names_of_fields, ",".join(values_of_fields_list))
        return sql_insert
    
    def populate_table(self,table_name, table_fields, data, unique_field=None):    
        """Populate a given table by "generating" the rows.
        table_name: name of the table to populate with data
        table_fields: a dictionary where the keys are the table's field names,
                      and values are the type of that field (in mysql)
        data: a list of 2-tuples, where the first element of the tuple is either 
              an empty dictionary, or a dictionary containing a "number_of" key 
              and corresponding value. 
              i.e. [ ({"number_of":4000}, {"grid_id":1, "sector_id":1}),
                     ({}, {"grid_id":1, "sector_id":2}) ]
              the corresponding value to "number_of" indicates how many of that 
              item to create. in this case, the first row asks populate_table to create
              4000 "jobs" in the given table_name, with field values grid_id=1 and sector_id=1
              
              if the first element of this tuple is an empty dictionary, like in the second 
              row of the above example, this indicates to create only one "item" (i.e. a rate)
              and insert that into the table. 
              
              the second element of the tuple is a dictionary where keys are field 
              names and corresponding values are actual values to insert into the table. 
        unique_field: optional argument. a string that specifies a field that needs 
                      to be unique per item. for example, when generating the jobs 
                      table, each job needs to have a unique job_id, so the argument 
                      would be unique_field="job_id"              
        """
        if len(data) == 0:
            return
        sql_insert = self.create_sql_for_populate_table(table_name, table_fields, data, unique_field)
        self.database.DoQuery(sql_insert)

    def add_row_from_dictionary(self, table_name, row_fields_and_values):
        """Argument is a dictionary that represents new row, with keys representing 
        field names, and values representing the values for the input configuration"""
        keys = row_fields_and_values.keys()
        values = [];
        for key in keys:
            if type(row_fields_and_values[key]) == str:
                values.append("'%s'" % row_fields_and_values[key])
            else:
                values.append(str(row_fields_and_values[key]))
        
        sql_insert = """INSERT INTO %s (%s) VALUES (%s);""" % (table_name, ",".join(keys), ",".join(values))
        self.database.DoQuery(sql_insert)

    def create_dictionary_from_sql_query(self, sql):
        """Returns a dictionary that represents a sql row, where keys are sql fields,
        and values are sql values"""        
        results = self.database.GetResultsFromQuery(sql)
        if len(results) == 1:
            return None
        else:
            return dict(zip(results[0],results[1]))

    def conditional_select_a_field(self, field_name, table_name, selector, selector_value):
        sql_select = """SELECT %s FROM %s WHERE %s = %s""" % (field_name, table_name, selector, selector_value)
        sql_results = self.database.GetResultsFromQuery(sql_select)
        return sql_results[1][0]

    def delete_table(self,table_name):
        """Deletes this table from the database
        """
        self.database.drop_table(table_name)
        
    def delete_db(self, name=DB_defaults.db, hostname=DB_defaults.host_name, 
                        username=DB_defaults.user_name, password=DB_defaults.password):
        """ Delete database with the given parameters. If no arguments are given, 
        then the defaults (in DB_defaults above) will be used. 
        """
        database = OpusDatabase(hostname=hostname, 
                                username=username, 
                                password=password, 
                                database_name='mysql', 
                                show_output=False)        
        database.drop_database(database=name)
        database.close()
    
    def clear_table(self,table_name):
        """ Deletes the contents of a table without removing the table from the database. """
        self.database.DoQuery("truncate  %s"% table_name)
            
    def disconnect(self):
        if self.database:
            self.database.close()
    

from opus_core.tests import opus_unittest
from opus_core.misc import does_test_database_server_exist

from urbansim.store.database_tools import DatabaseTools


if does_test_database_server_exist(module_name=__name__):
    class Tests(opus_unittest.OpusTestCase):
        def setUp(self):
            self.test_toolbox = DatabaseTools()
            self.test_toolbox.delete_db()
            self.database = self.test_toolbox.create_db()
        
        def test_db_connection(self):
            sql = "CREATE TABLE foo (id int, value int);"
            self.database.DoQuery(sql)
            
            results = self.database.GetResultsFromQuery("select count(*) from foo;")
            self.assertEqual(0, results[1][0])
    
        def test_create_and_populate_table(self):
            jobs_table_schema = {"job_id":"int", "grid_id":"int", "sector_id":"int"}
            jobs_data = [ ({"number_of":4000}, {"grid_id":1, "sector_id":1}),
                          ({"number_of":1000}, {"grid_id":1, "sector_id":2}) ]
            self.test_toolbox.create_table("jobs", jobs_table_schema)
            self.test_toolbox.populate_table("jobs", jobs_table_schema, jobs_data, "job_id")
            
            results = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs;")
            self.assertEqual(5000, results[1][0])
            results = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs WHERE sector_id=1;")
            self.assertEqual(4000, results[1][0])
            results = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs WHERE sector_id=2;")
            self.assertEqual(1000, results[1][0])
            
            jobs_data = [ ({}, {"job_id":5, "grid_id":5, "sector_id":5}) ] 
            self.test_toolbox.populate_table("jobs", jobs_table_schema, jobs_data)            
            
            results = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs;")
            self.assertEqual(5001, results[1][0])
            results = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs WHERE sector_id=5;")
            self.assertEqual(1, results[1][0])
            
        def test_clear_table(self):
            jobs_table_schema = {"job_id":"int", "grid_id":"int", "sector_id":"int"}
            jobs_data = [ ({"number_of":4000}, {"grid_id":1, "sector_id":1}),
                          ({"number_of":1000}, {"grid_id":1, "sector_id":2}) ]
            self.test_toolbox.create_table("jobs", jobs_table_schema)
            self.test_toolbox.populate_table("jobs", jobs_table_schema, jobs_data, "job_id")
            
            self.test_toolbox.clear_table("jobs")
            count = self.database.GetResultsFromQuery("SELECT COUNT(*) FROM jobs;")[1][0]
            self.assertEqual(count, 0)
            
        def tearDown(self):
            self.test_toolbox.delete_db()
    
    
if __name__=='__main__':
    opus_unittest.main()
