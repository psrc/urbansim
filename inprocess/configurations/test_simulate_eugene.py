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

# this is taken from eugene/tests/test_simulate.py -- it uses an xml configuration
# instead of the dictionary-based one

import os
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree

from opus_core.logger import logger
from opus_core.simulation_state import SimulationState

# from eugene.configs.baseline import Baseline
from inprocess.configurations.xml_configuration import XMLConfiguration
from urbansim.simulation.run_simulation_from_mysql import RunSimulationFromMysql

# find the directory containing the eugene xml configurations
inprocessdir = __import__('inprocess').__path__[0]
path = os.path.join(inprocessdir, 'configurations', 'projects', 'eugene_gridcell.xml')

class SimulationTest(opus_unittest.OpusTestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.simulation = RunSimulationFromMysql()
        # run_configuration = Baseline()
        run_configuration = XMLConfiguration(path).get_run_configuration('Eugene baseline')
        run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        run_configuration['cache_directory'] = os.path.join(self.temp_dir, 'eugene')
        self.simulation.prepare_for_simulation(run_configuration)
        self.completed_without_error = False

    def tearDown(self):
        if self.completed_without_error:    
            self.simulation.cleanup(remove_cache=True, remove_output_database=True)
            rmtree(self.temp_dir)
        else:
            logger.log_warning('Problem during simulation. Not removing baseyear cache directory: %s' % SimulationState().get_cache_directory())
            if 'output_configuration' in self.simulation.config:
                logger.log_warning('Problem during simulation. Not removing database: %s' % self.simulation.config['output_configuration'].database_name)
            logger.log_warning('Problem during simulation. Not removing temporary directory: %s' % self.temp_dir)
   
    def test_simulation(self):
        """Checks that the simulation proceeds without caching.
        """
        self.simulation.run_simulation()
        logger.disable_file_logging()
        self.completed_without_error = True
       
if __name__ == "__main__":
    opus_unittest.main()