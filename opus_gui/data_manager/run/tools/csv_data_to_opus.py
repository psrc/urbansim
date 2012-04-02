# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.export_storage import ExportStorage
from opus_core.store.sql_storage import sql_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.csv_storage import csv_storage 

def opusRun(progressCB,logCB,params):

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)
        
    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']
    csv_data_path = params_dict['csv_data_path']
    table_name = params_dict['csv_table_name']
    
    input_storage = csv_storage(storage_location = csv_data_path)
    
    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
    SimulationState().set_current_time(opus_data_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    if table_name == 'ALL':
        logCB('caching all tables...\n')
        lst = input_storage.get_table_names()
    else:
        lst = [table_name]
        
    for i in lst:
        logCB("Exporting table '%s' to year %s of cache located at %s...\n" %
                   (i, opus_data_year, opus_data_directory))
        ExportStorage().export_dataset(
            dataset_name = i,
            in_storage = input_storage,
            out_storage = output_storage)

def opusHelp():
    help = 'This tool will get a table in csv format and export it to the OPUS cache format.\n' \
           '\n' \
           'csv_data_path: full path to the csv data directory\n' \
           'csv_table_name: the name of the table to be exported\n' \
           'opus_data_directory: full path to the OPUS data directory (c:\\opus\\data\\seattle_parcel\\base_year_data)\n' \
           'opus_data_year: the year to which the data should be exported (2000)\n' 
    return help
