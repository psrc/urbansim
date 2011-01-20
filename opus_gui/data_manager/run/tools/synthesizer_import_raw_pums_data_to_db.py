# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import time
from synthesizer.raw_pums_data_processor import raw_pums_data_processor
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # get parameter values

    pums_hh_table_name = 'raw_pums_hh_data'
    pums_pp_table_name = 'raw_pums_pp_data'
    raw_pums_file_path = param_dict['raw_pums_file_path']
    database_server_connection = param_dict['database_server_connection']
    database_name = param_dict['database_name']
    
    # set up database server configuration
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    hostname = dbs_config.host_name
    username = dbs_config.user_name
    password = dbs_config.password
    db_type = dbs_config.protocol

    # Main application routine:
    start = time.time()
    pums = raw_pums_data_processor(username, password, hostname, database_name, db_type, raw_pums_file_path)

    logCB('Creating PUMS households table...\n')
    pums.create_hh_table(pums_hh_table_name)
    progressCB(3)
    logCB('Creating PUMS persons table...\n')
    pums.create_pp_table(pums_pp_table_name)
    progressCB(50)
    logCB('Inserting household records...\n')
    pums.insert_hh_records(pums_hh_table_name, raw_pums_file_path)
    progressCB(53)
    logCB('Inserting person records...\n')
    pums.insert_pp_records(pums_pp_table_name, raw_pums_file_path)
    progressCB(100)
    logCB('Operation lasted %f minutes\n'%((time.time() - start)/60))


def opusHelp():
    help = 'This tool will import the raw ASCII PUMS data to your database.\n' \
           '\n' \
           'Go to http://www2.census.gov/census_2000/datasets/PUMS/FivePercent/\n' \
           'and download the large ASCII file from your respective state.\n' \
           'and use it as the input to the "raw_pums_file_path" parameter in this tool.\n' \
           'PREREQUISITE TO RUNNING THIS TOOL:\n' \
           ' - download raw PUMS ASCII data from the above website.\n' \
           '\n'
    return help
