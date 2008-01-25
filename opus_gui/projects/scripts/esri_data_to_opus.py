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

import os, sys
from opus_core.export_storage import ExportStorage
from opus_core.store.esri_storage import esri_storage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

def opusRun(progressCB,logCB,params):

    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)

    esri_data_path = params_dict['esri_data_path']
    esri_table_name = params_dict['esri_table_name']
    opus_data_directory = params_dict['opus_data_directory']
    opus_data_year = params_dict['opus_data_year']

    input_storage = esri_storage(storage_location = esri_data_path)
    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)

    SimulationState().set_current_time(opus_data_year)
    SessionConfiguration(new_instance=True,
                         package_order=[],
                         in_storage=AttributeCache())

    print "Exporting table '%s' to year %s of cache located at %s..." % (esri_table_name, opus_data_year, opus_data_directory)

    ExportStorage().export_dataset(
                                   dataset_name = esri_table_name,
                                   in_storage = input_storage,
                                   out_storage = output_storage,
                                   )
    print "Finished exporting table '%s'" % (esri_table_name)



#import os
#import sys
#
#from optparse import OptionParser
#
#from opus_core.logger import logger
#from opus_core.export_storage import ExportStorage
#from opus_core.store.esri_storage import esri_storage
#from opus_core.store.attribute_cache import AttributeCache
#from opus_core.simulation_state import SimulationState
#from opus_core.session_configuration import SessionConfiguration
#
#
#if __name__ == '__main__':
#    parser = OptionParser()
#
#    parser.add_option('-d', '--esri_path', dest='esri_path',
#        type='string', help='The path to the directory or geodatabase containing the table to export (required).')
#    parser.add_option('-c', '--attribute_cache_directory', dest='attribute_cache_directory',
#        type='string', help='The filesystem path to the attribute cache to which output will be '
#            'written (required).')
#    parser.add_option('-t', '--table_name', dest='table_name',
#        type='string', help='The name of the table into which output will be '
#            'written (required).')
#    parser.add_option('-y', '--cache_year', dest='cache_year', type='string',
#        help="The attribute cache year into which to write the output (required).")
#
#    (options, args) = parser.parse_args()
#
#    esri_path = options.esri_path
#    attribute_cache_directory = options.attribute_cache_directory
#    table_name = options.table_name
#    cache_year = options.cache_year
#
#    if (esri_path is None or
#        attribute_cache_directory is None or
#        table_name is None or
#        cache_year is None):
#
#        parser.print_help()
#        sys.exit(1)
#
#    input_storage = esri_storage(storage_location = esri_path)
#
#    attribute_cache = AttributeCache(cache_directory=attribute_cache_directory)
#    output_storage = attribute_cache.get_flt_storage_for_year(cache_year)
#    SimulationState().set_current_time(cache_year)
#    SessionConfiguration(new_instance=True,
#                         package_order=[],
#                         in_storage=AttributeCache())
#
#    logger.start_block("Exporting table '%s' to year %s of cache located at %s..." %
#                   (table_name, cache_year, attribute_cache_directory))
#    try:
#        ExportStorage().export_dataset(
#            dataset_name = table_name,
#            in_storage = input_storage,
#            out_storage = output_storage,
#        )
#    finally:
#        logger.end_block()
