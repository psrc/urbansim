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

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.cross_database_operations import CrossDatabaseOperations
from opus_core.database_management.scenario_database_manager import ScenarioDatabaseManager
 
    
from opus_core.logger import logger

class FlattenScenarioDatabaseChain(object):

    def _fix_scenario_information_table(self, new_database):
        """Ensure that the scenario_information table doesn't point to any
        more databases.
        """
        new_database.metadata.reflect()
        scenario_information_table = new_database.get_table('scenario_information')
        qry = scenario_information_table.update(values = {'parent_database_url':''})
        new_database.engine.execute(qry)
            
    def _create_db_from_chain_via_python(self, 
                                         db_server_config_from,
                                         from_database_name,
                                         db_server_config_to,
                                         to_database_name, 
                                         tables_to_copy=[]
                                        ):
        """Copy a UrbanSim sytle database chain from 
        one MySQL server to another MySQL server."""

                
        db_server_from = DatabaseServer(db_server_config_from)
        db_server_to = DatabaseServer(db_server_config_to)
        db_server_to.drop_database(to_database_name)
        db_server_to.create_database(to_database_name)
        
        database_out = db_server_to.get_database(to_database_name)
        
        scenario_db_manager = ScenarioDatabaseManager(
            server_configuration = db_server_config_from, 
            base_scenario_database_name = from_database_name)
        table_mapping = scenario_db_manager.get_database_to_table_mapping()
    
        cross_db_operations = CrossDatabaseOperations()
        
        #by default, copy all tables
        if tables_to_copy == []:
            tables_to_copy = table_mapping.values()
            
        for database_name, tables in table_mapping.items():
            database_in = db_server_from.get_database(database_name)
            for table in tables:
                if table not in tables_to_copy and tables_to_copy != []:
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

    def copy_scenario_database(self, config):
        db_server_config_to = config['db_server_config_to']                                                   
        db_server_config_from = config['db_server_config_from'] 
        
        logger.start_block("Copying tables from database chain starting at '%s' on '%s'\nto database '%s' on '%s'"
                           % (config['to_database_name'], 
                              db_server_config_from.host_name, 
                              config['to_database_name'], 
                             db_server_config_to.host_name))
        
        try:
            self._create_db_from_chain_via_python(
                 db_server_config_to = db_server_config_to,
                 to_database_name=config['to_database_name'],
                 db_server_config_from = db_server_config_from,
                 from_database_name=config['from_database_name'],
                 tables_to_copy=config.get('tables_to_copy', []))
        finally:
            logger.end_block()
