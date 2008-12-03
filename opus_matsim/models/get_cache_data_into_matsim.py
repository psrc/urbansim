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

from opus_core.export_storage import ExportStorage
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.store.flt_storage import flt_storage
from opus_core.store.tab_storage import tab_storage
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
import os
import shutil
import sys


class GetCacheDataIntoMatsim(GetCacheDataIntoTravelModel):
    """Get needed data from UrbanSim cache into inputs for travel model.
       Essentially a variant of opus_core/tools/do_export_cache_to_tab_delimited_files.py
    """

    def run(self, config, year):
        logger.start_block('Starting GetCacheDataIntoMatsim.run(...)')
        
        cache_path = config['cache_directory'] + '/' + year.__str__()
        logger.log_status( " cache_path: " + cache_path ) ;
        
        output_directory = os.environ['OPUS_HOME'].__str__() + "/opus_matsim/tmp"
        logger.log_status(" output_directory: " + output_directory )
        
        # creating an empty tmp directory:
        shutil.rmtree( output_directory, ignore_errors = True )
        os.mkdir( output_directory )
        
        in_storage = flt_storage(storage_location = cache_path)
        out_storage = tab_storage(storage_location = output_directory)

        ExportStorage().export_dataset('persons', in_storage, out_storage)
        ExportStorage().export_dataset('jobs', in_storage, out_storage)
        ExportStorage().export_dataset('buildings', in_storage, out_storage)
        ExportStorage().export_dataset('parcels', in_storage, out_storage)
        ExportStorage().export_dataset('households', in_storage, out_storage )
        
        logger.end_block()


# the following is needed, since it is called as "main" from the framework ...  
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
    GetCacheDataIntoMatsim().run(resources, options.year)
