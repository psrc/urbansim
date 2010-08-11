# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
from opus_core.logger import logger

class StartRun(object):
    """ Helper class to start model from an xml config file. 
    """
    
    def run(self, config, executable):
        #--config=opus_matsim/sustain_city/configs/seattle_parcel.xml --executable=Seattle_baseline
        config = XMLConfiguration(config).get_run_configuration(executable)
        
        insert_auto_generated_cache_directory_if_needed(config)
     
        run_manager = RunManager(ServicesDatabaseConfiguration())
        
        run_manager.setup_new_run(cache_directory = config['cache_directory'],configuration = config)

        run_manager.run_run(config, run_as_multiprocess = True )

import time

class Tests(object):#(opus_unittest.OpusTestCase):
    ''' This test compares the execution time of two different scenarios 
        (or same scenarios but with a different konfiguration).
    '''
    
    def __init__(self):
        print "entering setUp"
        
        logger.log_status(' This test compares the execution time of two different scenarios \
                           (or same scenarios but with a different konfiguration).')
        
        self.scenario = None
        self.elapsed_time_sceanario = None
        self.start_time = None
        self.end_time = None
        print "leaving setUp"
        
    def test_run(self):
        elapsed_time1 = self.run_scenario("opus_matsim/sustain_city/tests/configs/seattle_parcel_test.xml", "Seattle_baseline")
        # preparing next run
        self.reset_time()
        elapsed_time2 = self.run_scenario("opus_matsim/sustain_city/tests/configs/san_antonio_zone_test.xml", "san_antonio_baseline")
        
        print "Runtime for Scenario 1 took %f min" % elapsed_time1
        print "Runtime for Scenario 2 took %f min" % elapsed_time2
        
    def run_scenario(self, config, executable):
        # instanciate first scenario
        self.scenario = StartRun()
        print "Running scenario"
        # get the actual time running the fist scenario
        self.start_time = time.time()
        # run first scenario
        self.scenario.run(config, executable)
        # stopping the time
        self.end_time = time.time()
        # return elapsed time in minutes
        print "Run complete"
        return (self.end_time - self.start_time)/60.0
        
    def reset_time(self):
        self.start_time = None
        self.end_time = None
            
if __name__ == "__main__":
    # opus_unittest.main()
    test = Tests()

