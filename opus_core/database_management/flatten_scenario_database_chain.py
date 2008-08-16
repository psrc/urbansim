#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

from opus_core.database_management.cross_database_operations import CrossDatabaseOperations
from opus_core.database_management.scenario_database_manager import ScenarioDatabaseManager
 
    
from opus_core.logger import logger

class FlattenScenarioDatabaseChain(object):

    def _fix_scenario_information_table(self, new_database):
        """Ensure that the scenario_information table doesn't point to any
        more databases.
        """
        if new_database.table_exists('scenario_information'):
            qry = None
            scenario_information_table = new_database.get_table('scenario_information')
            if 'PARENT_DATABASE_URL' in scenario_information_table.c:
                qry = scenario_information_table.update(values = {'PARENT_DATABASE_URL':''})
            elif 'parent_database_url' in scenario_information_table.c:
                qry = scenario_information_table.update(values = {'parent_database_url':''})
            if qry is not None: 
                new_database.execute(qry)
            
    def _create_db_from_chain_via_python(self, 
                                         from_database_configuration, 
                                         to_database_configuration,
                                         tables_to_copy):
                
        db_server_from = DatabaseServer(from_database_configuration)
        db_server_to = DatabaseServer(to_database_configuration)
        db_server_to.drop_database(to_database_configuration.database_name)
        db_server_to.create_database(to_database_configuration.database_name)
        
        database_out = db_server_to.get_database(to_database_configuration.database_name)
        
        scenario_db_manager = ScenarioDatabaseManager(
            server_configuration = from_database_configuration, 
            base_scenario_database_name = from_database_configuration.database_name)
        table_mapping = scenario_db_manager.get_database_to_table_mapping()
    
        cross_db_operations = CrossDatabaseOperations()
        
        #by default, copy all tables
        if tables_to_copy == []:
            tables_to_copy = table_mapping.values()
        elif 'scenario_information' not in tables_to_copy:
            tables_to_copy.append('scenario_information')
            
        for database_name, tables in table_mapping.items():
            database_in = db_server_from.get_database(database_name)
            for table in tables:
                if table not in tables_to_copy:
                    continue
                
                logger.start_block("Copying table '%s' from database '%s'" 
                                   % (table, database_name)) 
                
                try:               
                    cross_db_operations.copy_table(table_to_copy = table, 
                                                   database_in = database_in, 
                                                   database_out = database_out, 
                                                   use_chunking = True)
                finally:
                    logger.end_block()        
            database_in.close()
            
        self._fix_scenario_information_table(database_out)            
        database_out.close()
        db_server_from.close()
        db_server_to.close()

    def copy_scenario_database(self, 
                               from_database_configuration, 
                               to_database_configuration,
                               tables_to_copy = []):
        
        logger.start_block("Copying tables from database chain starting at '%s' on '%s'\nto database '%s' on '%s'"
                           % (from_database_configuration.database_name, 
                              from_database_configuration.host_name, 
                              to_database_configuration.database_name, 
                             to_database_configuration.host_name))
        
        try:
            self._create_db_from_chain_via_python(
                 from_database_configuration = from_database_configuration, 
                 to_database_configuration = to_database_configuration,
                 tables_to_copy = tables_to_copy)
        finally:
            logger.end_block()

from optparse import OptionParser

if __name__ == '__main__':
    """
    Flattens the full scenario database chain.
    """
        
    parser = OptionParser()
        
    parser.add_option("-o", "--host", dest="host_name", type="string",
        help="The database host (default: from environment"
            " variable, then nothing).")
    parser.add_option("-u", "--username", dest="user_name", type="string",
        help="The database connection password (default: from environment"
            " variable, then nothing).")
    parser.add_option("-p", "--password", dest="password", type="string",
        help="The database connection password (default: from environment"
            " variable, then nothing).")
    parser.add_option("-f", "--from_database", dest="from_database_name", 
        type="string", help="The database to flatten. (REQUIRED)")
    parser.add_option("-t", "--to_database", dest="to_database_name", 
        type="string", help="The new database to create. (REQUIRED)")
            
    (options, args) = parser.parse_args()
    
    from_database_configuration = ScenarioDatabaseConfiguration(
        host_name = options.host_name,
        user_name = options.user_name,
        password = options.password,
        database_name = options.from_database_name
    )
    to_database_configuration = ScenarioDatabaseConfiguration(
        host_name = options.host_name,
        user_name = options.user_name,
        password = options.password,
        database_name = options.to_database_name
    )    

    copier = FlattenScenarioDatabaseChain()
    copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                                  to_database_configuration = to_database_configuration)
