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
    pums_id_to_bg_id_file_path = param_dict['pums_id_to_bg_id_file_path']
    database_server_connection = param_dict['database_server_connection']
    database_name = param_dict['database_name']
    
    # set up database server configuration
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)   

    # Main application routine:

    opus_db.execute("""
            CREATE TABLE pums_id_to_bg_id (
              county int,
              tract int,
              bg int,
              puma5 int,
              tract_string text,
              number_of_digits int);
            """)
    
    opus_db.execute("""
            LOAD DATA LOCAL INFILE '%s' INTO TABLE pums_id_to_bg_id
            FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
            """ % (pums_id_to_bg_id_file_path))
    
    opus_db.execute("""
            update pums_id_to_bg_id
            set tract_string = tract;
    """)
    
    opus_db.execute("""
            update pums_id_to_bg_id
            set number_of_digits = length(tract_string);
    """)

    opus_db.execute("""
            update pums_id_to_bg_id
            set tract = tract*100
            where number_of_digits <= 3;
    """)

    progressCB(90)
    logCB("Closing database connection...\n")
    opus_db.close()
    logCB('Finished running queries.\n')
    progressCB(100)
    
def opusHelp():
    help = 'This tool will import the data necessary to add a PUMA id to the marginals tables.\n' \
           '\n' \
           'You will need to download a geographic correspondence table for your state from the \n' \
           'Missouri Census Data Center at http://mcdc2.missouri.edu/websas/geocorr2k.html \n' \
           '\n' \
           'Simply choose your state, Census Block Group 2000 for the source, PUMA for 5% samples for \n' \
           'the TARGET and leave all other options on their default values, then click "Run Request", \n' \
           'and download the resulting .csv file.\n' \
           'You will use the .csv file as the input to the pums_id_to_bg_id_file_path parameter in this tool.\n' \
           '\n' \
           'You will also need to remove the field names (first two lines) from the .csv file, and also \n' \
           'do a "find and replace" on the decimal point an replace it with nothing.  The block group ids \n' \
           'should not have any decimal points in them when imported into the database.\n' \
           '\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - download a geographic correspondence table from the instructions above\n' \
           '\n'
    return help 