#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
import tempfile
from shutil import rmtree

from opus_core.tests import opus_unittest
from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_core.misc import get_distinct_list
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.misc import does_database_server_exist_for_this_hostname

from urbansim.simulation.run_simulation_from_mysql import RunSimulationFromMysql

from washtenaw.configs.baseline import Baseline


if does_database_server_exist_for_this_hostname(
        module_name = __name__, 
        hostname = Baseline()['scenario_database_configuration'].host_name):
    
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