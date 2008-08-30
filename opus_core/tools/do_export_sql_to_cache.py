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

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.sql_storage import sql_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.database_management.opus_database import OpusDatabase
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-d', '--db_name', dest='db_name',
        type='string', help='Name of database to cache from (required).')
    parser.add_option('-c', '--attribute_cache_directory', dest='attribute_cache_directory',
        type='string', help='The filesystem path to the attribute cache to which output will be '
            'written (required).')
    parser.add_option('-t', '--table_name', dest='table_name',
        type='string', help='The name of the table into which output will be '
            'written (required).')
    parser.add_option('-y', '--cache_year', dest='cache_year', type='string',
        help="The attribute cache year into which to write the output (required).")
    parser.add_option('--protocol', dest='protocol', type='string', default = None,
        help='The password for the server on which the output database will '
            "be created (default: estimation_database_configuration setup '').")
    parser.add_option('-o', '--host', dest='host_name', type='string', default = None,
        help="The host name of the server one which the output database will "
            "be created (default: estimation_database_configuration setup "
            "'localhost').")
    parser.add_option('-u', '--user', dest='user_name', type='string', default = None,
        help='The user name for the server on which the output database will '
            "be created (default: estimation_database_configuration setup '').")
    parser.add_option('-p', '--password', dest='password', type='string', default = None,
        help='The password for the server on which the output database will '
            "be created (default: estimation_database_configuration setup '').")

    (options, args) = parser.parse_args()

    db_name = options.db_name
    attribute_cache_directory = options.attribute_cache_directory
    table_name = options.table_name
    cache_year = options.cache_year

    if (db_name is None or
        attribute_cache_directory is None or
        cache_year is None):

        parser.print_help()
        sys.exit(1)

    if table_name is None:
        table_name = 'ALL'
    
    dbserverconfig = EstimationDatabaseConfiguration(
        host_name = options.host_name,
        user_name = options.user_name,           
        password = options.password,
        protocol = options.protocol  
    )
    opusdb = OpusDatabase(dbserverconfig, db_name)

    input_storage = sql_storage(storage_location = opusdb)

    attribute_cache = AttributeCache(cache_directory=attribute_cache_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(cache_year)
    SimulationState().set_current_time(cache_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    if table_name == 'ALL':
        print 'caching all...'
        lst = input_storage.get_table_names()
        for i in lst:
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
            )
        sys.exit(1)

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
