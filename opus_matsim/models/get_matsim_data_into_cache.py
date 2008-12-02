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

#from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
#from matsim_functions import load_version_file
#from opus_core.variables.variable_name import VariableName
#from opus_core.storage_factory import StorageFactory
from urbansim.datasets.travel_data_dataset import TravelDataDataset
#from numpy import ravel, ones, array, repeat, newaxis
#from opus_core.export_storage import ExportStorage
#from opus_core.store.flt_storage import flt_storage
from opus_core.store.csv_storage import csv_storage


class GetMatsimDataIntoCache(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """
        """
        logger.log_status('Starting GetMatsimDataIntoCache.get_travel_data...')
        print >> sys.stderr, "MATSim replaces only _some_ of the columns of travel_data.  Yet, Urbansim does not truly merge them"
        print >> sys.stderr, " but simply overwrites the columns, without looking for a different sequence of from_zone_id, to_zone_id"
        
        input_directory = os.environ['OPUS_HOME'].__str__() + "/opus_matsim/tmp"
        logger.log_status("input_directory: " + input_directory )
        
        in_storage = csv_storage(storage_location = input_directory)

        table_name = "travel_data"
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )

        return travel_data_set


# this is needed since it is called from opus via "main":        
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetMatsimDataIntoCache().run(resources, options.year)
