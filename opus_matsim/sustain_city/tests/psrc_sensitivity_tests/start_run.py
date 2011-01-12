# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import optparse
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed

class StartRunOptionGroup(object):
    """ Helper class to start model from an xml config file. 
    """
    
    def __init__(self):
        logger.start_block("Starting UrbanSim")
        
        # default parameters are:
        # --config=opus_matsim/sustain_city/configs/seattle_parcel_prescheduled_events.xml 
        # --executable=Seattle_baseline
        parser = optparse.OptionParser()
        parser.add_option("-c", "--config", dest="config_file_name", action="store", type="string",
                          help="Name of file containing urbansim config")
        parser.add_option("-e", "--executable", dest="scenario_executable", action="store", type="string",
                          help="Model to execute")
        (options, args) = parser.parse_args()
        
        # start
        #self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_sensitivity_tests/config/psrc_sensitivity_test.xml' ).get_run_configuration( 'PSRC_baseline' )
        #self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_sensitivity_tests/config/seattle_parcel_common_test.xml' ).get_run_configuration( 'Seattle_baseline' )
        #self.config = XMLConfiguration( '/Users/thomas/Development/opus_home/data/vsp_configs/cupum/psrc_parcel_default_cupum.xml' ).get_run_configuration( 'PSRC_baseline' )
        #self.config = XMLConfiguration( '/Users/thomas/Development/opus_home/data/vsp_configs/cupum/seattle_parcel_common_test.xml' ).get_run_configuration( 'Seattle_baseline' )
        self.config = XMLConfiguration( '/Users/thomas/Development/opus_home/data/vsp_configs/cupum/psrc_parcel_ferry_testing.xml' ).get_run_configuration( 'PSRC_baseline' )
        #self.config = XMLConfiguration( options.config_file_name ).get_run_configuration( options.scenario_executable )
        
    def run(self):
        
        logger.start_block()
        insert_auto_generated_cache_directory_if_needed(self.config)
         
        run_manager = RunManager(ServicesDatabaseConfiguration())
        run_manager.setup_new_run(cache_directory = self.config['cache_directory'],configuration = self.config)
        
        run_manager.run_run(self.config, run_as_multiprocess = True )

        logger.end_block()
    
if __name__ == "__main__":
    start = StartRunOptionGroup()
    start.run()