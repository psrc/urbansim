# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


import os, sys, string
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer
from random import Random

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    
    # get parameter values
    database_name = param_dict['database_name']
    database_server_connection = param_dict['database_server_connection']
    raw_pums_persons_table_name = 'raw_pums_pp_data'
    raw_pums_households_table_name = 'raw_pums_hh_data'
    
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)   
    
    logCB("Creating temporary table pp_temp...\n")
    
    opus_db.execute("""
            drop table if exists pp_temp;
            """)
    opus_db.execute("""
            create table pp_temp
            select
            0 as pumano,
            SERIALNO, 0 as hhpumsid,
            0 as hhid,
            PNUM, 0 as personid,
            SEX, 0 as gender,
            AGE as AGE_PUMS, 0 as age,
            NUMRACE,
            WHITE,
            BLACK,
            AIAN,
            ASIAN,
            NHPI,
            OTHER,
            0 as race,
            ESR, 0 as employment
            from %s;
            """ % (raw_pums_persons_table_name))
    progressCB(5)
    
    logCB("Updating values...\n")

    index_name = get_random_index_name()
    opus_db.execute("""
            alter table pp_temp add index %s(SERIALNO);    
                    """ % (index_name))

    opus_db.execute("""
            update pp_temp as p, raw_pums_hh_data as h
            set p.pumano = h.PUMA5
            where p.SERIALNO = h.SERIALNO;
            """)

    opus_db.execute("""
            update pp_temp
            set hhpumsid = SERIALNO;
            """)
    index_name = get_random_index_name()

    opus_db.execute("""
            alter table pp_temp add index %s(hhpumsid);
            """ % (index_name))
    index_name = get_random_index_name()

    opus_db.execute("""
            alter table housing_pums add index %s(hhpumsid);
            """ % (index_name))

    opus_db.execute("""
            update pp_temp as p, housing_pums as h
            set p.hhid = h.hhid
            where p.hhpumsid = h.hhpumsid; 
            """)

    opus_db.execute("""
            update pp_temp
            set personid = PNUM;
            """)

    opus_db.execute("""
            update pp_temp
            set gender = SEX;
            """)

    opus_db.execute("""
            update pp_temp
            set age = AGE_PUMS;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 1
            where WHITE = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 2
            where BLACK = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 3
            where AIAN = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 4
            where ASIAN = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 5
            where NHPI = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 6
            where OTHER = 1;
            """)

    opus_db.execute("""
            update pp_temp
            set race = 7
            where NUMRACE > 1;
            """)

    opus_db.execute("""
            update pp_temp
            set employment = 1
            where ESR = '0';
            """)

    opus_db.execute("""
            update pp_temp
            set employment = 2
            where ESR='1' OR ESR='2' OR ESR='4' OR ESR='5';
            """)

    opus_db.execute("""
            update pp_temp
            set employment = 3
            where ESR = '3';
            """)

    opus_db.execute("""
            update pp_temp
            set employment = 4
            where ESR = '6';
            """)

    opus_db.execute("""
            drop table if exists person_pums;
            """)

    opus_db.execute("""
            create table person_pums
            select
            pumano,
            hhpumsid,
            hhid,
            personid,
            gender,
            age,
            race,
            employment
            from pp_temp;
            """)

    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)

def get_random_index_name():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return 'indx_' + ''.join(Random().sample(letters, 8))

def opusHelp():
    help = 'This tool will create the persons table necessary to run\n' \
           'the synthesizer algorithm.\n' \
           '\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - run the import_raw_pums_data_to_db tool\n' \
           ' - run the delete_empty_households_from_raw_pums_data tool\n' \
           '\n'
    return help    