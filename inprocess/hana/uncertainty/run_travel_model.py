# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
import shutil
from time import localtime, strftime
from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.fork_process import ForkProcess
from opus_core.logger import logger
from numpy.random import seed, randint

class OptionGroup(GenericOptionGroup):
    def __init__(self, **kwargs):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Run travel model (possibly) multiple times for one year.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--year", dest="year", default=0,
                               help="Year to run the travel model for.")
        self.parser.add_option("--cache-directory", dest="cache_directory", default=None, 
                               help="Cache directory with urbansim results.")
        
        
class RunTravelModel:
    """ 
        This class runs travel model (possibly) multiple times for one year. It generates number of households and jobs from posterior distribution and 
        creates appropriate input to the travel model. It needs a cache with urbansim results for that year to determine shares of jobs and households 
        of different characteristics. 
    """
                
    def run(self, year, configuration_path, cache_directory, log_file):
        config = get_config_from_opus_path(configuration_path)
        config['cache_directory'] = cache_directory
        number_of_runs = config.get('number_of_runs', 1)
        if 'all_seeds' in config.keys():
            seed_array = config['all_seeds']
        else:
            if 'seed' in config.keys():
                seed(config['seed'])
            seed_array = randint(1,2**30, number_of_runs)
        logger.log_status("All seeds: %s", seed_array)
        for tmrun in range(1, number_of_runs+1):
            logger.log_status("Travel model run %s, seed %s" % (tmrun, seed_array[tmrun-1]))
            subdir = 'emme_run_%s_%s' % (tmrun, strftime('%Y_%m_%d_%H_%M', localtime()))
            tmdir = os.path.join(cache_directory, subdir)
            config['seed']= (seed_array[tmrun-1],)
            logger.disable_file_logging(log_file)
            success = self._do_one_run(year, config)
            logger.enable_file_logging(log_file)
            if success:
                if not os.path.exists(tmdir):
                    os.makedirs('%s' % tmdir)
                logger.log_status("Copy results to %s" % tmdir)
                shutil.move(os.path.join(config['cache_directory'], str(year+1)), os.path.join(tmdir, str(year+1)))
                emme2logfiles = [os.path.join(config['cache_directory'],'emme2_%d_log.txt' % year), 
                                 os.path.join(config['cache_directory'],'emme2_export_macros_%d_log.txt' % year)]
                for file in emme2logfiles:
                    if os.path.exists(file):
                        shutil.move(os.path.join(config['cache_directory'],file), tmdir)
                 
    def _do_one_run(self, year, config):
        if not config['travel_model_configuration'].has_key(year):
            logger.log_status("No configuration for year %s" % year)
            return False
        for full_model_path in config['travel_model_configuration'][year].get('models'):
            optional_args=['-y', year]
            ForkProcess().fork_new_process(full_model_path, config, optional_args=optional_args, delete_temp_dir=False)
        return True    

    
if __name__ == "__main__":
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    try: import wingdbstub
    except: pass

    log_file = os.path.join(options.cache_directory, 'run_travel_model.log')
    logger.enable_file_logging(log_file)
    tmrun = RunTravelModel()
    tmrun.run(int(options.year), options.configuration_path, options.cache_directory, log_file)
 
 


