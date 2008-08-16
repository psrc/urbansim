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

import os
from opus_core.tests import opus_unittest
import tempfile
from shutil import rmtree

from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.session_configuration import SessionConfiguration
from psrc.travel_model_input_file_writer import TravelModelInputFileWriter

from opus_core.misc import does_test_database_server_exist
if does_test_database_server_exist(module_name=__name__):

    class TestTravelModelInputFileWriter(opus_unittest.OpusIntegrationTestCase):
        def setUp(self):
            self.database_name = 'test_travel_model_input_file_writer'
            
            self.dbconfig = DatabaseServerConfiguration(
                 protocol = 'mysql',
                 test = True)
            
            self.db_server = DatabaseServer(self.dbconfig)
            
            self.db_server.drop_database(self.database_name)
            self.db_server.create_database(self.database_name)
            self.database = self.db_server.get_database(self.database_name)
            
            self.create_jobs_table(self.database)
            self.create_zones_table(self.database)
            self.create_employment_sector_groups_table(self.database)
            self.create_constant_taz_columns_table(self.database)
            self.create_households_table(self.database)
            self.tempdir_path = tempfile.mkdtemp(prefix='opus_tmp')
    
        def tearDown(self):
            self.database.close()
            self.db_server.drop_database(self.database_name)
            if os.path.exists(self.tempdir_path):
                rmtree(self.tempdir_path)
    
        def test_create_tripgen_travel_model_input_file(self):
            from urbansim.datasets.gridcell_dataset import GridcellDataset
            from urbansim.datasets.job_dataset import JobDataset
            from urbansim.datasets.household_dataset import HouseholdDataset
            from urbansim.datasets.constant_taz_column_dataset import ConstantTazColumnDataset
            
            in_storage = StorageFactory().get_storage(
                  'sql_storage',
                  storage_location = self.database)
            sc = SessionConfiguration(new_instance=True,
                                 package_order = ['urbansim', 'psrc'],
                                 in_storage=in_storage)
            dataset_pool = sc.get_dataset_pool()
            #zone_set = dataset_pool.get_dataset('zone')
            #hh_set = dataset_pool.get_dataset('household')
            #job_set = dataset_pool.get_dataset('job')
            #taz_col_set = dataset_pool.get_dataset('constant_taz_column')
            
            TravelModelInputFileWriter().run(self.tempdir_path, 2000, dataset_pool)
            
            logger.log_status('tazdata path: ', self.tempdir_path)
            # expected values - data format: {zone:{column_value:value}}
            expected_tazdata = {1:{101: 19.9, 
                                   102: 2, 103: 0, 104:1, 105:0,
                                   106: 3, 107:11, 109:1, 
                                   110:0, 111:0, 112:0, 113:0, 114:0, 
                                   115:0, 116:0, 117:0, 118:0, 119:0, 
                                   120:2, 121:42, 122:0, 123:0, 124:11}, 
                                2:{101: 29.9, 
                                   102: 0, 103: 2, 104:1, 105:3,
                                   106: 1, 107:3, 109:0, 
                                   110:0, 111:0, 112:0, 113:3, 114:0, 
                                   115:0, 116:0, 117:0, 118:1, 119:1, 
                                   120:0, 121:241, 122:0, 123:0, 124:3}}
            
            # get real data from file
            real_tazdata = {1:{},2:{}}
            tazdata_file = open(os.path.join(self.tempdir_path, 'tripgen', 'inputtg', 'tazdata.ma2'), 'r')
            for a_line in tazdata_file.readlines():
                if a_line[0].isspace():
                    numbers = a_line.replace(':', ' ').split() # data line format:  1   101:  15.5
                    zone_id = int(numbers[0])
                    column_var = int(numbers[1])
                    value = float(numbers[2])
                    real_tazdata[zone_id][column_var] = value
    
            for zone in expected_tazdata.keys():
                for col_var in expected_tazdata[zone].keys():
                    self.assertAlmostEqual(real_tazdata[zone][col_var], expected_tazdata[zone][col_var], 3,\
                                           "zone %d, column variable %d did not match up."%(zone, col_var))
        

        def create_households_table(self, database):
            database.DoQuery("drop table if exists households")
            database.DoQuery("create table households (household_id int(11), zone_id int(11), income int(11), year int(11))")
            database.DoQuery("insert into households values(1, 1, 10, 2000), (2, 1, 11, 2000), (3, 2, 12, 2000), (4, 2, 13, 2000), (5, 2, 14, 2000), (6, 1, 15, 2000), (7, 2, 16, 2000), (8, 2, 16, 2000), (9, 2, 17, 2000)")
            # 9 houses total
            #incomes: 10, 11, 12, 13, 14, 15, 16, 16, 17
            # med=14, low_med=11.5, upper_med=16
            # in zone_1: 1,2,6

        def create_zones_table(self, database):
            database.DoQuery("drop table if exists zones")
            database.DoQuery("create table zones (zone_id int(11))")
            database.DoQuery("insert into zones values (1), (2)")   

        def create_employment_sector_groups_table(self, database):
            database.DoQuery("drop table if exists employment_sectors")
            database.DoQuery("create table employment_sectors (sector_id int(11))")
            database.DoQuery("insert into employment_sectors values (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12),(13),(14),(15),(16),(17),(18),(19)")
            
            
            database.DoQuery("drop table if exists employment_adhoc_sector_groups")
            database.DoQuery("create table employment_adhoc_sector_groups (group_id int(11), name varchar(16))")
            database.DoQuery("insert into employment_adhoc_sector_groups values (2, 'retail'), (21, 'manu'), (22, 'wtcu'), (24, 'fires'), (25, 'gov'), (26, 'edu')")

            database.DoQuery("drop table if exists employment_adhoc_sector_group_definitions")
            database.DoQuery("create table employment_adhoc_sector_group_definitions (sector_id int(11), group_id int(11))")
            database.DoQuery("insert into employment_adhoc_sector_group_definitions values (7, 2), (14, 2), (3,21), (4,21), (5,21), (6,22), (8,22), (9,22), (10,22), (11,24), (12,24), (13,24), (16,24), (17,24), (18,25), (15,26), (19,26)")
            
        def create_jobs_table(self, database):
            database.DoQuery("drop table if exists jobs")
            database.DoQuery("create table jobs (job_id int(11), zone_id int(11), sector_id int(11), year int(11))")
            database.DoQuery("insert into jobs values (1, 1, 1, 2000), (2, 1, 3, 2000), (3, 1, 4, 2000), (4, 1, 7, 2000), (5, 2, 9, 2000), " + \
                             "(6, 2, 11, 2000), (7, 2, 15, 2000), (8, 2, 16, 2000), (9, 2, 17, 2000)")
    
        def create_constant_taz_columns_table(self, database):
            database.DoQuery("drop table if exists constant_taz_columns")
            database.DoQuery("create table constant_taz_columns (`TAZ` int(11), `PCTMF` double, `GQI` int(11), `GQN` int(11), " + \
                             "`FTEUNIV` int(11), `DEN` int(11), `FAZ` int(11), `YEAR` int(11))")
            database.DoQuery("insert into constant_taz_columns values " + \
                             "(1, 19.9, 3, 11, 42, 1, 1, 2000), " + \
                             "(2, 29.9, 1, 3, 241, 2, 2, 2000)")
                                                                                       

if __name__ == "__main__":
    opus_unittest.main()