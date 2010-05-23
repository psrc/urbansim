# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.csv_storage import csv_storage


if __name__ == '__main__':
    parser = OptionParser()
    
    parser.add_option('-c', '--cache_path', dest='cache_path', type='string', 
        help='The filesystem path to the cache to export (required)')
    parser.add_option('-o', '--output_directory', dest='output_directory', 
        type='string', help='The filesystem path of the database to which '
            'output will be written (required)')
    parser.add_option('-t', '--table_name', dest='table_name', 
        type='string', help='Name of table to be exported (optional). Used if only one table should be exported.')

    (options, args) = parser.parse_args()
    
    cache_path = options.cache_path
    output_directory = options.output_directory
    table_name = options.table_name
    
    if None in (cache_path, output_directory):
        parser.print_help()
        sys.exit(1)

    in_storage = flt_storage(storage_location=cache_path)

    out_storage = csv_storage(storage_location=output_directory)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if table_name is not None:
        ExportStorage().export_dataset(table_name, in_storage=in_storage, out_storage=out_storage)
    else:
        ExportStorage().export(in_storage=in_storage, out_storage=out_storage)