# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os 
import shutil
from opus_core.resources import Resources
from abstract_emme2_travel_model import AbstractEmme2TravelModel

class RestoreTripTables(AbstractEmme2TravelModel):
    """Copy original trip tables to the 'triptabs' directory of the travel model.
    """
    def run(self, config, source_directory, year):
        base_dir = self.get_emme2_base_dir()
        dst = os.path.join(base_dir, 'triptabs')
        src = os.path.join(base_dir, source_directory)
        backup = os.path.join(base_dir, 'triptabs.last')
        if os.path.exists(backup):
            shutil.rmtree(backup)
        if os.path.exists(dst):
            shutil.copytree(dst, backup)
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year for which the emme2 directory is defined in the configuration.")
    parser.add_option("-d", "--directory", dest="directory", action="store", type="string", default="triptabs.org",
                      help="Name of sub-directory containing original trip tables (relative to the emme2 directory).")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    RestoreTripTables().run(resources, options.directory, options.year)    
