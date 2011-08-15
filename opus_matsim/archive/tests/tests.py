# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

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
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        print "leaving setUp"

    def tearDown(self):
        print "entering tearDown"
#        # Turn off the logger, so we can delete the cache directory.
#        logger.disable_all_file_logging()
        print "leaving tearDown"

    def cleanup_test_run(self):
        print "entering cleanup_test_run"
#        cache_dir = self.resources['cache_directory']
#        if os.path.exists(cache_dir):
#            rmtree(cache_dir)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir, True)
        print "leaving cleanup_test_run"
        
    def test_run(self):
 
        # The paths work as follows: opus_matsim.__path__ is the path of the opus_matsim python module.  So we can use that
        # as anchor ...
        config_location = os.path.join(opus_matsim.__path__[0], 'archive', 'tests')
        print "location: ", config_location
        run_config = XMLConfiguration( os.path.join(config_location,"test_config.xml")).get_run_configuration("Test")
        
        run_config['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        run_config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = \
            os.path.join(opus_matsim.__path__[0], 'tests', 'testdata', 'base_year_data')

        # insert_auto_generated_cache_directory... does things I don't understand.  Need to do the following to obtain consistent
        # behavior independent from the file root:
        run_config['cache_directory'] = None
        
        insert_auto_generated_cache_directory_if_needed(run_config)
        run_manager = RunManager(ServicesDatabaseConfiguration())
    
        run_manager.setup_new_run(cache_directory = run_config['cache_directory'],
                                  configuration = run_config)
        
        run_manager.run_run(run_config, run_as_multiprocess = True )
        

        self.assert_(True)
        
        self.cleanup_test_run()

        
if __name__ == "__main__":
    opus_unittest.main()

