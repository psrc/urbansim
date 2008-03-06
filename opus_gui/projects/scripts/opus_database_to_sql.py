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

import os, sys
from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.sql_storage import sql_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.opus_database import OpusDatabase
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration

def opusRun(progressCB,logCB,params):
    print "opus_database_to_sql.py called...."
    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)
        print "Key=%s Val=%s" % (key, val)

    sql_db_name = params_dict['sql_db_name']
    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']
    opus_table_name = params_dict['opus_table_name']

    dbserverconfig = DatabaseServerConfiguration()
    opusdb = OpusDatabase(dbserverconfig, sql_db_name)

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    attribute_cache_years = attribute_cache._get_sorted_list_of_years()
    if opus_data_year != 'ALL':
        attribute_cache_years = [opus_data_year]

    for year in attribute_cache_years:
        #input_storage = sql_storage(storage_location = opusdb)
        input_storage = attribute_cache.get_flt_storage_for_year(year)
                
        #output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
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
            print "Exporting %s, %s, %s" % (i,year,opus_data_directory)
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
                )
