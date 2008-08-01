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

import os, sys, subprocess
from opus_gui.exceptions.formatter import formatExceptionInfo
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
    
    # get parameter values
    host = os.environ['POSTGRESHOSTNAME']
    user = os.environ['POSTGRESUSERNAME']
    password = os.environ['POSTGRESPASSWORD']
    dbname = param_dict['dbname']
    shapefile = param_dict['shapefile_path']
    schema = param_dict['schema_name']
    overwrite = param_dict['overwrite']
    table_name = param_dict['output_table_name']
    geometry_type = param_dict['geometry_type']
    
    # check for presence of ogr2ogr
    try:
        p = subprocess.Popen('ogr2ogr', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_text, stderr_text = p.communicate()
    except WindowsError:
        print 'ogr2ogr is not properly installed or configured'
        return

    # check to see if shapefile exists
    if not os.path.isfile(shapefile):
        print 'shapefile does not exist'
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
   
    print '------------'                
    print ogr2ogr_cmd
    print '------------'
    
    # execute full command
    p = subprocess.Popen((ogr2ogr_cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_text, stderr_text = p.communicate()
    
    # print messages from ogr2ogr
    if stdout_text:
        print 'stdout from ogr2ogr:'
        print stdout_text
    if stderr_text:
        print 'stderr from ogr2ogr:'
        print stderr_text

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
    dbserverconfig = DatabaseServerConfiguration(protocol='postgres')
    db = OpusDatabase(dbserverconfig, dbname)
    query = 'DROP TABLE %s.%s' % (schema, table_name)
    try:
        db.DoQuery(query)
        print 'DROPPED TABLE %s' % table_name
    except:
        return
    