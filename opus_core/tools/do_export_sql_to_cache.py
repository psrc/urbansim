# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
    
    parser.add_option("--database_configuration", dest="database_configuration", default = "estimation_database_server",
                       action="store", help="Name of the database server configuration in database_server_configurations.xml where the output database is to be created. Defaults to 'estimation_database_server'.")

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
        database_configuration = options.database_configuration 
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
