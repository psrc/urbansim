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

import os, shutil

from opus_core.logger import logger
from opus_core.fork_process import ForkProcess
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.services.run_server.run_manager import RunManager as CoreRunManager

class RunManager(CoreRunManager):
    def restart_run(self, history_id, restart_year,
                    services_host_name,
                    services_database_name,
                    skip_urbansim=False,
                    skip_travel_model=False,
                    skip_cache_cleanup=False):
        """override restart_run method from core RunManager to accept argument to skip-travel-model

        Restart the specified run."""

        run_resources = self.create_run_resources_from_history(services_host_name=services_host_name,
                                                                   services_database_name=services_database_name,
                                                                   run_id=history_id,
                                                                   restart_year=restart_year)
        try:

            model_system = run_resources.get('model_system', None)
            if model_system is None:
                raise TypeError, ("The configuration must specify model_system, the"
                    " full Opus path to the model system to be used.")

            if not skip_cache_cleanup:
                # Delete 'year' folders left in the cache from a failed or stopped run (for years >= restart_year)
                year_to_purge = run_resources['years'][0]
                if skip_urbansim:
                    year_to_purge += 1
                while True:
                    dir_to_remove = os.path.join(run_resources['cache_directory'], str(year_to_purge))
                    if os.path.exists(dir_to_remove):
                        logger.log_status('Removing cache directory: %s' % dir_to_remove)
                        shutil.rmtree(dir_to_remove)
                        year_to_purge += 1
                    else:
                        break

            run_resources["skip_urbansim"] = skip_urbansim
            run_resources["skip_travel_model"] = skip_travel_model
            self.run_activity.add_row_to_history(history_id, run_resources, "restarted in %d" % run_resources['years'][0])

            exec('from %s import ModelSystem' % model_system)

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            model_system.run_multiprocess(run_resources)

            self.run_activity.add_row_to_history(history_id, run_resources, "done")

        except:
            self.run_activity.add_row_to_history(history_id, run_resources, "failed")
            raise

    def prepare_for_run(self, run_resources):
        """Prepares for simulation: caching data, create run_activity item,
           derives from run_run, except that it doesn't really start simulation.
           """        
        if self.run_activity is not None:
            history_id = self.run_activity.get_new_history_id()
            
            #add history_id to cache directory
            head, tail = os.path.split(run_resources['cache_directory'])
            cache_directory = os.path.join(head, 'run_' +str(history_id)+'.'+tail)
            ### TODO: There is no good reason to be changing Configurations!
            run_resources['cache_directory'] = cache_directory

        else:
            ### TODO: There is no good reason to be changing Configurations!
            cache_directory = run_resources['cache_directory']

        # Create baseyear cache
        if run_resources['creating_baseyear_cache_configuration'].cache_from_mysql:
            ForkProcess().fork_new_process(
                run_resources['creating_baseyear_cache_configuration'].cache_scenario_database, run_resources)
        else:
            CacheFltData().run(run_resources)
            
        # Make the cache_directory if it doesn't exist (doesn't include per-year directories).
        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

        if self.run_activity is not None:
            self.run_activity.add_row_to_history(history_id, run_resources, "started")

        return history_id
        