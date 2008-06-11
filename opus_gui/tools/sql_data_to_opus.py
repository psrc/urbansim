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

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']
    sql_db_name = params_dict['sql_db_name']
    table_name = params_dict['table_name']


    dbserverconfig = DatabaseServerConfiguration()
    opusdb = OpusDatabase(dbserverconfig, sql_db_name)

    input_storage = sql_storage(storage_location = opusdb)

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
    SimulationState().set_current_time(opus_data_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    if table_name == 'ALL':
        print 'caching all tables...'
        lst = input_storage.get_table_names()
        for i in lst:
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
            )
    else:
        logger.start_block("Exporting table '%s' to year %s of cache located at %s..." %
                   (table_name, opus_data_year, opus_data_directory))
        ExportStorage().export_dataset(
            dataset_name = table_name,
            in_storage = input_storage,
            out_storage = output_storage)
