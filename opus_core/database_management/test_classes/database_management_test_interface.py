#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.tests import opus_unittest
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration

from sqlalchemy.schema import Table
from sqlalchemy.types import Integer, SmallInteger, Float, Numeric, \
    VARCHAR, Boolean, CLOB, DateTime


base_schema = {
    'integer_col':'INTEGER',
    'clob_col':'TEXT',
    'smallinteger_col':'SHORT',
    'float_col':'FLOAT'                
}

base_schema2 = {
    'integer_col':'INTEGER',
    'numeric_col':'DOUBLE',
    'varchar_col':'VARCHAR',
    'boolean_col':'BOOLEAN'                
}

base_scenario_information_schema = {
    'parent_database_url':'VARCHAR'
}

class DatabaseManagementTestInterface(opus_unittest.OpusTestCase):
    def setUp(self):        
        self.databases = ['db_chain_son', 'db_chain_dad', 'db_chain_granddad']
        
        self.config = DatabaseServerConfiguration(test = True)
        self.server = DatabaseServer(self.config)
        self._create_databases()
        self.db_chain_granddad = self.server.get_database('db_chain_granddad')
        self.db_chain_dad = self.server.get_database('db_chain_dad')
        self.db_chain_son = self.server.get_database('db_chain_son')
        
        self._create_tables()
        self.granddad_schema = self.db_chain_granddad.get_table('base_schema')
        self.dad_schema = self.db_chain_dad.get_table('base_schema')
        self.granddad_schema2 = self.db_chain_granddad.get_table('base_schema2')
        self.son_schema2 = self.db_chain_son.get_table('base_schema2')
        
        self._seed_values()
        
    def _create_databases(self):
        
        for db in self.databases:
            try: 
                self.server.drop_database(db)
            except:
                pass
            
            self.server.create_database(db)
        
    def _create_tables(self):
        self.db_chain_granddad.create_table_from_schema('base_schema', base_schema)
        self.db_chain_granddad.create_table_from_schema('base_schema2', base_schema2)
        self.db_chain_granddad.create_table_from_schema('scenario_information', base_scenario_information_schema)
        
        self.db_chain_dad.create_table_from_schema('base_schema', base_schema)
        self.db_chain_dad.create_table_from_schema('scenario_information', base_scenario_information_schema)

        self.db_chain_son.create_table_from_schema('base_schema2', base_schema2)
        self.db_chain_son.create_table_from_schema('scenario_information', base_scenario_information_schema)
        
    def _seed_values(self):
        u = self.db_chain_granddad.get_table('scenario_information').insert(
              values = {
                self.db_chain_granddad.get_table('scenario_information').c.parent_database_url:''})   
        self.db_chain_granddad.engine.execute(u)
        
        u = self.db_chain_dad.get_table('scenario_information').insert(
              values = {
                self.db_chain_dad.get_table('scenario_information').c.parent_database_url:'db_chain_granddad'})

        self.db_chain_dad.engine.execute(u)
        u = self.db_chain_son.get_table('scenario_information').insert(
              values = {
                self.db_chain_son.get_table('scenario_information').c.parent_database_url:'db_chain_dad'})   
        self.db_chain_son.engine.execute(u)
        
        granddad_vals = [
            {'integer_col': 0, 'clob_col': '0', 'smallinteger_col': 0, 'float_col': 0.0},                      
            {'integer_col': 2, 'clob_col': '2', 'smallinteger_col': 2, 'float_col': 2.0},                          
            {'integer_col': 4, 'clob_col': '4', 'smallinteger_col': 4, 'float_col': 4.0}                                         
        ]

        dad_vals = [
            {'integer_col': 0, 'clob_col': '0', 'smallinteger_col': 0, 'float_col': 0.0},  
            {'integer_col': 1, 'clob_col': '1', 'smallinteger_col': 1, 'float_col': 1.0},                   
            {'integer_col': 2, 'clob_col': '2', 'smallinteger_col': 2, 'float_col': 2.0},  
            {'integer_col': 3, 'clob_col': '3', 'smallinteger_col': 3, 'float_col': 3.0},                        
            {'integer_col': 4, 'clob_col': '4', 'smallinteger_col': 4, 'float_col': 4.0}                                         
        ]    
        
        granddad_vals2 = [
            {'integer_col': 0, 'varchar_col': '0', 'boolean_col': True, 'numeric_col': 0.0},                      
            {'integer_col': 2, 'varchar_col': '2', 'boolean_col': True, 'numeric_col': 2.0},                          
            {'integer_col': 4, 'varchar_col': '4', 'boolean_col': True, 'numeric_col': 4.0}                                         
        ]

        son_vals2 = [
            {'integer_col': 0, 'varchar_col': '0', 'boolean_col': False, 'numeric_col': 0.0},                      
            {'integer_col': 4, 'varchar_col': '4', 'boolean_col': False, 'numeric_col': 4.0}                                         
        ]
        
        self.db_chain_granddad.engine.execute(self.granddad_schema.insert(), granddad_vals)
        self.db_chain_granddad.engine.execute(self.granddad_schema2.insert(), granddad_vals2)        
        self.db_chain_dad.engine.execute(self.dad_schema.insert(), dad_vals)
        self.db_chain_son.engine.execute(self.son_schema2.insert(), son_vals2)
                     
    def tearDown(self):
        self.db_chain_granddad.close()
        self.db_chain_dad.close()
        self.db_chain_son.close()
        
        self.server.drop_database('db_chain_granddad')
        self.server.drop_database('db_chain_dad')
        self.server.drop_database('db_chain_son')
        
        self.server.close()
        