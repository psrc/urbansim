# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.sql_storage import sql_storage
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration


if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option('-c', '--cache_path', dest='cache_path',
        type='string', help='The filesystem path to the cache to export (required).')
    parser.add_option('-d', '--database_name', dest='database_name',
        type='string', help='The name of the database to which output will be '
            'written (required).')

    parser.add_option("--database_configuration", dest="database_configuration", default = "estimation_database_server",
                       action="store", help="Name of the database server configuration in database_server_configurations.xml where the output database is to be created. Defaults to 'estimation_database_server'.")
    
    parser.add_option('-t', '--table_name', dest='table_name', type='string', 
        help='Name of table to be exported (optional). Used if only one table should be exported.')

    (options, args) = parser.parse_args()

    cache_path = options.cache_path
    database_name = options.database_name    
    if database_name is None or cache_path is None:
        parser.print_help()
        sys.exit(1)
    
    table_name = options.table_name
    
    logger.log_status('Initializing database...')
    db_server = DatabaseServer(EstimationDatabaseConfiguration(
            database_name = database_name,
            database_configuration = options.database_configuration
            )
        )
    if not db_server.has_database(database_name): # if only one table should be exported,
        db_server.create_database(database_name)                            # the database can exist

    db = db_server.get_database(database_name)
   
    input_storage = flt_storage(storage_location = cache_path)
    
    output_storage = sql_storage(
                        storage_location = db)
            
    logger.start_block('Exporting cache to sql...')
    try:
        if table_name is None:
            ExportStorage().export(in_storage=input_storage, out_storage=output_storage)
        else:
            db.drop_table(table_name)
            ExportStorage().export_dataset(table_name, in_storage=input_storage, out_storage=output_storage)        
    finally:
        logger.end_block()