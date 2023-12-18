# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import re

from opus_core.logger import logger
from opus_core.database_management.database_server import DatabaseServer



class RenameBySwappingEmploymentAndCommercialOrIndustrialOrHomeBasedForElcm(object):
    def rename_by_swapping_employment_and_commercial_or_industrial_or_home_based_for_elcm(self, 
            db_config, db_name):
                
        db_server = DatabaseServer(db_config)
        
        try:
            db = db_server.get_database(db_name)
        except:
            raise NameError("Unknown database '%s'!" % db_name)
        
        pattern_template = '%s_%s_location_choice_model_%s'
        pattern = re.compile('^%s$' % pattern_template 
            % ('(employment)',
               '(commercial|industrial|home_based)', 
               '(specification|coefficients)'
               ))
        
        new_tables = []
        for table in db.get_tables_in_database():
            match = pattern.match(table)
            if match:
                new_tables.append((pattern_template 
                        # Swap around employment and commercial/industrial/home_based
                        % (match.group(2), match.group(1), match.group(3)), 
                    table))

        if len(new_tables) == 0:
            logger.log_warning('No tables to convert!')
            return

        for new_name, old_name in new_tables:
            logger.log_status('Renaming %s to %s.' % (old_name, new_name))
            db.drop_table(new_name)
            db.DoQuery('CREATE TABLE %s SELECT * FROM %s;' 
                % (new_name, old_name))
            # Rename old table
            db.drop_table('%s_old' %old_name)
            db.DoQuery('RENAME TABLE %s TO %s_old;' % (old_name, old_name))
        

import os    
from opus_core.tests import opus_unittest

from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration

class TestRenameBySwappingEmploymentAndCommercialOrIndustrialForElcm(opus_unittest.OpusTestCase):
    def setUp(self):
        self.db_name = 'test_rename_commercial_and_industrial'
        
        self.db_server = DatabaseServer(TestDatabaseConfiguration(protocol = 'mysql'))
        
        self.db_server.drop_database(self.db_name)
        self.db_server.create_database(self.db_name)
        self.db = self.db_server.get_database(self.db_name)
        
        self.tables_to_convert = (
            'employment_commercial_location_choice_model_specification',
            'employment_commercial_location_choice_model_coefficients',
            'employment_industrial_location_choice_model_specification',
            'employment_industrial_location_choice_model_coefficients',
            )
            
        self.other_tables = (
            'i_am_not_to_be_renamed_location_choice_model_specifications',
            'i_am_not_to_be_renamed_location_choice_model_coefficients',
            'employment_industrial_location_choice_model_coefficients_old',
            )
        
        for table in self.tables_to_convert + self.other_tables:
            self.db.DoQuery('CREATE TABLE %s (id INT);' % table)
            
        self.output_tables = (
            'commercial_employment_location_choice_model_specification',
            'commercial_employment_location_choice_model_coefficients',
            'industrial_employment_location_choice_model_specification',
            'industrial_employment_location_choice_model_coefficients',
            )
        
        
    def tearDown(self):
        self.db.close()
        self.db_server.drop_database(self.db_name)
        self.db_server.close()
        
        
    def test_setUp(self):
        for table in self.tables_to_convert + self.other_tables:
            if not self.db.table_exists(table):
                self.fail('Expected test table %s did not exist. (Check setUp)' 
                    % table)
                    
        for table in self.output_tables:
            if self.db.table_exists(table):
                self.fail('Unexpected results table %s exists. (Check setUp)' 
                    % table)
        
        
    def test_rename_tables(self):
        r = RenameBySwappingEmploymentAndCommercialOrIndustrialOrHomeBasedForElcm()
        r.rename_by_swapping_employment_and_commercial_or_industrial_or_home_based_for_elcm(
            TestDatabaseConfiguration(protocol = 'mysql'), self.db_name)
        
        for table in self.output_tables + self.other_tables:
            if not self.db.table_exists(table):
                self.fail('Expected output table %s does not exist.' % table)
                    
        for table in self.tables_to_convert:
            if self.db.table_exists(table):
                self.fail('Input table %s still exists.' % table)
        
        
if __name__ == '__main__':
    opus_unittest.main()