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

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # get parameter values
    pums_id_to_bg_id_file_path = param_dict['pums_id_to_bg_id_file_path']
    database_server_connection = param_dict['database_server_connection']
    database_name = param_dict['database_name']
    
    # set up database server configuration
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    opus_db = OpusDatabase(database_server_configuration=dbs_config, database_name=database_name)

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