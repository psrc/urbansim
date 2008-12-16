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

from opus_core.logger import logger
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
from opus_core.tests import opus_unittest
from shutil import rmtree
import opus_matsim
import os
import tempfile

# doing the testing separately since it seems easier to combine the three modules into one test

# files in eugene/tests may serve as examples ...


class Tests(opus_unittest.OpusTestCase):
    
    def setUp(self):
        print "entering setUp"
#        self.config = TestDatabaseConfiguration(database_name = 'eugene_services_test')
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        print "leaving setUp"

    def tearDown(self):
        print "entering tearDown"
        # Turn off the logger, so we can delete the cache directory.
        logger.disable_all_file_logging()
#        db_server = DatabaseServer(self.config)
#        db_server.drop_database('eugene_services_test')
#        db_server.close()
        print "leaving tearDown"

    def cleanup_test_run(self):
        print "entering cleanup_test_run"
#        cache_dir = self.resources['cache_directory']
#        if os.path.exists(cache_dir):
#            rmtree(cache_dir)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        print "leaving cleanup_test_run"
        
    def test_run(self):
        
        config_location = os.path.join(opus_matsim.__path__[0], 'configs')
        print "location: ", config_location
        run_config = XMLConfiguration( os.path.join(config_location,"test.xml")).get_run_configuration("Seattle_baseline")
#        run_config = XMLConfiguration( os.path.join(config_location,"eugene_gridcell.xml")).get_run_configuration("Eugene_baseline")
        
        run_config['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        run_config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = os.path.join(opus_matsim.__path__[0], 'data', 'seattle_parcel', 'base_year_data')
        insert_auto_generated_cache_directory_if_needed(run_config)
        
        run_manager = RunManager(ServicesDatabaseConfiguration())
        
        run_manager.setup_new_run(cache_directory = run_config['cache_directory'],
                                  configuration = run_config)
        
        run_manager.run_run(run_config, run_as_multiprocess = True )
        

        self.assert_(True)
        
        self.cleanup_test_run()

        
if __name__ == "__main__":
    opus_unittest.main()

