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

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    
    # get parameter values
    database_name = param_dict['database_name']
    database_server_connection = param_dict['database_server_connection']
    households_table_name = param_dict['households_table_name']
    
    query = "DELETE h.* FROM %s AS h WHERE h.persons = '00' IS NULL" % (households_table_name)

    # create engine and connection
    logCB("Openeing database connection\n")
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    opus_db = OpusDatabase(database_server_configuration=dbs_config, database_name=database_name)

    # Do Query       
    logCB("Deleting empty household records...\n")
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