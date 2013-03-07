# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.export_storage import ExportStorage
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

if __name__ == '__main__':
    parser = OptionParser(usage="python %prog from to [options]",
                          description='Converts a dataset from one format to another. "from" and "to" can be one of the following: '
                          'csv, tab, tsv, flt, sql, dbf, esri, hdf5, hdf5g')
    
    parser.add_option('-d', '--directory', dest='directory',
        type='string', help='The filesystem path containing the input data. If converting a database table, this is the database name (required).')
    parser.add_option('-o', '--output', dest='output', 
        type='string', help='Full name of the output directory or file or output database name (required).')
    parser.add_option('-t', '--table_name', dest='table_name', 
        type='string', help='The name of the table (required). If exporting from a file, it must correspond to the filename without the suffix.')
    parser.add_option('--no-type-info', dest='append_type_info', action="store_false", default=True,
                      help='No type info is added to column names. Available for tab and comma delimited output types.')
    parser.add_option('--compression', dest='compression', type='choice', default=None, choices=['gzip', 'lzf'],
                      help='Compression type for hdf5 and hdf5g output types. Available: gzip, lzf. Default is no compression.')
    parser.add_option("--database_configuration", dest="database_configuration", default = "indicators_database_server",
            action="store", help="Name of the database server configuration in database_server_configurations.xml where the output database is to be created. Defaults to 'indicators_database_server'. Used only with sql output type.")
    (options, args) = parser.parse_args()

    directory = options.directory
    output_file = options.output
    table_name = options.table_name
    
    arg_list = {'hdf5': ['compression'],
                'hdf5g': ['compression'],
                'tab': ['append_type_info'],
                'tsv': ['append_type_info'],
                'csv': ['append_type_info'],
                }
    create_output_directory = ['hdf5', 'tab', 'tsv', 'csv', 'dbf']
    if (directory is None or output_file is None or table_name is None):      
        parser.print_help()
        sys.exit(1)
    storage_intype = args[0]
    storage_outtype = args[1]
        
    if storage_intype == 'sql':
        database_name = directory
        db_server = DatabaseServer(DatabaseConfiguration(
            database_name = database_name,
            database_configuration = options.database_configuration
            )
        )                
        db = db_server.get_database(database_name)
        directory = db
        
    if storage_outtype == 'sql':
        database_name = output_file
        db_server = DatabaseServer(DatabaseConfiguration(
            database_name = database_name,
            database_configuration = options.database_configuration
            )
        )
        if not db_server.has_database(database_name):
            db_server.create_database(database_name)                          
        db = db_server.get_database(database_name)
        output_file = db
        
    input_storage = StorageFactory().get_storage('%s_storage' % storage_intype, storage_location = directory)
    output_storage = StorageFactory().get_storage('%s_storage' % storage_outtype, storage_location = output_file)
    
    if storage_outtype in create_output_directory and not os.path.exists(output_file):
        os.makedirs(output_file)
        
    logger.start_block("Converting table '%s' from %s into %s ..." % (table_name, storage_intype, storage_outtype))
    kwargs = {}
    for arg in arg_list.get(storage_outtype, []):
        kwargs[arg] = getattr(options, arg, None)
    try:
        if hasattr(output_storage,"drop_table"):
            output_storage.drop_table(table_name)
        ExportStorage().export_dataset(
            dataset_name = table_name,
            in_storage = input_storage, 
            out_storage = output_storage, **kwargs)
    finally:
        logger.end_block()
    
# Examples:
###########
# Convert sql table 'my_table' in database 'my_database' into a cache directory my_cache/2000:
# python convert_table.py sql flt -d my_database -t my_table -o my_cache/2000

# Convert a table 'persons' from cache into a csv file in the current directory, without type info in the column names:
# python convert_table.py flt csv -d my_cache/2000 -t persons -o . --no-type-info

# Convert a tsv file my_file.tsv in the current directory into an hdf5 file with each attribute being an upper level hdf5 dataset:
# python convert_table.py tsv hdf5 -d . -t my_file -o . 

# Convert a dbf file my_table.dbf in the current directory into an hdf5 file with the table being an hdf5 group in an existing hdf5 file:
# python convert_table.py dbf hdf5g -d . -t my_table -o my_existing_file.hdf5

# Convert a table 'my_table' from an hdf5 file (with the table being a group) into a sql database 'my_database':
# python convert_table.py hdf5g sql -d my_existing_file.hdf5 -t my_table -o my_database


 