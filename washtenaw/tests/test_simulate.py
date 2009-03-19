# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
import tempfile
from shutil import rmtree

from opus_core.tests import opus_unittest
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState

from urbansim.simulation.run_simulation_from_mysql import RunSimulationFromMysql

from washtenaw.configs.baseline import Baseline

class SimulationTest(opus_unittest.OpusTestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.simulation = RunSimulationFromMysql()
        run_configuration = Baseline()
        run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        run_configuration['creating_baseyear_cache_configuration'].tables_to_cache = ["development_events"]
        run_configuration['scenario_database_configuration'].database_name = "washtenaw_class"
        run_configuration['seed'] = 1,#(1,1)  # always start with same random seed
        self.simulation.prepare_for_simulation(run_configuration)
        self.completed_without_error = False

    def tearDown(self):
        if self.completed_without_error:
            self.simulation.cleanup(remove_cache=True, remove_output_database=True)
            rmtree(self.temp_dir)
        else:
            logger.log_warning(
                'Problem during simulation. Not removing baseyear cache '
                'directory: %s' 
                    % SimulationState().get_cache_directory()
                )
            logger.log_warning(
                'Problem during simulation. Not removing database: %s' % 
                    self.simulation.config['estimation_database_configuration'].database_name
                )
            logger.log_warning(
                'Problem during simulation. Not removing temporary '
                'directory: %s' 
                    % self.temp_dir
                )

    def xtest_prepare_for_simulation(self):
        # do nothing, so that only the setUp procedure runs
        pass
    
    def xtest_simulation(self): # temporarily switched off, since the database data does not match the code for now
        """Checks that the simulation proceeds without caching.
        """
        self.simulation.run_simulation()
        logger.disable_file_logging()
        self.completed_without_error = True
    
if __name__ == "__main__":
    opus_unittest.main()