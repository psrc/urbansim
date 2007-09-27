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

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.dbf_storage import dbf_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.mysql_database_server import MysqlDatabaseServer
from opus_core.configurations.database_server_configuration import DatabaseServerConfiguration


if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option('-d', '--dbf_directory', dest='dbf_directory',
        type='string', help='The filesystem path to the directory containing the dbf file to export (required).')
    parser.add_option('-c', '--attribute_cache_directory', dest='attribute_cache_directory', 
        type='string', help='The filesystem path to the attribute cache to which output will be '
            'written (required).')
    parser.add_option('-t', '--table_name', dest='table_name', 
        type='string', help='The name of the table into which output will be '
            'written (required).')
    parser.add_option('-y', '--cache_year', dest='cache_year', type='string',
        help="The attribute cache year into which to write the output (required).")

    (options, args) = parser.parse_args()

    dbf_directory = options.dbf_directory
    attribute_cache_directory = options.attribute_cache_directory    
    table_name = options.table_name    
    cache_year = options.cache_year
    
    if (dbf_directory is None or 
        attribute_cache_directory is None or 
        table_name is None or
        cache_year is None):
        
        parser.print_help()
        sys.exit(1)
        
    input_storage = dbf_storage(storage_location = dbf_directory)
    
    attribute_cache = AttributeCache(cache_directory=attribute_cache_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(cache_year)
    SimulationState().set_current_time(cache_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())
    
    logger.start_block("Exporting table '%s' to year %s of cache located at %s..." %
                   (table_name, cache_year, attribute_cache_directory))
    try:
        ExportStorage().export_dataset(
            dataset_name = table_name,
            in_storage = input_storage, 
            out_storage = output_storage,
        )
    finally:
        logger.end_block()
    