# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed

class StartRunOptionGroup(object):
    """ Helper class to start model from an xml config file. 
    """
    
    def __init__(self):
        logger.start_block("Starting UrbanSim")
        
        # starts BASE SCENARIO
        #self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_sensitivity_tests/config/psrc_base_scenario.xml' ).get_run_configuration( 'PSRC_baseline' )
        
        # starts MOD SCENARIO WITHOUT MATSIM
        self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_sensitivity_tests/config/psrc_modified_without_matsim_scenario.xml' ).get_run_configuration( 'PSRC_baseline' )
        
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