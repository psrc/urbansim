# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
import opus_matsim.sustain_city.tests as test_dir
from opus_core.logger import logger

class TravelCostTest(object):
    """ Runs test scenario for travel costs
    """

    def __init__(self):
        print "Entering setup"
        
        logger.log_status('Running UrbanSim to test the impact of travel costs (provided from an dummy travel model)')
        
        # get sensitivity test path
        self.test_dir_path = test_dir.__path__[0]
        
        self.config_file = os.path.join( self.test_dir_path, "configs", "seattle_parcel_travel_cost_test.xml")
        print 'Loding UrbanSim config file: %s' % self.config_file
        
        # get seattle_parcel configuration
        self.config = XMLConfiguration( self.config_file ).get_run_configuration( "Seattle_baseline" )
        insert_auto_generated_cache_directory_if_needed(self.config)
        
        print "Leaving setup"
    
    def test_run(self):
        print "Entering test run"
        
        run_manager = RunManager(ServicesDatabaseConfiguration())
        run_manager.setup_new_run(cache_directory = self.config['cache_directory'],configuration = self.config)
        
        run_manager.run_run(self.config, run_as_multiprocess = True )
        
        print "Leaving test run"
        
if __name__ == "__main__":
    tct = TravelCostTest()
    tct.test_run()