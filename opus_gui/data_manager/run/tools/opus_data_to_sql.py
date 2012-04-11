# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.export_storage import ExportStorage
from opus_core.store.sql_storage import sql_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.database_server import DatabaseServer

def opusRun(progressCB,logCB,params):
    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    database_name = params_dict['database_name']
    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']
    opus_table_name = params_dict['opus_table_name']
    
    database_server_connection = params_dict['database_server_connection']
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    server = DatabaseServer(database_server_configuration = dbs_config)
    opusdb = server.get_database(database_name=database_name)

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    attribute_cache_years = [int(year) for year in os.listdir(opus_data_directory) if year.isdigit() and len(year) == 4]
    if opus_data_year != 'ALL':
        attribute_cache_years = [opus_data_year]

    for year in attribute_cache_years:
        #input_storage = sql_storage(storage_location = opusdb)
        input_storage = attribute_cache.get_flt_storage_for_year(year)
        #output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
        if opus_data_year == 'ALL':
            opusdb = server.get_database(database_name=database_name+"_"+str(year))
        output_storage = sql_storage(storage_location = opusdb)
        SimulationState().set_current_time(year)
        SessionConfiguration(new_instance=True,
                             package_order=[],
                             in_storage=AttributeCache())
        
        if opus_table_name != 'ALL':
            opus_table_name_list = [opus_table_name]
        else:
            opus_table_name_list = input_storage.get_table_names()

        for i in opus_table_name_list:
            logCB("Exporting %s, %s, %s\n" % (i,year,opus_data_directory))
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
                )

def opusHelp():
    help = 'This tool will get a table from an Opus Cache and export it to a SQL database.\n' \
           '\n' \
           'database_server_connection: the database server connection configured in the database server connection settings \n' \
           'opus_data_directory: full path to the OPUS data directory (c:\\opus\\data\\seattle_parcel\\base_year_data)\n' \
           'opus_data_year: the year to which the data should be exported (2000)\n' \
           'database_name: the name of the database (or PostgreSQL schema) that contains the table\n' \
           'table_name: the name of the table to be exported\n'
    return help