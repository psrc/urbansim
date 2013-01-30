# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.model_coordinators.model_system import ModelSystem as CoreModelSystem
from opus_core.model_coordinators.model_system import RunModelSystem, main
from opus_core.configuration import Configuration

class ModelSystem(CoreModelSystem):
    """
    Uses the information in configuration to run/estimate a set of models.
    """
    
    #def _run_each_year_as_separate_process(self, start_year, end_year, seed_array, resources, log_file_name='run_multiprocess.log'):
    def _run_each_year_as_separate_process(self, iyear, year, 
                                           seed=None, 
                                           resources=None, 
                                           profiler_name=None,
                                           log_file=None):
        
        skip_first_year_of_urbansim = resources.get('skip_urbansim', False)
        if iyear == 0 and skip_first_year_of_urbansim:
            return True
        #run urbansim
        success = CoreModelSystem._run_each_year_as_separate_process(self, iyear, year, 
                                                                     seed=seed, 
                                                                     resources=resources, 
                                                                     profiler_name=profiler_name,
                                                                     log_file=log_file
                                                                     )
        success = success and self._run_travel_models_from_resources_in_separate_processes(year, resources)
        return success
    
    def _run_travel_models_from_resources_in_separate_processes(self, year, resources):
        success = True
        if ('travel_model_configuration' in resources) and (not resources.get('skip_travel_model', False)):
            # tnicolai add start year to travel model config
            logger.log_status('Triggering travelmodel')
            tmc = resources['travel_model_configuration']
            tmc['start_year'] = year # end tnicolai
            success = success and self._run_travel_models_in_separate_processes(tmc, year, resources)
            logger.log_status('Leaving travelmodel')

        if 'post_year_configuration' in resources:
            success = success and self._run_travel_models_in_separate_processes(resources['post_year_configuration'], 
                                                                                year,
                                                                                resources)

        return success

    def _run_travel_models_in_separate_processes(self, year_models_dict, year, resources):
        success = True
        if year in year_models_dict:
            if 'models' in year_models_dict[year]:
                models = year_models_dict[year]['models']  #post_year_process format
            else:
                models = year_models_dict['models']  #travel model format
            for opus_path in models:
                success = self._fork_new_process(opus_path, resources, optional_args=['-y', year])
        return success                
                
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    main(ModelSystem)