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

from opus_core.store.opus_database import OpusDatabase
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration

from urbansim.store.database_tools import DatabaseTools
from opus_core.logger import logger

class FlattenScenarioDatabaseChain(object):
    def _create_db_from_chain_via_sql(self, 
                                      to_host_name,
                                      to_database_name, 
                                      to_user_name, 
                                      to_password, 
                                      table_mapping, 
                                      tables_to_copy=[]
                                     ):
        """Use SQL commands to copy an UrbanSim style database chain from
        from one MySQL to a new databsae on the same MySQL.  This method
        does the copy via SQL - it does not bring the data into Python.
        
        Given a dictionary that maps tables to their database location 
        will create a database that contains all the tables in this dictionary. 
        Example use would be to aggregate all tables in an UrbanSim database-chain (Scenario Database $$) 
        into one database"""
        db_server_config = DatabaseServerConfiguration(host_name=to_host_name,
                                                       user_name=to_user_name,
                                                       password=to_password
                                                   )
        db_server = MysqlDatabaseServer(db_server_config)
        db_server.drop_database(to_database_name)
        db_server.create_database(to_database_name)
        new_database = db_server.get_database(to_database_name)

        for table_name, table_database_name in table_mapping.iteritems():
            if table_name not in tables_to_copy:
                continue
            logger.start_block("Copying table '%s' from database '%s' to '%s'" 
                               % (table_name, table_database_name, to_database_name))
            try:
                sql = "create table %(new_database_name)s.%(table_name)s select * from %(old_database_name)s.%(table_name)s" % {
                    'table_name':table_name,
                    'old_database_name':table_database_name,
                    'new_database_name':to_database_name,
                    }
                new_database.DoQuery(sql)
                if table_name == 'scenario_information':
                    self._fix_scenario_information_table(table_database_name, new_database, to_database_name)
            finally:
                logger.end_block()
        
    def _fix_scenario_information_table(self, from_database_name, new_database, to_database_name):
        """Ensure that the scenario_information table doesn't point to any
        more databases.
        """
        new_database.DoQuery("update %s.scenario_information set parent_database_url=''" % to_database_name)
            
    def _create_db_from_chain_via_python(self, 
                                        from_host_name, 
                                        from_database_name,
                                        from_user_name,
                                        from_password,
                                        to_host_name,
                                        to_database_name, 
                                        to_user_name,
                                        to_password, 
                                        table_mapping, 
                                        tables_to_copy=[]
                                        ):
        """Use Python to copy a UrbanSim sytle database chain from 
        one MySQL server to another MySQL server.  This method does the copy
        by reading the data to memory.
        
        Given a dictionary that maps tables to their database location 
        will create a database that contains all the tables in this dictionary. 
        Example use would be to aggregate all tables in an UrbanSim database-chain (Scenario Database $$) 
        into one database"""
        db_server_config = DatabaseServerConfiguration(host_name=to_host_name,
                                                       user_name=to_user_name,
                                                       password=to_password
                                                   )
        db_server = MysqlDatabaseServer(db_server_config)
        db_server.drop_database(to_database_name)

        # TODO: move DatabaseTools functionality into OpusDatabase.
        db_tool = DatabaseTools()
        new_database = db_tool.create_db(name=to_database_name,
                                         hostname=to_host_name,
                                         username=to_user_name,
                                         password=to_password)
        
        for table_name, table_database_name in table_mapping.iteritems():
            if table_name not in tables_to_copy:
                continue
            logger.start_block("Copying table '%s' from database '%s'" 
                               % (table_name, table_database_name))
            try:
                from_database = OpusDatabase(hostname=from_host_name, 
                                             username=from_user_name, 
                                             password=from_password, 
                                             database_name=table_database_name)
                #GetResultsFromQuery returns a list, where first element is a list of field names, 
                #and other elements are the values
                table = from_database.GetResultsFromQuery("SELECT * FROM %s.%s;" % (table_database_name, table_name))
                
                table_schema = from_database.get_schema_from_table(table_name)
                new_database.create_table(table_name, table_schema)
                
                field_names = table[0]
                field_values = table[1:]
                names_values_dict = []
                #iterate through the rows of the original table
                for v in field_values:
                    row_dict = {}
                    #create a dictionary that represents one row of data in this table
                    #(mapping of field names to values)
                    for (name, value) in zip(field_names, v):
                        #add extra quotes around values that are strings
                        if isinstance(value, str):
                            value = "'%s'" % value
                        row_dict[name] = value
    
                    names_values_dict.append(({}, row_dict))
                #copy original table's rows to new table
                db_tool.populate_table('%s.%s' % (to_database_name, table_name), 
                                       field_names, 
                                       names_values_dict)
                
                from_database.close()
                if table_name == 'scenario_information':
                    self._fix_scenario_information_table(table_database_name, new_database, to_database_name)
            finally:
                logger.end_block()
            
        new_database.close()

    def copy_scenario_database(self, config):
        """If mode is 'sql' do the copy via SQL statements.
        If mode is 'python' do the copy by reading data into Python.
        """
        logger.start_block("Copying tables from database chain starting at '%s' on '%s'\nto database '%s' on '%s'"
                           % (config['to_database_name'], 
                              config['from_host_name'], 
                              config['to_database_name'], 
                              config['to_host_name']))
        try:
            scenario_db = ScenarioDatabase(hostname=config['from_host_name'], 
                                           username=config['from_user_name'], 
                                           password=config['from_password'],
                                           database_name=config['from_database_name'])
            table_mapping = scenario_db.get_table_mapping()
            scenario_db.close()
            if config['mode'] == 'python':
                self._create_db_from_chain_via_python(to_host_name=config['to_host_name'],
                                                     to_database_name=config['to_database_name'],
                                                     to_user_name=config['to_user_name'],
                                                     to_password=config['to_password'],
                                                     from_host_name=config['from_host_name'],
                                                     from_database_name=config['from_database_name'],
                                                     from_user_name=config['from_user_name'],
                                                     from_password=config['from_password'],
                                                     table_mapping=table_mapping,
                                                     tables_to_copy=config['tables_to_copy'])
            elif config['mode'] == 'sql':
                self._create_db_from_chain_via_sql(to_host_name=config['to_host_name'],
                                                  to_database_name=config['to_database_name'],
                                                  to_user_name=config['to_user_name'],
                                                  to_password=config['to_password'],
                                                  table_mapping=table_mapping,
                                                  tables_to_copy=config['tables_to_copy'])
            else:
                raise StandardError("Mode most be one of 'sql' or 'python'")
        finally:
            logger.end_block()
