# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from opus_core.logger import logger

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
        
        if 'scenario_information' in tables_in_database:
            scenario_info_table = database.get_table('scenario_information')
            if 'PARENT_DATABASE_URL' in scenario_info_table.c:
                col = scenario_info_table.c.PARENT_DATABASE_URL
            elif 'parent_database_url' in scenario_info_table.c:
                col = scenario_info_table.c.parent_database_url
            else:
                raise 'Scenario information table contains no parent_database_url column'
            
            query = select(columns = [col])
            next_database_name = database.execute(query).fetchone()
            if next_database_name == () or next_database_name[0] == '':
                next_database_name = None
            else:
                next_database_name = next_database_name[0]
            
            if next_database_name is not None:  
                #old method stored chain as a jdbc url; if this is the case, this code will update it              
                match = re.search("jdbc:mysql://[^/]*/(.*)", next_database_name)
                if match is not None:
                    next_database_name = match.group(1)          
                    if 'PARENT_DATABASE_URL' in scenario_info_table.c:
                        u = scenario_info_table.update(values = {'PARENT_DATABASE_URL':next_database_name})
                    else:
                        u = scenario_info_table.update(values = {'parent_database_url':next_database_name})
                    database.execute(u)
                database.close()
                table_mapping = self._get_table_mapping(next_database_name, table_mapping)
            else: database.close()
        else:
            database.close()
            
        return table_mapping
    
from opus_core.tests import opus_unittest
from opus_core.database_management.test_classes.database_management_test_interface \
    import DatabaseManagementTestInterface 


class ScenarioDatabaseManagerTest(DatabaseManagementTestInterface):

    def test_table_mapping_no_chain(self):
        sdm = ScenarioDatabaseManager(self.config, 'db_chain_granddad')
        t_mapping = sdm._get_table_mapping('db_chain_granddad', {})
        
        expected = {
            'base_schema': 'db_chain_granddad',
            'base_schema2': 'db_chain_granddad',
            'scenario_information': 'db_chain_granddad'
        }
        
        self.assertEqual(t_mapping, expected)
    
    def test_table_mapping_chain(self):
        sdm = ScenarioDatabaseManager(self.config, 'db_chain_son')
        t_mapping = sdm._get_table_mapping('db_chain_son', {})
        
        expected = {
            'base_schema': 'db_chain_dad',
            'base_schema2': 'db_chain_son',
            'scenario_information': 'db_chain_son'
        }
        
        self.assertEqual(t_mapping, expected)
                
    def test_database_to_table_mapping_no_chain(self):
        sdm = ScenarioDatabaseManager(self.config, 'db_chain_granddad')
        d_mapping = sdm.get_database_to_table_mapping()
        
        expected = {
            'db_chain_granddad': ['base_schema', 'base_schema2', 'scenario_information']
        }
        self.assertEqual(len(expected.keys()), len(d_mapping.keys()))
        for k,v in d_mapping.items():
            self.assertTrue(k in expected)
            for table in v:
                self.assertTrue(table in expected[k])            
    
    def test_database_to_table_mapping_chain(self):
        sdm = ScenarioDatabaseManager(self.config, 'db_chain_son')
        d_mapping = sdm.get_database_to_table_mapping()
        
        expected = {
            'db_chain_son': ['base_schema2', 'scenario_information'],
            'db_chain_dad': ['base_schema']
        }
        self.assertEqual(len(expected.keys()), len(d_mapping.keys()))
        for k,v in d_mapping.items():
            self.assertTrue(k in expected)
            for table in v:
                self.assertTrue(table in expected[k]) 
    
    def test_jdbc_url_overwritten_properly(self):
        sdm = ScenarioDatabaseManager(self.config, 'db_chain_son')
        
        url = 'jdbc:mysql://name.host.domain/db_chain_dad'
        u = self.db_chain_son.get_table('scenario_information').update(
              values = {
                self.db_chain_son.get_table('scenario_information').c.parent_database_url:url})   
        self.db_chain_son.execute(u)       
             
        sdm._get_table_mapping('db_chain_son', {})
        
        s = select(
            columns=[self.db_chain_son.get_table('scenario_information').c.parent_database_url])
        result = self.db_chain_son.execute(s)
        
        output_url = result.fetchone()[0]
        expected_url = 'db_chain_dad'
        self.assertEqual(output_url, expected_url)

if __name__ == '__main__':
    opus_unittest.main()