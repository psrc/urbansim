# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys, re
from opus_core.export_storage import ExportStorage
from opus_core.store.sql_storage import sql_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer
from opus_core import paths
from opus_core.misc import create_list_string

def opusRun(progressCB,logCB,params):

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    opus_data_directory = params_dict['opus_data_directory']
    opus_data_directory = paths.prepend_opus_home_if_relative(opus_data_directory)
    opus_data_year = params_dict['opus_data_year']
    database_name = params_dict['database_name']
    table_name = params_dict['table_name']
    database_server_connection = params_dict['database_server_connection']
    
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opusdb = server.get_database(database_name=database_name, create_if_doesnt_exist=False)
    
    input_storage = sql_storage(storage_location = opusdb)

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
    SimulationState().set_current_time(opus_data_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    if table_name == 'ALL':
        lst = input_storage.get_table_names()
    else:
        lst = re.split(' +', table_name.strip())
        
    lst_out = create_list_string(lst, ', ')

    logCB('caching tables:\n%s\n' % lst_out)
        
    for i in lst:
        logCB("Exporting table '%s' to year %s of cache located at %s...\n" %
                   (i, opus_data_year, opus_data_directory))
        ExportStorage().export_dataset(
            dataset_name = i,
            in_storage = input_storage,
            out_storage = output_storage,
        )

    logCB('successfully cached tables:\n%s\n' % lst_out)

def opusHelp():
    help = 'This tool will get a table from a SQL database and export it to the OPUS cache format.\n' \
           '\n' \
           'opus_data_directory: path to the OPUS data directory (full path, e.g., c:\\opus\\data\\seattle_parcel\\base_year_data, or relative to OPUS_HOME)\n' \
           'opus_data_year: the year to which the data should be exported (2000)\n' \
           'database_name: the name of the database (or PostgreSQL schema) that contains the table\n' \
           'table_name: the name of the tables to be exported, separated by spaces. ALL imports all tables\n'
    return help
