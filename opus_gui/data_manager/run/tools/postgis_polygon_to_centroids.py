# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys, subprocess
from sqlalchemy import create_engine, MetaData
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

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

    database_name = param_dict['database_name']
    drop_existing = param_dict['drop_existing']
    schema = param_dict['schema']
    new_table_name = param_dict['new_table_name']
    geometry_field_name = param_dict['geometry_field_name']
    existing_table_name = param_dict['existing_table_name']
    centroid_inside_polygon = param_dict['centroid_inside_polygon']
    database_server_connection = param_dict['database_server_connection']
    
    # create engine and connection
    logCB("Openeing database connection\n")
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    connection_string = str(dbs_config) + '/%s' % (database_name) 
    engine = create_engine(connection_string)
    connection = engine.connect()
    
    metadata = MetaData()
    metadata.bind = engine
    metadata.reflect(schema=schema)    

    # get primary key
    primary_key_name = get_primary_key(metadata, schema, existing_table_name)  
    
    # drop existing table
    if drop_existing == 'True':
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
    logCB(query + '\n')
    connection.execute(query)
    connection.close()
    logCB('Finished creating %s\n' % new_table_name)
    
def drop_table(new_table_name, schema, connection):
    query = 'DROP TABLE IF EXISTS %s.%s;' % (schema, new_table_name)
    try:
        connection.execute(query)
        logCB('DROPPED TABLE %s\n' % new_table_name)
    except:
        return

def get_primary_key(metadata, schema, existing_table_name):
    tbl = metadata.tables['%s.%s' % (schema, existing_table_name)]
    for i in tbl.c:
        if i.primary_key:
            primary_key_name = i.name
            return primary_key_name
        
def opusHelp():
    help = 'This tool takes a PostGIS polygon layer and converts the geometry to centroid points as a new layer.\n' \
           '\n' \
           'database_name: the working database name\n' \
           'drop_existing: will attempt to delete the new_table_name if it already exists (True or False, default: False)\n' \
           'schema: the working schema name\n' \
           'new_table_name: the name of the new table to be created\n' \
           'geometry_field_name: specify the name of the geometry field (optional, default: wkb_geometry)\n' \
           'existing_table_name: name of existing table to be converted to centroids\n' \
           'centroid_inside_polygon: force centroid inside polygon (True or False, default: False)\n'                      
    return help
    