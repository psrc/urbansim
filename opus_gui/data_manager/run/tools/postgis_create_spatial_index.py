# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from sqlalchemy import create_engine, MetaData
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.items():
        param_dict[str(key)] = str(val)
        
    # TODO:
    #    - automatically get geometry column name (probably requires custom type in sqlalchemy)
    #    - more error checking and messages
    
    # get parameter values
    database_name = param_dict['database_name']
    schema = param_dict['schema']
    table_name = param_dict['table_name']
    geometry_column_name = param_dict['geometry_column_name']
    run_vacuum_analyze = param_dict['run_vacuum_analyze']
    index_name = table_name + '_geom_indx'
    database_server_connection = param_dict['database_server_connection']

    # create engine and connection
    logCB("Openeing database connection\n")
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    connection_string = str(dbs_config) + '/%s' % (database_name) 
    engine = create_engine(connection_string)
    connection = engine.connect()
    
    # set up queries
    # drop index if exists
    query1 = '''DROP INDEX IF EXISTS %s.%s;''' % (schema, index_name)
    # create the new index
    query2 = '''CREATE INDEX %s ON %s.%s USING GIST (%s);''' % (index_name, schema, table_name, geometry_column_name)
    
    queries = [query1, query2]
    
    # execute queries
    for query in queries:
        logCB("Running query:\n")
        logCB("%s\n" % query)
        connection.execute(query)
    
    # update database statistics
    if run_vacuum_analyze == 'True':
        logCB("Running vacuum\n")
        import psycopg2.extensions
        connection.connection.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        query = '''VACUUM ANALYZE;'''
        connection.execute(query)
    
    #close connection
    logCB("Closing database connection\n")
    connection.close()
    logCB('Finished creating spatial index on %s\n' % table_name)
    
def opusHelp():
    help = 'This tool will create a spatial index on the geometry column of a PostGIS table.\n' \
           '\n' \
           'database_name: the name of the PostGIS database\n' \
           'schema: the name of the schema inside the PostGIS database that contains the table\n' \
           'table_name: the name of the table to create the spatial index on\n' \
           'geometry_column_name: the name of the geometry column to create the spatial index on\n' \
           'run_vacuum_analyze: True or False, update statistics on the database after spatial index is created'
    return help