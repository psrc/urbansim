# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    
    # get parameter values
    database_name = param_dict['database_name']
    database_server_connection = param_dict['database_server_connection']
    raw_pums_households_table_name = 'raw_pums_hh_data'

    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)
        
    logCB("Creating temporary table hh_temp...\n")
    
    opus_db.execute("""
            drop table if exists hh_temp;
            """)
    opus_db.execute("""
            create table hh_temp
            select PUMA5, 0 as pumano,
                   SERIALNO, 0 as hhpumsid,
                   UNITTYPE, 0 as hhtype,
                   NOC, 0 as childpresence,
                   HHT, 0 as hhldtype,
                   PERSONS, 0 as hhldsize,
                   HINC, 0 as hhldinc,
                   0 as groupquarter
            from %s;
            """ % (raw_pums_households_table_name))
    progressCB(5)
    logCB("Updating values...\n")
    opus_db.execute("""
            update hh_temp
            set pumano = PUMA5,
            hhpumsid = SERIALNO;
            """)
    opus_db.execute("""        
            update hh_temp
            set hhtype = 1
            where UNITTYPE = 0;
            """)
    opus_db.execute("""
            update hh_temp
            set hhtype = 2
            where UNITTYPE = 1 or UNITTYPE = 2;
            """)
    opus_db.execute("""        
            update hh_temp
            set childpresence = 1
            where NOC <> '00';
            """)    
    opus_db.execute("""        
            update hh_temp
            set childpresence = 2
            where NOC = '00';
            """)            
    opus_db.execute("""
            update hh_temp
            set childpresence = -99
            where hhtype = 2;
            """)
    opus_db.execute("""         
            update hh_temp
            set hhldtype = 1
            where HHT = 1;
            """)
    opus_db.execute("""
            update hh_temp
            set hhldtype = 2
            where HHT = 2;
            """)
    opus_db.execute("""        
            update hh_temp
            set hhldtype = 3
            where HHT = 3;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldtype = 4
            where HHT = 4 or HHT = 6;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldtype = 5
            where HHT = 5 or HHT = 7;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldtype = -99
            where hhtype = 2;
            """)            
    opus_db.execute("""
            update hh_temp
            set hhldsize = 1
            where persons = '01';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 2
            where persons = '02';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 3
            where persons = '03';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 4
            where persons = '04';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 5
            where persons = '05';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 6
            where persons = '06';
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = 7
            where cast(persons as signed) >= 7;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldsize = -99
            where hhtype = 2;
            """)           
    opus_db.execute("""    
            update hh_temp
            set hhldinc = 1
            where cast(HINC as signed) <= 14999;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 2
            where (cast(HINC as signed) >= 15000) AND (cast(HINC as signed) <= 24999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 3
            where (cast(HINC as signed) >= 25000) AND (cast(HINC as signed) <= 34999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 4
            where (cast(HINC as signed) >= 35000) AND (cast(HINC as signed) <= 44999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 5
            where (cast(HINC as signed) >= 45000) AND (cast(HINC as signed) <= 59999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 6
            where (cast(HINC as signed) >= 60000) AND (cast(HINC as signed) <= 99999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 7
            where (cast(HINC as signed) >= 100000) AND (cast(HINC as signed) <= 149999);
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = 8
            where cast(HINC as signed) >= 150000;
            """)
    opus_db.execute("""            
            update hh_temp
            set hhldinc = -99
            where hhtype = 2;
            """)
    opus_db.execute("""
            update hh_temp
            set groupquarter = 1
            where UNITTYPE = 1;
            """)
    opus_db.execute("""            
            update hh_temp
            set groupquarter = 2
            where UNITTYPE = 2;
            """)
    opus_db.execute("""            
            update hh_temp
            set groupquarter = -99
            where UNITTYPE = 0;
            """)
    progressCB(75)
    logCB("Creating 'housing_pums' table for synthesizer...\n")
    opus_db.execute("""
            drop table if exists housing_pums;
            """)
    opus_db.execute("""
            create table housing_pums
            select pumano, hhpumsid,hhtype, childpresence, hhldtype, hhldsize, hhldinc, groupquarter
            from hh_temp;
            """)
    opus_db.execute("""            
            ALTER TABLE housing_pums ADD COLUMN hhid INTEGER NOT NULL AUTO_INCREMENT AFTER hhpumsid, add primary key (hhid);
            """)
    
    hhld_variables = 'childpresence, hhldtype, hhldsize, hhldinc'
    gq_variables = 'groupquarter'
    opus_db.execute('''create table hhld_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 1'''%(hhld_variables))
    opus_db.execute('''create table gq_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 2'''%(gq_variables))

    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)
    
def opusHelp():
    help = 'This tool will create the households table necessary to run\n' \
           'the synthesizer algorithm.\n' \
           '\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - run the import_raw_pums_data_to_db tool\n' \
           ' - run the delete_empty_households_from_raw_pums_data tool\n' \
           '\n'
    return help    