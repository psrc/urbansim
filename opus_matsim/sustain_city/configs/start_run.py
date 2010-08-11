# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
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
        
    insert_auto_generated_cache_directory_if_needed(config)
     
    run_manager = RunManager(ServicesDatabaseConfiguration())
        
    run_manager.setup_new_run(cache_directory = config['cache_directory'],configuration = config)
    
    #try: #tnicolai
    #    import pydevd
    #    pydevd.settrace()
    #except: pass
    
    run_manager.run_run(config, run_as_multiprocess = True )
    

'''from opus_core.tests import opus_unittest
class StartRunOptionGroupTest(opus_unittest.OpusTestCase):
    def __init__(self):
        print "entering __init__"
        
    def setUp(self):
        print "entering setUp"
        
    def test_run(self):
        print "entering test_run"
        
    def tearDown(self):
        print "entering tearDown"
        
    def cleanup_test_run(self):
        print "entering cleanup_test_run"'''
       
"""if __name__ == '__main__':
    opus_unittest.main()"""
        