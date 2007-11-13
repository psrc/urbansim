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

import re
from opus_core.logger import logger

from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer
from sqlalchemy import select

class ScenarioDatabaseManager(object):
    """Extract a flattened scenario database to the cache.
    """
    def __init__(self, server_configuration, base_scenario_database_name):
        self.database_server = DatabaseServer(server_configuration)
        self.base_scenario_database_name = base_scenario_database_name
        
    def get_database_to_table_mapping(self):
        table_mapping = self._get_table_mapping(
            scenario_database_name = self.base_scenario_database_name,
            table_mapping = {})
        
        database_to_table_mapping = {}
        for table_name, database_name in table_mapping.items():
            if database_name not in database_to_table_mapping:
                database_to_table_mapping[database_name] = [table_name]
            else:
                database_to_table_mapping[database_name].append(table_name)
                
        return database_to_table_mapping        

    def _get_table_mapping(self, scenario_database_name, table_mapping):
        database = self.database_server.get_database(scenario_database_name)
        
        tables_in_database = database.get_tables_in_database()
        relevant_tables = [table_name for table_name in tables_in_database 
                                if table_name not in table_mapping]
        
        for table_name in relevant_tables:
            table_mapping[table_name] = scenario_database_name 
            logger.log_status('Found: ' + scenario_database_name + "." + table_name,
                              tags=['database'], verbosity_level=3)
        
        #TODO: there's no reason to have the parent database url store JDBC
        #      It should just be a database name
        if 'scenario_information' in tables_in_database:
            scenario_info_table = database.get_table('scenario_information')
            if 'PARENT_DATABASE_URL' in scenario_info_table.c:
                col = scenario_info_table.c.PARENT_DATABASE_URL
            elif 'parent_database_url' in scenario_info_table.c:
                col = scenario_info_table.c.parent_database_url
            else:
                raise 'Scenario information table contains no parent_database_url column'
            
            query = select(columns = [col])
            next_database_name = database.engine.execute(query).fetchone()
            if next_database_name == () or next_database_name[0] == '':
                next_database_name = None
            else:
                next_database_name = next_database_name[0]
            
            database.close()
            if next_database_name is not None:                
                match = re.search("jdbc:mysql://[^/]*/(.*)", next_database_name)
                if match == None :
                    raise ValueError("parent database url is not a MySQL JDBC url" )
                next_database_name = match.group(1)
                table_mapping = self._get_table_mapping(next_database_name, table_mapping)
        else:
            database.close()
            
        return table_mapping