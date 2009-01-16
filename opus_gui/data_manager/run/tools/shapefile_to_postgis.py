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

import os, sys, subprocess
from opus_core.database_management.configurations.indicators_database_configuration import IndicatorsDatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # TODO - 
    #    - add 'append' option
    #    - add 'sql statement' option
    
    # get parameter values
    dbname = param_dict['dbname']
    shapefile = param_dict['shapefile_path']
    schema = param_dict['schema_name']
    overwrite = param_dict['overwrite']
    table_name = param_dict['output_table_name']
    geometry_type = param_dict['geometry_type']
    database_server_connection = param_dict['database_server_connection']
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    host = dbs_config.host_name
    user = dbs_config.user_name
    password = dbs_config.password
    
    # check for presence of ogr2ogr
    try:
        p = subprocess.Popen('ogr2ogr', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_text, stderr_text = p.communicate()
    except:
        logCB('ogr2ogr is not properly installed or configured\n')
        return

    # check to see if shapefile exists
    if not os.path.isfile(shapefile):
        logCB('shapefile does not exist\n')
        return
    
    # set proper table name and schema
    if table_name == 'default':
        table_name = os.path.split(shapefile)[1].split('.')[0]
    if schema == 'default':
        schema = 'public'    
        
    # delete existing table if overwrite = YES
    if overwrite == 'YES':
        drop_table(table_name, dbname, schema)
    
    # set up base command
    base_cmd = 'ogr2ogr -f PostgreSQL PG:"host=%s user=%s dbname=%s password=%s" %s' \
                % (host, user, dbname, password, shapefile)
    # add switches to base command
    ogr2ogr_cmd = base_cmd + get_lco_options() + get_nln_option(schema, table_name) + get_nlt_option(geometry_type) #+ ' -a_srs EPSG:32148' 
   
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
    
    logCB('Finished exporting shapefile to %s.%s' % (dbname, schema))

def get_lco_options():
    precision = ' PRECISION=NO'
    lco_options = ' -lco' + precision
    return lco_options

def get_nln_option(schema, table_name):
    nln_option = ' -nln ' + schema + '.' + table_name
    return nln_option

def get_nlt_option(geometry_type):
    if geometry_type == 'default':
        nlt_option = ''
    else:
        nlt_option = ' -nlt ' + geometry_type
    return nlt_option

def drop_table(table_name, dbname, schema):
    dbserverconfig = IndicatorsDatabaseConfiguration(protocol='postgres')
    server = DatabaseServer(database_server_configuration = dbserverconfig)
    db = server.get_database(database_name=dbname)
    query = 'DROP TABLE %s.%s' % (schema, table_name)
    try:
        db.execute(query)
        logCB('DROPPED TABLE %s \n' % table_name)
    except:
        return

def opusHelp():
    help = 'This tool will export a shapefile to a PostGIS database using ogr2ogr.exe.  You must' \
           'have ogr2ogr.exe in your system PATH for this tool to work.\n' \
           '\n' \
           'dbname: the name of the PostGIS database to export to\n' \
           'shapefile_path: the full path to the shapefile to export (c:\\temp\\test.shp)\n' \
           'schema_name: the name of the schema in the PostGIS database to export to\n' \
           'overwrite: YES or NO, attempts to overwrite an existing table\n' \
           'output_table_name: the name of the table to be created in the database\n' \
           'geometry_type: the type of geometry to be created (NONE, GEOMETRY, POINT, LINESTRING, POLYGON, GEOMETRYCOLLECTION, MULTIPOINT, MULTILINE, MULTIPOLYGON, MULTILINESTRING)'
    return help
    