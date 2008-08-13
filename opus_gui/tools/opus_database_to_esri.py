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

import os, sys
from opus_core.export_storage import ExportStorage
esri_is_avail = False
try:
    from opus_core.store.esri_storage import esri_storage
    esri_is_avail = True
except ImportError:
    print "Unable to import esri_storage"
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

def opusRun(progressCB,logCB,params):
    print "opus_database_to_esri.py called...."
    params_dict = {}
    for key, val in params.iteritems():
        params_dict[str(key)] = str(val)
        print "Key=%s Val=%s" % (key, val)

    # Output esri data path
    esri_data_path = params_dict['esri_data_path']
    # Data clasification - Database (must be specified)
    opus_data_directory = params_dict['opus_data_directory']
    # Data clasification - Dataset (explicit or ALL)
    opus_data_year = params_dict['opus_data_year']
    # Data clasification - Array (explicit or ALL)
    opus_table_name = params_dict['opus_table_name']

    attribute_cache = AttributeCache(cache_directory=opus_data_directory)
    attribute_cache_years = attribute_cache._get_sorted_list_of_years()
    #print "Name = %s - Length of years list = %d" % (attribute_cache.get_storage_location(),
    #                                                 len(attribute_cache_years))

    if opus_data_year != 'ALL':
        attribute_cache_years = [opus_data_year]

    for year in attribute_cache_years:
        #input_storage = esri_storage(storage_location = esri_data_path)
        input_storage = attribute_cache.get_flt_storage_for_year(year)
        
        #output_storage = attribute_cache.get_flt_storage_for_year(opus_data_year)
        if esri_is_avail:
            output_storage = esri_storage(storage_location = esri_data_path)
        else:
            output_storage = None
        SimulationState().set_current_time(year)
        SessionConfiguration(new_instance=True,
                             package_order=[],
                             in_storage=AttributeCache())
        
        if opus_table_name != 'ALL':
            opus_table_name_list = [opus_table_name]
        else:
            opus_table_name_list = input_storage.get_table_names()

        for i in opus_table_name_list:
            print "Exporting %s, %s, %s" % (i,year,opus_data_directory)
            ExportStorage().export_dataset(
                dataset_name = i,
                in_storage = input_storage,
                out_storage = output_storage,
                )
