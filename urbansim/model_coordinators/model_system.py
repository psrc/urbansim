#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os
from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.model_coordinators.model_system import ModelSystem as CoreModelSystem
from opus_core.model_coordinators.model_system import RunModelSystem

class ModelSystem(CoreModelSystem):
    """
    Uses the information in configuration to run/estimate a set of models.
    """
            
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
                    resources['seed'] = seed_array[iyear]
                    logger.disable_file_logging(log_file)
                    if profiler_name is not None:
                        resources["profile_filename"] = "%s_%s" % (profiler_name, year) # add year to the profile name
                    ForkProcess().fork_new_process(
                        'urbansim.model_coordinators.model_system', resources, optional_args='--log-file-name=%s' % log_file_name)
                    logger.enable_file_logging(log_file, verbose=False)
                finally:
                    logger.end_block()

            if ('travel_model_configuration' in resources) and (not resources.get('skip_travel_model', False)):
                self._run_travel_models_in_separate_processes(resources['travel_model_configuration'], year, resources)

            if 'post_year_configuration' in resources:
                self._run_travel_models_in_separate_processes(resources['post_year_configuration'], year, resources)
            iyear +=1


    def _run_travel_models_in_separate_processes(self, year_models_dict, year, resources):
        if year in year_models_dict:
            if 'models' in year_models_dict[year]:
                models = year_models_dict[year]['models']  #post_year_process format
            else:
                models = year_models_dict['models']  #travel model format
            for opus_path in models:
                ForkProcess().fork_new_process(opus_path,
                    resources, optional_args='-y %d' % year)                

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    s = ModelSystem()
    RunModelSystem(s)