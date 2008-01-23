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

import os 
import shutil
from opus_core.resources import Resources
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel

class RestoreTripTables:
    """Copy original trip tables to the 'triptabs' directory of the travel model.
    """
    def run(self, config, source_directory, year):
        tm = AbstractEmme2TravelModel()
        dir = tm.get_emme2_dir(config, year)
        dst = os.path.join(dir, 'triptabs')
        src = os.path.join(dir, source_directory)
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
