# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import re

from opus_core.logger import logger
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration



class DBSubPattern(object):
    def convert_databases(self, db_config, databases, tables, patterns, backup=True, backup_postfix='_old'):
        dbconfig = DatabaseServerConfiguration(
            host_name = db_config.host_name,
            protocol = 'mysql',
            user_name = db_config.user_name,
            password = db_config.password                                       
        )
        db_server = DatabaseServer(dbconfig)
        
        for db_name in databases:
            db = db_server.get_database(db_name)
            self.convert_database(db, tables[db_name], patterns, backup, backup_postfix)
            db.close()
            
        db_server.close()
    
    def convert_database(self, db, tables, patterns, backup=True, backup_postfix='_old'):
        for table in tables:
            self.convert_table(db, table, patterns, backup, backup_postfix)
    
    def convert_table(self, db, table_name, patterns, backup=True, backup_postfix='_old'):
        try: db.DoQuery('select * from %s' % table_name)
        except: return
        
        if backup:
            backup_table_name = '%s%s' % (table_name, backup_postfix)
            
            i=0
            while self._table_exists(db, backup_table_name):
                i+=1
                backup_table_name = '%s%s%d' % (table_name, backup_postfix, i)

            db.DoQuery('create table %(backup_table)s select * from %(table)s;'
                        % {'backup_table':backup_table_name,
                           'table':table_name})
                           
            try: db.DoQuery('select * from %s' % backup_table_name)
            except:
                logger.log_error("Back up of table '%s' to '%s' failed. "
                    "Skipping conversion." % (table_name, backup_table_name))
                return
        
        results = db.GetResultsFromQuery('select variable_name from %s' 
                                          % table_name)[1:]
        
        results = [i[0] for i in results]
        
        for i in range(len(results)):
            try:
                new_row = results[i]
                for pattern, replacement in patterns:
                    new_row = re.sub(pattern, replacement, new_row)
            except TypeError:
                continue # Not dealing with a string here.

            if new_row == results[i]: 
                continue # Nothing changed. Don't bother with the update query.

            new_row = '"%s"' % new_row
                
            query = ('update %(table)s set variable_name=%(new_row)s where '
                'variable_name="%(old_row)s";' 
                % {'table':table_name,
                   'new_row':new_row, 
                   'old_row':results[i]})

            db.DoQuery(query)

    def _table_exists(self, db, table_name):
        try: db.DoQuery('select * from %s' % table_name)
        except: return False
        else: return True


from opus_core.tests import opus_unittest
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class TestDBSubPattern(opus_unittest.OpusTestCase):
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
            
        table_schema = 'id INT, do_not_change_this_column TEXT, variable_name TEXT'
        table_data = (
            '(1,"Does not match P A T T E R N.","Matches pattern."),'
            '(2,"Matches pattern.","Does not match P A T T E R N."),'
            '(3,NULL,NULL),'
            '(4,"","")'
            )
            
        self.expected_output_unchanged = [
            ['id', 'do_not_change_this_column', 'variable_name'],
            [1,"Does not match P A T T E R N.","Matches pattern."],
            [2,"Matches pattern.","Does not match P A T T E R N."],
            [3,None,None],
            [4,"",""]
            ]
        
        self.patterns = [
            (r'(pattern)(\.)', r'\1 well\2'),
            (r'^Matches pattern well\.$', r'Matches pattern perfectly!')
            ]
        
        self.expected_output_changed = [
            ['id', 'do_not_change_this_column', 'variable_name'],
            [1,"Does not match P A T T E R N.","Matches pattern perfectly!"],
            [2,"Matches pattern.","Does not match P A T T E R N."],
            [3,None,None],
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
                       table_schema))
                
                db.DoQuery(insert_items_template 
                            % {'table':table_name, 'data':table_data})
                
        
    def tearDown(self):
        for db_name in self.test_db_names:
            self.db_server.drop_database(db_name)
            
        for db in self.dbs:
            db.close()
            
        self.db_server.close()
        
        
    def test_convert_table(self):
        DBSubPattern().convert_table(self.dbs[0], self.test_table_names[0], 
            self.patterns)
        
        db = self.dbs[0]
        
        table0 = self.test_table_names[0]
        results = db.GetResultsFromQuery('select * from %s;' % table0)
        self.assert_(results == self.expected_output_changed,
            "Convert failed for single table (%s) -- incorrect conversion."
            " Expected %s. Recieved %s." 
                % (table0,
                   self.expected_output_changed,
                   results))
                       
        for table in self.test_table_names[1:]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assert_(results == self.expected_output_unchanged,
                "Convert failed for single table (%s) -- incorrect conversion."
                " Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_unchanged,
                       results))
        
        for db in self.dbs[1:]:
            for table in self.test_table_names:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assert_(results == self.expected_output_unchanged,
                    "Convert failed for single table (%s) -- converted wrong"
                        " table(s). Expected %s. Recieved %s." 
                            % (table,
                               self.expected_output_unchanged,
                               results))
        
        
    def test_convert_table_backup(self):
        db = self.dbs[0]
        table = self.test_table_names[0]
        
        DBSubPattern().convert_table(db, table, self.patterns,
                                        backup=True, backup_postfix='_old')
        backup_table_name = '%s_old' % table
        try:
            results = db.GetResultsFromQuery('select * from %s' % backup_table_name)
        except:
            self.fail("Backup failed for single table (%s) -- backup table (%s) not "
                "created." % (table, backup_table_name))
            
        self.assert_(results == self.expected_output_unchanged,
            "Backup failed for single table (%s) -- changed contents."
            " Expected %s. Recieved %s." 
                % (table, self.expected_output_unchanged, results)
            )
                                
                   
    def test_convert_database(self):
        DBSubPattern().convert_database(self.dbs[0], 
            self.test_table_names[0:2], self.patterns)
        
        db = self.dbs[0]
        for table in self.test_table_names[0:2]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assert_(results == self.expected_output_changed,
                "Convert failed for database0 (%s) -- incorrect "
                "conversion. Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_changed,
                       results))
                       
        for table in self.test_table_names[2:]:
            results = db.GetResultsFromQuery('select * from %s;' % table)
            self.assert_(results == self.expected_output_unchanged,
                "Convert failed for database0 (%s) -- changed wrong table(s)."
                " Expected %s. Recieved %s." 
                    % (table,
                       self.expected_output_unchanged,
                       results))
        
        for i in range(len(self.dbs[1:])):
            db = self.dbs[i+1]
            
            for table in self.test_table_names:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assert_(results == self.expected_output_unchanged,
                    "Convert failed for database%s (%s) -- converted wrong"
                        " table(s). Expected %s. Recieved %s." 
                            % (i,
                               table, 
                               self.expected_output_unchanged,
                               results))

                               
    def test_convert_databases(self):
        DBSubPattern().convert_databases(TestDatabaseConfiguration(protocol='mysql'), 
            self.config['databases'], self.config['tables'], self.patterns)
        
        for db_name in self.config['databases']:
            db = self.db_server.get_database(db_name)
            
            tables = self.config['tables'][db_name]
            for table in tables:
                results = db.GetResultsFromQuery('select * from %s;' % table)
                self.assert_(results == self.expected_output_changed,
                    "Convert failed %s (%s) -- incorrect conversion."
                        " Expected %s. Recieved %s." 
                            % (db_name,
                               table,
                               self.expected_output_changed,
                               results))
    
        
if __name__ == "__main__":
    opus_unittest.main()