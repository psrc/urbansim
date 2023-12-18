# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

class ConvertDatabase(object):
    def convert_databases(self, db_config, config):
        databases = config['databases']
        tables = config['tables']
        
        try: backup = config['backup']
        except KeyError: backup = True
        
        try: backup_postfix = config['backup_postfix']
        except KeyError: backup_postfix = '_old'
        
        dbconfig = DatabaseServerConfiguration(
            protocol = 'mysql',
            host_name = db_config.host_name,
            user_name = db_config.user_name,
            password = db_config.password                                       
        )
        db_server = DatabaseServer(dbconfig)
        
        for db_name in databases:
            db = db_server.get_database(db_name)

            self.convert_database(db, tables[db_name], backup, backup_postfix)
                
            db.close()
            
        db_server.close()
    
    
    def convert_database(self, db, tables, backup=True, backup_postfix='_old'):
        for table in tables:
            self.convert_table(db, table, backup, backup_postfix)
    
    
    def convert_table(self, db, table_name, backup=True, backup_postfix='_old'):
        try: db.DoQuery('select * from %s' % table_name)
        except: return
        
        if backup:
            backup_table_name = '%s%s' % (table_name, backup_postfix)
            
            db.DoQuery('drop table if exists %(backup_table)s;'
                        % {'backup_table':backup_table_name})
            
            db.DoQuery('create table %(backup_table)s select * from %(table)s;'
                        % {'backup_table':backup_table_name,
                           'table':table_name})
        
        results = db.GetResultsFromQuery('select variable_name from %s' 
                                          % table_name)[1:]
        
        results = [i[0] for i in results]
        
        for i in range(len(results)):
            if results[i] is None: results[i] = "NULL"
            else:
                try: results[i] = '"' + results[i] + '"'
                except: pass
                
            new_row = results[i].replace('opus.','')
            new_row = new_row.replace('core','opus_core')
            
            query = ('update %(table)s set variable_name=%(new_row)s where '
                'variable_name=%(old_row)s;' 
                % {'table':table_name,
                   'new_row':new_row, 
                   'old_row':results[i]})
            
            db.DoQuery(query)


from opus_core.tests import opus_unittest

