# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from opus_core.tests import opus_unittest
import tempfile
from shutil import rmtree

from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.test_database_configuration import TestDatabaseConfiguration
from opus_core.session_configuration import SessionConfiguration
from psrc_parcel.travel_model_input_file_writer import TravelModelInputFileWriter

class TestTravelModelInputFileWriter(opus_unittest.OpusTestCase):
    def setUp(self):
        self.database_name = 'test_tm_input_file_writer_with_worker_files'
        
        self.dbconfig = TestDatabaseConfiguration()
        
        self.db_server = DatabaseServer(self.dbconfig)
        
        self.db_server.drop_database(self.database_name)
        self.db_server.create_database(self.database_name)
        self.database = self.db_server.get_database(self.database_name)
        
        self.create_jobs_table(self.database)
        self.create_zones_table(self.database)
        self.create_employment_sector_groups_table(self.database)
        self.create_constant_taz_columns_table(self.database)
        self.create_households_table(self.database)
        self.create_persons_table(self.database)
        self.tempdir_path = tempfile.mkdtemp(prefix='opus_tmp')

    def tearDown(self):
        self.database.close()
        self.db_server.drop_database(self.database_name)
        if os.path.exists(self.tempdir_path):
            rmtree(self.tempdir_path)

    def test_create_tripgen_travel_model_input_files(self):
        in_storage = StorageFactory().get_storage(
              'sql_storage',
              storage_location = self.database)
        sc = SessionConfiguration(new_instance=True,
                             package_order = ['urbansim', 'psrc'],
                             in_storage=in_storage)
        dataset_pool = sc.get_dataset_pool()
        
        TravelModelInputFileWriter().run(self.tempdir_path, 2000, dataset_pool)
        
        logger.log_status('tazdata path: ', self.tempdir_path)
        # expected values - data format: {zone:{column_value:value}}
        expected_tazdata = {1: [[1,1], [1,2]], 
                            2: [[2,2]], 
                            3: [],
                            4: [[2,2]]
                            }
        # get real data from file
        real_tazdata = {1:[],2:[], 3:[], 4:[]}
        # income groups 1 to 4
        for i in [1,2,3,4]:
            tazdata_file = open(os.path.join(self.tempdir_path, 'tripgen', 'inputtg', 'tazdata.mf9%s' % i), 'r')
            for a_line in tazdata_file.readlines():
                if a_line[0].isspace():
                    numbers = a_line.split()
                    zone_id = int(numbers[0])
                    job_zone_id = int(numbers[1])
                    real_tazdata[i].append([zone_id, job_zone_id])
                    
        for group in expected_tazdata.keys():
            self.assertEqual(real_tazdata[group], expected_tazdata[group],
                                       "income group %d, columns did not match up."%group)

    def create_households_table(self, database):
        database.drop_table("households")
        schema = {
                  'household_id': 'INTEGER',
                  'zone_id': 'INTEGER',
                  'income': 'INTEGER',
                  'year': 'INTEGER',
                  'building_id': 'INTEGER'
        }
        database.create_table_from_schema('households', schema)
        values = [{'household_id':a, 'zone_id':b, 'income':c, 'year':d, 'building_id':e} for a,b,c,d,e in \
                     [(1, 1, 10, 2000, 1), (2, 1, 11, 2000, 2), (3, 2, 12, 2000, 4), (4, 2, 13, 2000, 4), (5, 2, 14, 2000, 5), (6, 1, 15, 2000, 1), (7, 2, 16, 2000, 5), (8, 2, 16, 2000, 6), (9, 2, 17, 2000, 7)]]
        households = database.get_table('households')
        database.engine.execute(households.insert(), values) 
        # 9 houses total
        #incomes: 10, 11, 12, 13, 14, 15, 16, 16, 17
        # med=14, low_med=11.5, upper_med=16
        # in zone_1: 1,2,6

    def create_persons_table(self, database):
        database.drop_table("persons")
        schema = {
                  'person_id': 'INTEGER',
                  'household_id': 'FLOAT',
                  'job_id': 'INTEGER',
                  'is_worker': 'INTEGER',
                  'work_at_home': 'INTEGER'
        }
        database.create_table_from_schema('persons', schema)
        values = [{'person_id':z, 'household_id':a, 'job_id':b, 'is_worker':c, 'work_at_home':d} for z,a,b,c,d in \
                    [(1, 1, 3, 1, 0), (2, 4, 8, 1, 0), (3, 1, 9, 1, 0), (4, 7, 2, 1, 1), (5, 6, -1, 1, 0), (6, 9, 6, 1, 0), (7, 9, -1, 0, 0), (8, 2, 1, 1, 1), (9, 2, 4, 1, 1)]]

        persons = database.get_table('persons')
        database.engine.execute(persons.insert(), values)
        
    def create_zones_table(self, database):
        database.drop_table('zones')
        schema = {
                  'zone_id': 'INTEGER',
        }
        database.create_table_from_schema('zones', schema)
        
        zones = database.get_table('zones')
        values = [{'zone_id':1}, {'zone_id':2}]
        database.engine.execute(zones.insert(), values)

    def create_employment_sector_groups_table(self, database):
        database.drop_table('employment_sectors')
        schema = {
                  'sector_id': 'INTEGER',
        }
        database.create_table_from_schema('employment_sectors', schema)
        values = [{'sector_id':i} for i in range(1,20)]
        employment_sectors = database.get_table('employment_sectors')
        database.engine.execute(employment_sectors.insert(), values)            
        
        database.drop_table('employment_adhoc_sector_groups')
        schema = {
                  'group_id': 'INTEGER',
                  'name': 'TEXT'
        }
        database.create_table_from_schema('employment_adhoc_sector_groups', schema)
        values = [{'group_id':a, 'name':b} for a,b in [(2, 'retail'), (21, 'manu'), (22, 'wtcu'), (24, 'fires'), (25, 'gov'), (26, 'edu')]]
        employment_sectors = database.get_table('employment_adhoc_sector_groups')
        database.engine.execute(employment_sectors.insert(), values)            

        schema = {
                  'sector_id': 'INTEGER',
                  'group_id': 'INTEGER',
        }            
        database.drop_table('employment_adhoc_sector_group_definitions')
        database.create_table_from_schema('employment_adhoc_sector_group_definitions', schema)
        values = [{'sector_id':a, 'group_id':b} for a,b in [(7, 2), (14, 2), (3,21), (4,21), (5,21), (6,22), (8,22), (9,22), (10,22),  (11,24), (12,24), (13,24), (16,24), (17,24), (18,25), (15,26), (19,26)]]
        employment_sectors = database.get_table('employment_adhoc_sector_group_definitions')
        database.engine.execute(employment_sectors.insert(), values)    
                    
    def create_jobs_table(self, database):
        database.drop_table('jobs')
        schema = {
                  'job_id': 'INTEGER',
                  'zone_id': 'INTEGER',
                  'sector_id': 'INTEGER',
                  'year': 'INTEGER',
        }
        database.create_table_from_schema('jobs', schema)

        values = [{'job_id':1, 'zone_id':1, 'sector_id':1, 'year':2000}, 
                  {'job_id':2, 'zone_id':1, 'sector_id':3, 'year':2000}, 
                  {'job_id':3, 'zone_id':1, 'sector_id':4, 'year':2000}, 
                  {'job_id':4, 'zone_id':1, 'sector_id':7, 'year':2000}, 
                  {'job_id':5, 'zone_id':2, 'sector_id':9, 'year':2000},
                  {'job_id':6, 'zone_id':2, 'sector_id':11, 'year':2000}, 
                  {'job_id':7, 'zone_id':2, 'sector_id':15, 'year':2000}, 
                  {'job_id':8, 'zone_id':2, 'sector_id':16, 'year':2000}, 
                  {'job_id':9, 'zone_id':2, 'sector_id':17, 'year':2000}]
        jobs = database.get_table('jobs')
        database.engine.execute(jobs.insert(), values)

    def create_constant_taz_columns_table(self, database):
        database.drop_table('constant_taz_columns')
        schema = {
                  'TAZ': 'INTEGER',
                  'PCTMF': 'FLOAT',
                  'GQI': 'INTEGER',
                  'GQN': 'INTEGER',
                  'FTEUNIV': 'INTEGER',
                  'DEN': 'INTEGER',
                  'FAZ': 'INTEGER',
                  'YEAR': 'INTEGER',
        }
        database.create_table_from_schema('constant_taz_columns', schema)
        values = [{'TAZ':a, 'PCTMF':b, 'GQI':c, 'GQN':d, 'FTEUNIV':e, 'DEN':f, 'FAZ':g, 'YEAR':h} for a,b,c,d,e,f,g,h in \
                    [(1, 19.9, 3, 11, 42, 1, 1, 2000),(2, 29.9, 1, 3, 241, 2, 2, 2000)]
                  ]
        constant_taz_columns = database.get_table('constant_taz_columns')
        database.engine.execute(constant_taz_columns.insert(), values)
                                                                                   

if __name__ == "__main__":
    opus_unittest.main()