# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
import os, time

class StartRunOptionGroup(object):
    """ Helper class to start model from an xml config file. 
    """
    
    def __init__(self):
        logger.start_block("Starting UrbanSim")
        
        # starts the psrc measurement test (measuring the amout of data and amount of time executing urabnSim with MATSim)
        #self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_measurements/config/psrc_measurement.xml' ).get_run_configuration( 'accra_baseline' )
        
        # starts the same measurements with a smaller scenario (Seattle baseline)
        #self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_measurements/config/seattle_parcel_measurement.xml' ).get_run_configuration( 'Seattle_baseline' )
        
        # starts sensetivity test for psrc
        self.config = XMLConfiguration( 'opus_matsim/sustain_city/tests/psrc_measurements/config/psrc_measurement.xml' ).get_run_configuration( 'accra_baseline' )
        
        # add result dictionary to config, where all measurements are stored
        self.config['psrc_logfile'] = self.create_logfile()

        
    def run(self):
        
        logger.start_block()
        insert_auto_generated_cache_directory_if_needed(self.config)
         
        run_manager = RunManager(ServicesDatabaseConfiguration())
        run_manager.setup_new_run(cache_directory = self.config['cache_directory'],configuration = self.config)
        
        start_time = time.time()
        run_manager.run_run(self.config, run_as_multiprocess = True )
        end_time = time.time()
        
        self.dump_results(self.config, int(end_time-start_time))
        logger.end_block()
        
            
    def create_logfile(self):
        
        logger.log_status('Creating logfile...')
        
        destination = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp', 'psrc_log.txt')
        
        file_object = open( destination , 'w')
        
        file_object.write('PSRC measurements results\n')
        file_object.write('=========================\n') 
        file_object.write('\n') 
        
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status('Finished creating logfile.')
        
        return destination
    
    def dump_results(self, config, duration):
        
        logger.log_status('Loging results...')
        
        file = config['psrc_logfile']
        
        # append measurements to log file
        file_object = open( file , 'a') 
        
        file_object.write('Duration of complete simulation run:%f\n'%duration) 
        file_object.write('\n')
        
        file_object.flush()
        if not file_object.closed:
            file_object.close()
            
        logger.log_status('Finished loging.')
    
if __name__ == "__main__":
    start = StartRunOptionGroup()
    start.run()