from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class TestConvertDatabases(opus_unittest.OpusTestCase):
    def setUp(self):
        self.test_db_names = [
            'convert_database_test_db1', 
            'convert_database_test_db2',
            ]
        
        self.test_table_names = [
            'table1',
            'table2',
            'table3',
            ]
            
        table_structure = 'id INT, do_not_change_this_column TEXT, variable_name TEXT'
        table_data = (
            '(1,"No opus dot.","constant"),'
            '(2,"opus.core.miscellaneous","No opus dot."),'
            '(3,"opus.urbansim.gridcell.percent_water",'
                '"gc_cbd = gridcell.disaggregate('
                    'opus.psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)"),'
            '(4,"","")'
            )
            
        self.expected_output_unchanged = [
            ['id', 'do_not_change_this_column', 'variable_name'],
            [1,"No opus dot.","constant"],
            [2,"opus.core.miscellaneous","No opus dot."],
            [3,"opus.urbansim.gridcell.percent_water",
                "gc_cbd = gridcell.disaggregate("
                    "opus.psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)"],
            [4,"",""]
            ]
        
        self.expected_output_changed = [
            ['id', 'do_not_change_this_column', 'variable_name'],
            [1,"No opus dot.","constant"],
            [2,"opus.core.miscellaneous","No opus dot."],
            [3,"opus.urbansim.gridcell.percent_water",
                "gc_cbd = gridcell.disaggregate("
                    "psrc.zone.generalized_cost_hbw_am_drive_alone_to_129)"],
            [4,"",""]
            ]
            
        insert_items_template = (
            "insert into %(table)s values %(data)s;")
        
        table_list = {}
        for db_name in self.test_db_names:
            table_list[db_name] = []
            for table in self.test_table_names:
                table_list[db_name] += [table]
        
        self.config = {
            'databases':self.test_db_names,
            'tables':table_list,
            
            'backup':True,
            'backup_postfix':'_old',
            }
            
            
        self.db_server = DatabaseServer(TestDatabaseConfiguration(protocol = 'mysql'))
        
        self.dbs = []
        for db_name in self.test_db_names:
            self.db_server.drop_database(db_name)
            self.db_server.create_database(db_name)
            self.dbs += [self.db_server.get_database(db_name)]
        
        for db in self.dbs:
            for table_name in self.test_table_names:
                db.DoQuery('create table %s (%s)' 
                    % (table_name,
                       table_structure))
                
                db.DoQuery(insert_items_template 
                            % {'table':table_name, 'data':table_data})
                
        
    def tearDown(self):
        for db_name in self.test_db_names:
            self.db_server.drop_database(db_name)
            
        for db in self.dbs:
            db.close()
            
        self.db_server.close()
        
        
    def test_convert_table(self):
        ConvertDatabase().convert_table(self.dbs[0], self.test_table_names[0])
        
        db = self.dbs[0]
        
        table0 = self.test_table_names[0]
        results = db.GetResultsFromQuery('select * from %s;' % table0)
        self.assertTrue(results == self.expected_output_changed,
            "Convert failed for single table (%s) -- incorrect conversion."
            " Expected %s. Recieved %s." 
                % (table0,
                   self.expected_output_changed,
                   results))
                       
        for table in self.test_table_names[1:]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assertTrue(results == self.expected_output_unchanged,
                "Convert failed for single table (%s) -- incorrect conversion."
                " Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_unchanged,
                       results))
        
        for db in self.dbs[1:]:
            for table in self.test_table_names:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assertTrue(results == self.expected_output_unchanged,
                    "Convert failed for single table (%s) -- converted wrong"
                        " table(s). Expected %s. Recieved %s." 
                            % (table,
                               self.expected_output_unchanged,
                               results))
        
        
    def test_convert_table_backup(self):
        db = self.dbs[0]
        table = self.test_table_names[0]
        
        ConvertDatabase().convert_table(db, table,
                                        backup=True, backup_postfix='_old')
        
        results = db.GetResultsFromQuery('select * from %s_old;' % table)
        self.assertTrue(results == self.expected_output_unchanged,
            "Backup failed for single table (%s) -- changed contents."
            " Expected %s. Recieved %s." 
                % (table,
                   self.expected_output_unchanged,
                   results))
                   
                   
    def test_convert_database(self):
        ConvertDatabase().convert_database(self.dbs[0], 
            self.test_table_names[0:2])
        
        db = self.dbs[0]
        for table in self.test_table_names[0:2]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assertTrue(results == self.expected_output_changed,
                "Convert failed for database0 (%s) -- incorrect "
                "conversion. Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_changed,
                       results))
                       
        for table in self.test_table_names[2:]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assertTrue(results == self.expected_output_unchanged,
                "Convert failed for database0 (%s) -- changed wrong table(s)."
                " Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_unchanged,
                       results))
        
        for i in range(len(self.dbs[1:])):
            db = self.dbs[i+1]
            
            for table in self.test_table_names:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assertTrue(results == self.expected_output_unchanged,
                    "Convert failed for database%s (%s) -- converted wrong"
                        " table(s). Expected %s. Recieved %s." 
                            % (i,
                               table, 
                               self.expected_output_unchanged,
                               results))

                               
    def test_convert_databases(self):
        ConvertDatabase().convert_databases(TestDatabaseConfiguration(protocol='mysql'), self.config)
        
        for db_name in self.config['databases']:
            db = self.db_server.get_database(db_name)
            
            tables = self.config['tables'][db_name]
            for table in tables:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assertTrue(results == self.expected_output_changed,
                    "Convert failed %s (%s) -- incorrect conversion."
                        " Expected %s. Recieved %s." 
                            % (db_name,
                               table,
                               self.expected_output_changed,
                               results))
    
        
if __name__ == "__main__":
    opus_unittest.main()