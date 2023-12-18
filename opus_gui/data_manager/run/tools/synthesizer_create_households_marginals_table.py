# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.items():
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
    logCB(" *** to check to make sure each record in the 'housing_marginals'\n")
    logCB(" *** table has a proper 'pumano' assigned to it.  You may need to \n")
    logCB(" *** manually update the 'pumano' for each \n")
    logCB(" *** block group that this set of queries was \n")
    logCB(" *** unable to match up properly due to idiosyncrasies\n")
    logCB(" *** in the way that block group ids are recorded\n")
    logCB(" *** in the original source files.\n")
    
    opus_db.execute("""
            drop table if exists housing_marginals;
            """)
    progressCB(50)
    logCB("Creating housing_marginals table...\n")
    opus_db.execute("""
            CREATE TABLE housing_marginals
            SELECT
              mid(GEO_ID, 8, 5) as county,
              0 as pumano,
              cast(mid(GEO_ID, 13, 6) as unsigned) as tract,
              cast(right(GEO_ID, 1) as unsigned) as bg,
              P010001 as hhtotal,
              P010008 + P010012 + P010015 as childpresence1,
              P010009 + P010013 + P010016 + P010017 + P010002 as childpresence2,
              P010007 as hhldtype1,
              P010011 as hhldtype2,
              P010014 as hhldtype3,
              P010002 as hhldtype4,
              P010017 as hhldtype5,
              P014010 as hhldsize1,
              P014003+P014011 as hhldsize2,
              P014004+P014012 as hhldsize3,
              P014005+P014013 as hhldsize4,
              P014006+P014014 as hhldsize5,
              P014007+P014015 as hhldsize6,
              P014008+P014016 as hhldsize7,
              P052002 + P052003 as hhldinc1,
              P052004 + P052005 as hhldinc2,
              P052006 + P052007 as hhldinc3,
              P052008 + P052009 as hhldinc4,
              P052010 + P052011 as hhldinc5,
              P052012 + P052013 as hhldinc6,
              P052014 + P052015 as hhldinc7,
              P052016 + P052017 as hhldinc8,
              P009026 as groupquarter1,
              P009027 as groupquarter2
            FROM raw_sf3_data;
    """)
    
    logCB("Updating PUMA identifier...\n")
    opus_db.execute("""
            UPDATE housing_marginals h, pums_id_to_bg_id p
            SET h.pumano = p.puma5
            WHERE h.county = p.county AND h.tract = p.tract AND h.bg = p.bg;
    """)

    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)
    
def opusHelp():
    help = 'This tool will create the housing marginals table necessary to\n' \
           'run the synthesizer algorithm.\n' \
           '\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - run the import_sf3_raw_data_to_db tool\n' \
           ' - run the import_pums_id_to_bg_id_to_db tool\n' \
           '\n'
    return help 