# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import sys, optparse

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed

#class StartRunOptionGroup(GenericOptionGroup):
class StartRunOptionGroup(object):
    """ Helper class to start model from an xml config file. 
    """
        
    logger.start_block("Starting UrbanSim")
    
    # get program arguments from the command line
    program_arguments = sys.argv[1:]
    
    # default parameters are:
    # --config=opus_matsim/sustain_city/configs/seattle_parcel_prescheduled_events.xml 
    # --executable=Seattle_baseline
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="config_file_name", action="store", type="string",
                      help="Name of file containing urbansim config")
    parser.add_option("-e", "--executable", dest="scenario_executable", action="store", type="string",
                      help="Model to execute")
    (options, args) = parser.parse_args()
        
    if options.config_file_name == None:
        logger.log_error("Missing path to the urbansim config file")
    if options.scenario_executable == None:
        logger.log_error("Missing name of executable scenario")
    
    config = XMLConfiguration( options.config_file_name ).get_run_configuration( options.scenario_executable )
    # tnicolai: debug
    #config = XMLConfiguration( '/Users/thomas/Development/opus_home/matsim4opus/urbansim_config/seattle_parcel.xml' ).get_run_configuration( 'Seattle_baseline' )
        
    insert_auto_generated_cache_directory_if_needed(config)
     
    run_manager = RunManager(ServicesDatabaseConfiguration())
        
    run_manager.setup_new_run(cache_directory = config['cache_directory'],configuration = config)
    
    #try: #tnicolai: for debugging
    #    import pydevd
    #    pydevd.settrace()
    #except: pass

    run_manager.run_run(config, run_as_multiprocess = True )
    
    logger.end_block("UrbanSim simulation run done.")

        