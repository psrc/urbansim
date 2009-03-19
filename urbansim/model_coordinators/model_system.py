# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.model_coordinators.model_system import ModelSystem as CoreModelSystem
from opus_core.model_coordinators.model_system import RunModelSystem

class ModelSystem(CoreModelSystem):
    """
    Uses the information in configuration to run/estimate a set of models.
    """
            
    def __init__(self):
        CoreModelSystem.__init__(self)
    
    def _run_each_year_as_separate_process(self, start_year, end_year, seed_array, resources, log_file_name='run_multiprocess.log'):
        skip_first_year_of_urbansim = resources.get('skip_urbansim', False)
        log_file = os.path.join(resources['cache_directory'], log_file_name)
        profiler_name = resources.get("profile_filename", None)
        iyear = 0
        for year in range(start_year, end_year+1):
            if (year <> start_year) or ((year == start_year) and (not skip_first_year_of_urbansim)):
                logger.start_block('Running UrbanSim for year %d in new process' % year)
                try:
                    resources['years'] = (year, year)
                    resources['seed'] = seed_array[iyear],
                    logger.disable_file_logging(log_file)
                    if profiler_name is not None:
                        resources["profile_filename"] = "%s_%s" % (profiler_name, year) # add year to the profile name
                    self._fork_new_process(
                        'urbansim.model_coordinators.model_system', resources, optional_args=['--log-file-name', log_file_name])
                    logger.enable_file_logging(log_file, verbose=False)
                finally:
                    logger.end_block()

            if ('travel_model_configuration' in resources) and (not resources.get('skip_travel_model', False)):
                self._run_travel_models_in_separate_processes(resources['travel_model_configuration'], year, resources)

            if 'post_year_configuration' in resources:
                self._run_travel_models_in_separate_processes(resources['post_year_configuration'], year, resources)
            iyear +=1
        self._notify_stopped()

    def _run_travel_models_in_separate_processes(self, year_models_dict, year, resources):
        if year in year_models_dict:
            if 'models' in year_models_dict[year]:
                models = year_models_dict[year]['models']  #post_year_process format
            else:
                models = year_models_dict['models']  #travel model format
            for opus_path in models:
                self._fork_new_process(opus_path, resources, optional_args=['-y', year])

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from shutil import rmtree
    from optparse import OptionParser
    from opus_core.resources import Resources   
    from opus_core.file_utilities import get_resources_from_file
    
    s = ModelSystem()
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-d", "--delete-resources-file-directory", dest="delete_resources_file_directory",
                      action="store_true",
                      help="Delete the directory containing the pickled resources file when done?")
    parser.add_option("--skip-cache-after-each-year", dest="skip_cache_after_each_year", default=False, 
                      action="store_true", help="Datasets will not be cached at the end of each year.")
    parser.add_option("--log-file-name", dest="log_file_name", default='run_model_system.log',
                      help="File name for logging output of model system (without directory).")

    (options, args) = parser.parse_args()
    
    resources = Resources(get_resources_from_file(options.resources_file_name))
    delete_resources_file_directory = options.delete_resources_file_directory
    skip_cache_after_each_year = options.skip_cache_after_each_year
    log_file_name = options.log_file_name
    RunModelSystem(model_system = s, 
                   resources = resources, 
                   skip_cache_after_each_year = skip_cache_after_each_year, 
                   log_file_name = log_file_name)
    if delete_resources_file_directory:
        dir = os.path.split(options.resources_file_name)[0]
        rmtree(dir)