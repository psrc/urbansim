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
    parser.add_option('-p', '--protocol', dest='protocol', type='string', default = None,
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
    parser.add_option('-t', '--table_name', dest='table_name', type='string', 
        help='Name of table to be exported (optional). Used if only one table should be exported.')

    (options, args) = parser.parse_args()

    cache_path = options.cache_path
    database_name = options.database_name    
    if database_name is None or cache_path is None:
        parser.print_help()
        sys.exit(1)
            
    host_name = options.host_name
    user_name = options.user_name            
    password = options.password
    protocol = options.protocol
    
    table_name = options.table_name
    
    logger.log_status('Initializing database...')
    db_server = DatabaseServer(EstimationDatabaseConfiguration(
            protocol = protocol,
            host_name = host_name,
            user_name = user_name,
            password = password,
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