#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington and 2008 Kai Nagel
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

from numpy import array
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
from opus_core.tests import opus_unittest
import opus_matsim
import os
import sys

# doing the testing separately since it seems easier to combine the three modules into one test

# files in eugene/tests may serve as examples ...


class Tests(opus_unittest.OpusTestCase):
    
    def test_run(self):
        
        config_location = os.path.join(opus_matsim.__path__[0], 'configs')
        print "location: ", config_location
        config = XMLConfiguration( os.path.join(config_location,"test.xml")).get_run_configuration("Seattle_baseline")
#        config = XMLConfiguration( os.path.join(config_location,"eugene_gridcell.xml")).get_run_configuration("Eugene_baseline")
        
        insert_auto_generated_cache_directory_if_needed(config)
        
        run_manager = RunManager(ServicesDatabaseConfiguration())
        
        run_manager.setup_new_run(cache_directory = config['cache_directory'],configuration = config)
        
        run_manager.run_run(config, run_as_multiprocess = True )
        
        print >> sys.stderr, "should remove the output directory after run"
        
        self.assert_(True)
        
if __name__ == "__main__":
    opus_unittest.main()

