# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration

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
            tables_to_copy = sum(table_mapping.values(), [])  # flat a list of lists
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
        
    parser.add_option("--database_configuration", dest="database_configuration", default = "scenario_database_server",
                      action="store", help="Name of the database server configuration in database_server_configurations.xml where the scenario database is located. Defaults to 'scenario_database_server'.") 
    
    parser.add_option("-f", "--from_database", dest="from_database_name", 
        type="string", help="The database to flatten. (REQUIRED)")
    parser.add_option("-t", "--to_database", dest="to_database_name", 
        type="string", help="The new database to create. (REQUIRED)")
            
    (options, args) = parser.parse_args()
    
    from_database_configuration = ScenarioDatabaseConfiguration(
        database_name = options.from_database_name,
        database_configuration = options.database_configuration
    )
    to_database_configuration = ScenarioDatabaseConfiguration(
        database_name = options.to_database_name,
        database_configuration = options.database_configuration
    )    

    copier = FlattenScenarioDatabaseChain()
    copier.copy_scenario_database(from_database_configuration = from_database_configuration, 
                                  to_database_configuration = to_database_configuration)
