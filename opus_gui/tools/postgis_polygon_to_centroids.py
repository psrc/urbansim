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
from sqlalchemy import create_engine, MetaData

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    # TODO:
    #    - automatically get geometry column name (probably requires custom type in sqlalchemy)
    #    - more error checking and messages
    #    - get all columns?
    #    - set constraint on new primary_key column instead of just naming it oid
    
    # get parameter values
    username = os.environ['POSTGRESUSERNAME']
    password = os.environ['POSTGRESPASSWORD']
    hostname = os.environ['POSTGRESHOSTNAME']
    database_name = 'jesse_test_spatial_db'
    drop_existing = param_dict['drop_existing']
    schema = param_dict['schema']
    new_table_name = param_dict['new_table_name']
    geometry_field_name = param_dict['geometry_field_name']
    existing_table_name = param_dict['existing_table_name']
    centroid_inside_polygon = param_dict['centroid_inside_polygon']
    
    # build connection string
    connection_string = 'postgres://%s:%s@%s/%s' % (
            username,
            password,
            hostname,
            database_name
            )
       
    # create engine and connection
    engine = create_engine(connection_string)
    connection = engine.connect()
    metadata = MetaData()
    metadata.bind = engine
    metadata.reflect(schema=schema)
    
    # get primary key
    primary_key_name = get_primary_key(metadata, schema, existing_table_name)  
    
    # drop existing table
    if drop_existing == 'True':
        print 'ATTEMPTING TO DROP TABLE'
        drop_table(new_table_name, schema, connection)
            
    # force centroid inside polygon
    if centroid_inside_polygon == 'True':
        centroid_function = 'ST_PointOnSurface'
    else:
        centroid_function = 'ST_Centroid'    
  
    # set up query
    query = '''CREATE TABLE %s.%s as
    SELECT %s as oid, %s(%s) as wkb_geometry from %s.%s;
            ''' % (
                   schema,
                   new_table_name,
                   primary_key_name,
                   centroid_function,
                   geometry_field_name,
                   schema,
                   existing_table_name
                   )

    # execute query
    print query
    connection.execute(query)
    connection.close()
    
def drop_table(new_table_name, schema, connection):
    query = 'DROP TABLE IF EXISTS %s.%s;' % (schema, new_table_name)
    try:
        connection.execute(query)
        print 'DROPPED TABLE %s' % new_table_name
    except:
        return

def get_primary_key(metadata, schema, existing_table_name):
    tbl = metadata.tables['%s.%s' % (schema, existing_table_name)]
    for i in tbl.c:
        if i.primary_key:
            primary_key_name = i.name
            return primary_key_name