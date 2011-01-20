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
    raw_sf3_data_table_name = 'raw_sf3_data'

    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)   
    
    logCB(" ***  WARNING *** \n")
    logCB(" *** At the end of this tool, you will need\n")
    logCB(" *** to check to make sure each record in the 'person_marginals'\n")
    logCB(" *** table has a proper 'pumano' assigned to it.  You may need to \n")
    logCB(" *** manually update the 'pumano' for each \n")
    logCB(" *** block group that this set of queries was \n")
    logCB(" *** unable to match up properly due to idiosyncrasies\n")
    logCB(" *** in the way that block group ids are recorded\n")
    logCB(" *** in the original source files.\n")
    
    opus_db.execute("""
            drop table if exists person_marginals;
            """)
    progressCB(50)    
    logCB("Creating person_marginals table...\n")
    opus_db.execute("""
        CREATE TABLE person_marginals
        SELECT
          mid(GEO_ID, 8, 5) as county,
          0 as pumano,
          cast(mid(GEO_ID, 13, 6) as unsigned) as tract,
          cast(right(GEO_ID, 1) as unsigned) as bg,
          P008002 as gender1,
          P008041 as gender2,
          P008003+P008004+P008005+P008006+P008007+P008042+P008043+P008044+P008045+P008046 as age1,
          P008008+P008009+P008010+P008011+P008012+P008013+P008014+P008015+P008016+P008017+P008047+P008048+P008049+P008050+P008051+P008052+P008053+P008054+P008055+P008056 as age2,
          P008018+P008019+P008020+P008021+P008022+P008023+P008024+P008025+P008057+P008058+P008059+P008060+P008061+P008062+P008063+P008064 as age3,
          P008026+P008027+P008065+P008066 as age4,
          P008028+P008029+P008067+P008068 as age5,
          P008030+P008031+P008069+P008070 as age6,
          P008032+P008033+P008034+P008071+P008072+P008073 as age7,
          P008035+P008036+P008037+P008074+P008075+P008076 as age8,
          P008038+P008039+P008077+P008078 as age9,
          P008040+P008079 as age10,
          P006002 as race1,
          P006003 as race2,
          P006004 as race3,
          P006005 as race4,
          P006006 as race5,
          P006007 as race6,
          P006008 as race7,
          P008003+P008004+P008005+P008006+P008007+P008008+P008009+P008010+P008011+P008012+P008013+P008014+P008015+P008016+P008017+P008018+P008042+P008043+P008044+P008045+P008046+P008047+P008048+P008049+P008050+P008051+P008052+P008053+P008054+P008055+P008056+P008057 as employment1,
          P043004+P043006+P043011+P043013 as employment2,
          P043007+P043014 as employment3,
          P043008+P043015 as employment4
        from raw_sf3_data;
    """)
    
    logCB("Updating PUMA identifier...\n")
    opus_db.execute("""
            UPDATE person_marginals h, pums_id_to_bg_id p
            SET h.pumano = p.puma5
            WHERE h.county = p.county AND h.tract = p.tract AND h.bg = p.bg;
    """)

    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)
    
def opusHelp():
    help = 'This tool will create the person marginals table necessary to\n' \
           'run the synthesizer algorithm.\n' \
           '\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - run the import_sf3_raw_data_to_db tool\n' \
           ' - run the import_pums_id_to_bg_id_to_db tool\n' \
           '\n'
    return help 