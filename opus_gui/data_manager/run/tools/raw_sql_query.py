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
    query = param_dict['query']

    # create engine and connection
    logCB("Openeing database connection\n")
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opus_db = server.get_database(database_name=database_name)
    
    # Do Query
    logCB("Running Query...\n")
    opus_db.execute(query)
    
    # Finish up
    logCB("Closing database connection\n")
    opus_db.close()
    logCB('Finished running query\n')
    
def opusHelp():
    help = 'This tool will execute a raw SQL query on a database connection.\n' \
           '\n' \
           'database_name: the name of the database or Postgres schema\n' \
           'query: The SQL query to run'
    return help