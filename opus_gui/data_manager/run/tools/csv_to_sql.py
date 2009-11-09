# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys, subprocess
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration


    
def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # TODO - 
    #    - add 'where' option
    #    - add 'select' option
    #    - add 'overwrite' option
    
    # get parameter values
    database_name = param_dict['database_name']
    csv_file_path = param_dict['csv_file_path']
    output_table_name = param_dict['output_table_name']
    database_server_connection = param_dict['database_server_connection']
    overwrite = param_dict['overwrite']
    
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    host = dbs_config.host_name
    user = dbs_config.user_name
    password = dbs_config.password
    protocol = dbs_config.protocol
    
    # check for presence of ogr2ogr
    try:
        p = subprocess.Popen('ogr2ogr', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_text, stderr_text = p.communicate()
    except:
        logCB('ogr2ogr is not properly installed or configured\n')
        return

    # check to see if csv file exists
    if not os.path.isfile(csv_file_path):
        logCB('csv file does not exist\n')
        return
    
    # set proper table name
    if output_table_name == '':
        output_table_name = os.path.split(csv_file_path)[1].split('.')[0]
        
    # delete existing table if overwrite = YES
    if overwrite == 'True':
        logCB('dropping table %s' % output_table_name)
        drop_table(dbs_config, database_name, output_table_name)
    
    # set up base command
    if protocol == 'mysql':
        ogr2ogr_cmd = 'ogr2ogr -f MySQL MYSQL:"%s,host=%s,user=%s,password=%s" %s' \
                    % (database_name, host, user, password, csv_file_path)
    elif protocol == 'postgres':
        ogr2ogr_cmd = 'ogr2ogr -f PostgreSQL PG:"host=%s user=%s dbname=%s password=%s" %s' \
                    % (host, user, database_name, password, csv_file_path)
    else:
        logCB('A database other than MySQL or PostgreSQL was specified')
        return
    
    # add switches to ogr2ogr_cmd command
    # check for output_table_name
    if output_table_name != '':
        ogr2ogr_cmd = ogr2ogr_cmd + get_nln_option(output_table_name)
       
    logCB('Running ogr2ogr using: \n')          
    logCB(ogr2ogr_cmd + '\n')
    
    # execute full command
    p = subprocess.Popen((ogr2ogr_cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_text, stderr_text = p.communicate()
    
    # print messages from ogr2ogr
    if stdout_text:
        logCB('stdout from ogr2ogr: \n') 
        logCB(stdout_text + '\n')
    if stderr_text:
        logCB('stderr from ogr2ogr: \n')
        logCB(stderr_text + '\n')
    
    logCB('Finished exporting csv file to %s' % database_name)

def get_nln_option(table_name):
    nln_option = ' -nln ' + table_name
    return nln_option

def drop_table(dbs_config, database_name, output_table_name):
    server = DatabaseServer(database_server_configuration=dbs_config)
    db = server.get_database(database_name = database_name)
    print db.database_name
    db.drop_table(output_table_name)

def opusHelp():
    help = 'This tool will export a csv file to a PostgreSQL or MySQL database using ogr2ogr.exe.  You must' \
           'have ogr2ogr.exe in your system PATH for this tool to work.\n' \
           '\n' \
           'dbname: the name of the PostgreSQL or MySQL database to export to\n' \
           'csv_file_path: the full path to the csv file to export (c:\\temp\\test.csv)\n' \
           'overwrite: YES or NO, attempts to overwrite an existing table\n' \
           'output_table_name: the name of the table to be created in the database\n' \
           'database_server_connection: the name of a configured database server connection'
    return help
