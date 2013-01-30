# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.model_coordinators.model_system import ModelSystem as CoreModelSystem
from urbansim.model_coordinators.model_system import ModelSystem as UrbanSimModelSystem
from opus_core.model_coordinators.model_system import main

class ModelSystem(UrbanSimModelSystem):
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

        success = True
        #run urbansim
        if iyear > 0 or not resources.get('skip_non_travel_models_first_year', False):
            success = success and CoreModelSystem._run_each_year_as_separate_process(self, iyear, year,
                                                                                     seed=seed, 
                                                                                     resources=resources, 
                                                                                     profiler_name=profiler_name,
                                                                                     log_file=log_file
                                                                                     )

        success = success and self._run_travel_models_from_resources_in_separate_processes(year, resources)
        return success
                
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    main(ModelSystem)