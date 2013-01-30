# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.hdf5g_storage import hdf5g_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration


if __name__ == '__main__':
    parser = OptionParser(description='Converts all tables contained (as groups) in an hdf5 file into Opus cache.')
    
    parser.add_option('-f', '--file', dest='hdf5_file',
        type='string', help='The full file name containing datasets to export (required).')
    parser.add_option('-c', '--attribute_cache_directory', dest='attribute_cache_directory', 
        type='string', help='The filesystem path to the attribute cache to which output will be '
            'written (required).')
    parser.add_option('-y', '--cache_year', dest='cache_year', type='string',
        help="The attribute cache year into which to write the output (required).")

    (options, args) = parser.parse_args()

    file_name = options.hdf5_file
    attribute_cache_directory = options.attribute_cache_directory
    cache_year = options.cache_year
    
    if (file_name is None or 
        attribute_cache_directory is None or 
        cache_year is None):
        
        parser.print_help()
        sys.exit(1)
        
    input_storage = hdf5g_storage(storage_location = file_name)
    
    attribute_cache = AttributeCache(cache_directory=attribute_cache_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(cache_year)
    SimulationState().set_current_time(cache_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())
    
    for table_name in input_storage.get_table_names():
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
    