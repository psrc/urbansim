# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from opus_core.export_storage import ExportStorage
from opus_core.store.esri_storage import esri_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

def opusRun(progressCB,logCB,params):

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    esri_data_path = params_dict['esri_data_path']
    esri_table_name = params_dict['esri_table_name']
    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']

    input_storage = esri_storage(storage_location = esri_data_path)
    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)

    SimulationState().set_current_time(opus_data_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    if esri_table_name == 'ALL':
        logCB("Sending all tables to OPUS storage...\n")
        lst = input_storage.get_table_names()
        for i in lst:
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
            )

    else:
        logCB("Exporting table '%s' to OPUS storage located at %s...\n" % (esri_table_name, opus_data_directory))
        ExportStorage().export_dataset(
                                       dataset_name = esri_table_name,
                                       in_storage = input_storage,
                                       out_storage = output_storage,
                                       )
        logCB("Finished exporting table '%s'\n" % (esri_table_name))

def opusHelp():
    help = 'This tool will convert an ESRI based table to the specified OPUS cache.\n' \
           '\n' \
           'esri_data_path: folder path for shapefiles (c:\\temp), database path for personal and file geodatabases' \
           '(c:\\test.gdb or c:\\test.mdb), or database connection path for SDE geodatabases (Database Connections\\your connection.sde)\n' \
           'esri_table_name: name of shapefile (test.shp), feature class (your_feature_class) contained in esri_data_path, or ALL for all tables\n' \
           'opus_data_directory: full path to the OPUS data directory (c:\\opus\\data\\seattle_parcel\\base_year_data)\n' \
           'opus_data_year: the year to which the data should be exported (2000)'
    return help