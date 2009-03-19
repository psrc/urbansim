# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.logger import logger
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration



class CombineTables(object):
    def combine_tables(self, db_config, db_name, from_tables_names, to_table_name):
        dbconfig = DatabaseServerConfiguration(
            host_name = db_config.host_name,
            protocol = 'mysql',
            user_name = db_config.user_name,
            password = db_config.password                                       
        )
        db_server = DatabaseServer(dbconfig)
        
        try:
            db = db_server.get_database(db_name)
        except:
            raise NameError, "Unknown database '%s'!" % db_name

        union_statements = []
        for from_table_name in from_tables_names:
            union_statements.append('(SELECT * FROM %s)' % from_table_name)
            
        create_table_query = "CREATE TABLE %s " % to_table_name
        create_table_query += ' UNION ALL '.join(union_statements)
        create_table_query += ';'
        
        try:
            db.DoQuery('DROP TABLE IF EXISTS %s;' % to_table_name)
            db.DoQuery(create_table_query)
        except:
            raise NameError, "Unknown or invalid table specified!"
                    

import os    
from opus_core.tests import opus_unittest
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class TestCombineTables(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_server = DatabaseServer(TestDatabaseConfiguration(protocol = 'mysql'))
        self.db_name = 'test_combine_tables'
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
        
        self.from_tables = (
            ('table_a', 'A'), 
            ('table_b', 'B'),
            ('table_c', 'C'),
            ('table_d', 'D'),
            )
        table_ids = {
            'table_a': [1], 
            'table_b': [2,3],
            'table_c': [4,5,6,7],
            'table_d': [8,9,10,11,12,13,14,15],
            }
        self.to_table = 'to_table'
        
        for table, type in self.from_tables:
            self.db.DoQuery('CREATE TABLE %s (job_id INT, sector_id INT, '
                'grid_id INT, sic INT, building_type varchar(5), '
                'home_based tinyint(4), impute_flag tinyint(4));' 
                    % table)

            values = ','.join(
                ['(%(j)s, %(j)s, %(j)s, %(j)s, "%(type)s", %(j)s, %(j)s)' 
                    % {'j':j, 'type':type} for j in table_ids[table]]
                )
            self.db.DoQuery('INSERT INTO %(table_name)s (job_id, sector_id, '
                'grid_id, sic, building_type, home_based, impute_flag) VALUES '
                '%(values)s;' 
                    % {'table_name':table,
                       'values':values,
                      }
                )
            number_rows = self.db.GetResultsFromQuery('SELECT count(*) FROM %s' % table)[1][0]
            self.assertEqual(number_rows, len(table_ids[table]))
                        
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        for table, type in self.from_tables:
            try:
                self.db.DoQuery('select * from %s;' % table)
            except:
                self.fail('Expected input table %s did not exist. (Check setUp)' 
                    % self.from_table)
                    
        try:
            self.db.DoQuery('select * from %s;' % self.to_table)
            self.fail('Output table %s already exists. (Check setUp)' 
                % self.to_table)
        except: pass
        
    
    def test_create_table(self):
        CombineTables().combine_tables(TestDatabaseConfiguration(protocol='mysql'), self.db_name, 
            [i[0] for i in self.from_tables], 
            self.to_table)
        
        try:
            self.db.DoQuery('select * from %s;' % self.to_table)
        except: 
            self.fail('Output table %s not created.' % self.to_table)
        
    
    def test_combine_tables(self):
        CombineTables().combine_tables(TestDatabaseConfiguration(protocol='mysql'), self.db_name, 
            [i[0] for i in self.from_tables], 
            self.to_table)
        
        expected_rows = 0
        for table, type in self.from_tables:
            count = self.db.GetResultsFromQuery('select count(*) from %s' 
                % table)[1:][0][0]
            expected_rows += count
        
        try:
            count = self.db.GetResultsFromQuery('select count(*) from %s;' 
                % self.to_table)[1:][0][0]
        except:
            self.fail('Expected output table %s does not exist.' % self.to_table)

        if (expected_rows != count):
            for table_name, type in self.from_tables:
                self._print_table(table_name)
            self._print_table(self.to_table)
            
        self.assert_(expected_rows == count,
            'Incorrect number of rows in output. Expected %s; received %s.'
                % (expected_rows, count))

    def _print_table(self, table_name):
        """Provide debugging info to figure out why the above test is failing, sometimes."""
        try:
            results = self.db.GetResultsFromQuery('select * from %s' % table_name)
            logger.start_block('Contents of table %s' % table_name)
            try:
                for row in results:
                    logger.log_status(row)
            finally:
                logger.end_block()
        except:
            logger.log_status('Error accessing table %s' % table_name)
            logger.log_stack_trace()
        
if __name__ == '__main__':
    opus_unittest.main()