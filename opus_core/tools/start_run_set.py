# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import sys
import pickle

from numpy.random import seed, randint

from opus_core.logger import logger
from opus_core.misc import write_to_text_file
from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.services.run_server.run_manager import RunManager


class StartRunSetOptionGroup(GenericOptionGroup):
    """Class for starting multiple runs.
    """
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Starts running a set of runs.")
        self.parser.add_option("-r", "--pickled-resource-file", dest="pickled_resource_file", default=None,
                                help="Opus path to pickled configuration file.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None,
                                help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                                help="file name of xml configuration (must also provide a scenario name using -s)")
        self.parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                                help="name of the scenario to run")
        self.parser.add_option("--directory-to-cache", dest="existing_cache_to_copy", default=None,
                                action="store",
                                help="Directory containing data to put in new cache.")
        self.parser.add_option("--years-to-cache", dest="years_to_cache",
                                default=None, action="store",
                                help="List of years of data to take from the directory-to-cache (default is all years).")

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = StartRunSetOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    run_manager = RunManager(option_group.get_services_database_configuration(options))

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
            exec(import_stmt, globals())
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
        config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = options.existing_cache_to_copy
        if options.years_to_cache is not None:
            config['creating_baseyear_cache_configuration'].baseyear_cache.years_to_cache = eval(options.years_to_cache)

    number_of_runs = config.get("number_of_runs", 1)
    number_of_runs_in_parallel = min(config.get("parallel_runs", 1), number_of_runs)
    # generate seeds for multiple runs
    root_seed = config.get("seed", None)
    seed(root_seed)
    # generate different seed for each run (each seed contains 1 number)
    seed_array = randint(1,2**30, number_of_runs)
    list_of_cache_directories = []
    for irun in range(number_of_runs):
        config['seed']= (seed_array[irun],)
        this_config = config.copy()
        if ((irun + 1) % number_of_runs_in_parallel) == 0:
            run_in_background = False
        else:
            run_in_background = True
        run_manager.setup_new_run(cache_directory = this_config['cache_directory'],
                                  configuration = this_config)
        run_manager.run_run(this_config, run_as_multiprocess=False,
                            run_in_background=run_in_background)
        if irun == 0:
            # log file for the multiple runs will be located in the first cache
            first_cache_directory = this_config['cache_directory']
            log_file = os.path.join(first_cache_directory, 'multiple_runs.log')
            logger.enable_file_logging(log_file)
            logger.log_status("Multiple runs: %s replications" % number_of_runs)
            logger.log_status("root random seed = %s" % str(root_seed))
        else:
            logger.enable_file_logging(log_file, verbose=False)

        logger.log_status("Run %s: %s" % (irun+1, this_config['cache_directory']))
        logger.disable_file_logging(log_file)
        list_of_cache_directories.append(this_config['cache_directory'])
        write_to_text_file(os.path.join(first_cache_directory,"cache_directories"),
                                list_of_cache_directories)