# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
import subprocess
from opus_core.export_storage import ExportStorage
from opus_core.store.csv_storage import csv_storage 
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

def opusRun(progressCB,logCB,params):
    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    # Output csv data path
    csv_data_path = params_dict['csv_data_path']
    # Data clasification - Database (must be specified)
    opus_data_directory = params_dict['opus_data_directory']
    # Data clasification - Dataset (explicit or ALL)
    opus_data_year = params_dict['opus_data_year']
    # Data clasification - Array (explicit or ALL)
    opus_table_name = params_dict['opus_table_name']

    execute_after_export = params_dict['execute_after_export']

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    attribute_cache_years = [int(year) for year in os.listdir(opus_data_directory) if year.isdigit() and len(year) == 4]

    if opus_data_year != 'ALL':
        attribute_cache_years = [opus_data_year]

    for year in attribute_cache_years:

        input_storage = attribute_cache.get_flt_storage_for_year(year)
        
        output_storage = csv_storage(storage_location = csv_data_path)

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
            
        logCB("Successfully exported all datasets.")
            
    file_name_list = [output_storage._get_file_path_for_table(i)
                      for i in opus_table_name_list]
    subprocess.Popen([execute_after_export] + file_name_list)
