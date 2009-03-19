# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os, shutil

from opus_core.logger import logger
from opus_core.services.run_server.run_manager import RunManager as CoreRunManager

class RunManager(CoreRunManager):
    def restart_run(self, run_id, restart_year,
                    project_name,
                    skip_urbansim=False,
                    skip_travel_model=False,
                    skip_cache_cleanup=False):
        """override restart_run method from core RunManager to accept argument to skip-travel-model

        Restart the specified run."""
        self.update_environment_variables(run_resources = {'project_name':project_name}) 
        run_resources = self.create_run_resources_from_history(run_id=run_id,
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
            self.add_row_to_history(run_id, run_resources, "restarted in %d" % run_resources['years'][0])

            exec('from %s import ModelSystem' % model_system)

            # add years run
            model_system = ModelSystem()

            if 'base_year' not in run_resources:
                run_resources['base_year'] = run_resources['years'][0] - 1

            model_system.run_multiprocess(run_resources)

            self.add_row_to_history(run_id, run_resources, "done")

        except:
            self.add_row_to_history(run_id, run_resources, "failed")
            raise