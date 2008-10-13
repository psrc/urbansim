#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import time
from synthesizer.raw_pums_data_processor import raw_pums_data_processor
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # get parameter values
    create_hh_table = param_dict['create_hh_table']
    pums_hh_table_name = param_dict['pums_hh_table_name']
    insert_hh_records = param_dict['insert_hh_records']
    create_pp_table = param_dict['create_pp_table']
    pums_pp_table_name = param_dict['pums_pp_table_name']
    insert_pp_records = param_dict['insert_pp_records']
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
    if create_hh_table == 'y':
        logCB('Creating PUMS households table...\n')
        pums.create_hh_table(pums_hh_table_name)
        progressCB(3)
    if create_pp_table == 'y':
        logCB('Creating PUMS persons table...\n')
        pums.create_pp_table(pums_pp_table_name)
        progressCB(50)
    if insert_hh_records == 'y':
        logCB('Inserting household records...\n')
        pums.insert_hh_records(pums_hh_table_name, raw_pums_file_path)
        progressCB(53)
    if insert_pp_records == 'y':
        logCB('Inserting person records...\n')
        pums.insert_pp_records(pums_pp_table_name, raw_pums_file_path)
        progressCB(100)
    logCB('Operation lasted %f minutes\n'%((time.time() - start)/60))
    