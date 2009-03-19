# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
import sys

from optparse import OptionParser

from opus_core.logger import logger
from opus_core.export_storage import ExportStorage
from opus_core.store.esri_storage import esri_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration


if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-d', '--esri_path', dest='esri_path',
        type='string', help='The path to the directory or geodatabase containing the table to export (required).')
    parser.add_option('-c', '--attribute_cache_directory', dest='attribute_cache_directory',
        type='string', help='The filesystem path to the attribute cache to which output will be '
            'written (required).')
    parser.add_option('-t', '--table_name', dest='table_name',
        type='string', help='The name of the table into which output will be '
            'written (required).')
    parser.add_option('-y', '--cache_year', dest='cache_year', type='string',
        help="The attribute cache year into which to write the output (required).")

    (options, args) = parser.parse_args()

    esri_path = options.esri_path
    attribute_cache_directory = options.attribute_cache_directory
    table_name = options.table_name
    cache_year = options.cache_year

    if (esri_path is None or
        attribute_cache_directory is None or
        table_name is None or
        cache_year is None):

        parser.print_help()
        sys.exit(1)

    input_storage = esri_storage(storage_location = esri_path)

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
