# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.tsv_storage import tsv_storage
from opus_core.store.hdf5g_storage import hdf5g_storage


if __name__ == '__main__':
    parser = OptionParser(description='Converts a table in given tsv file into a group in an hdf5 file.')
    
    parser.add_option('-d', '--tsv_directory', dest='tsv_directory',
        type='string', help='The filesystem path to the directory containing the tsv file to export (required).')
    parser.add_option('-o', '--output_file', dest='output_file', 
        type='string', help='Full name of the output file (required).')
    parser.add_option('-t', '--table_name', dest='table_name', 
        type='string', help='The name of the table (required). Must correspond to the tsv file name (excluding suffix).')
    parser.add_option('--compression', dest='compression', type='string', default=None,
                      help='Compression type. Available: gzip, lzf. Default is no compression.')
    (options, args) = parser.parse_args()

    directory = options.tsv_directory
    output_file = options.output_file   
    table_name = options.table_name
    
    if (directory is None or 
        output_file is None or 
        table_name is None):
        
        parser.print_help()
        sys.exit(1)
        
    input_storage = tsv_storage(storage_location = directory)
    output_storage = hdf5g_storage(storage_location = output_file)
    
    logger.start_block("Exporting table '%s' into %s..." %
                   (table_name, output_file))
    try:
        output_storage.drop_table(table_name)
        ExportStorage().export_dataset(
            dataset_name = table_name,
            in_storage = input_storage, 
            out_storage = output_storage, 
            compression=options.compression
        )
    finally:
        logger.end_block()
    