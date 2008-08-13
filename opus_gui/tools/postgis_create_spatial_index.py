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
from sqlalchemy import create_engine, MetaData

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    # TODO:
    #    - automatically get geometry column name (probably requires custom type in sqlalchemy)
    #    - more error checking and messages
    
    # get parameter values
    username = os.environ['POSTGRESUSERNAME']
    password = os.environ['POSTGRESPASSWORD']
    hostname = os.environ['POSTGRESHOSTNAME']
    database_name = param_dict['database_name']
    schema = param_dict['schema']
    table_name = param_dict['table_name']
    geometry_column_name = param_dict['geometry_column_name']
    run_vacuum_analyze = param_dict['run_vacuum_analyze']
    
    index_name = table_name + '_geom_indx'


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
    
    # set up queries
    # drop index if exists
    query1 = '''DROP INDEX IF EXISTS %s.%s;''' % (schema, index_name)
    # create the new index
    query2 = '''CREATE INDEX %s ON %s.%s USING GIST (%s);''' % (index_name, schema, table_name, geometry_column_name)
    
    queries = [query1, query2]
    
    # execute queries
    for query in queries:
        connection.execute(query)
    
    # update database statistics
    if run_vacuum_analyze == 'True':
        print "running vacuum"
        import psycopg2.extensions
        connection.connection.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        query = '''VACUUM ANALYZE;'''
        connection.execute(query)
    
    #close connection
    connection.close()