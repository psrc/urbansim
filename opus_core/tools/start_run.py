# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import sys, pickle

from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.services.run_server.run_manager import RunManager


class StartRunOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Starts running the specified configuration.")
        self.parser.add_option("-r", "--pickled-resource-file", dest="pickled_resource_file", default=None, 
                                help="Opus path to pickled configuration file.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                                help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                                help="file name of xml configuration (must also provide a scenario name using -s)")
        self.parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                                help="name of the scenario to run")
        self.parser.add_option("--directory-to-cache", dest="existing_cache_to_copy", default=None, 
                                help="Directory containing data to put in new cache.")
        self.parser.add_option("--years-to-cache", dest="years_to_cache", default=None, 
                                help="List of years of data to take from the directory-to-cache (default is all years).")                   
        self.parser.add_option("--run-as-single-process", dest="run_as_single_process", default=False, 
                                help="Determines if multiple processes may be used.")
        self.parser.add_option("-p", "--profile", dest="profile_filename", default=None, 
                                help="Turn on code profiling. Output data are in python hotshot format.")
        

if __name__ == "__main__":
    #try: import wingdbstub
    #except: pass
    option_group = StartRunOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    run_manager = RunManager(option_group.get_services_database_configuration(options))
    run_as_multiprocess = not options.run_as_single_process
    
    if options.pickled_resource_file is not None:
        f = file(options.pickled_resource_file, 'r')
        try:
            config = pickle.load(f)
        finally:
            f.close()
    elif options.configuration_path is not None:
        opus_path = options.configuration_path
        try:
            config = get_config_from_opus_path(opus_path)
        except ImportError:
            # TODO: Once all fully-specified configurations are stored as classes,
            #       get rid of this use.
            import_stmt = 'from %s import run_configuration as config' % opus_path
            exec(import_stmt)
        insert_auto_generated_cache_directory_if_needed(config)
    elif options.xml_configuration is not None:
        if options.scenario_name is None:
            parser.print_help()
            sys.exit(1)
        config = XMLConfiguration(options.xml_configuration).get_run_configuration(options.scenario_name)
        insert_auto_generated_cache_directory_if_needed(config)
    else:
        parser.print_help()
        sys.exit(1)
        
    if options.existing_cache_to_copy is not None:
        config['creating_baseyear_cache_configuration'].cache_from_database = False
        config['creating_baseyear_cache_configuration'].baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = options.existing_cache_to_copy,
            )
        if options.years_to_cache is not None:
            config['creating_baseyear_cache_configuration'].baseyear_cache.years_to_cache = eval(options.years_to_cache)

    if options.profile_filename is not None:
        config["profile_filename"] = options.profile_filename
 
    run_manager.setup_new_run(cache_directory = config['cache_directory'],
                              configuration = config)
    run_manager.run_run(config, 
                        scenario_name=options.scenario_name,
                        run_as_multiprocess=run_as_multiprocess)
