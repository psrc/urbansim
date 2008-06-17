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

# Test that the Eugene simulation runs without crashing for 2 years (using the old format dictionary based configurations)
# This version also reads the input data from the MySQL database, rather than a cache

import os
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree

from opus_core.logger import logger
from eugene.configs.baseline import Baseline

from urbansim.simulation.run_simulation_from_mysql import RunSimulationFromMysql


class SimulationTest(opus_unittest.OpusTestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.simulation = RunSimulationFromMysql()
        run_configuration = Baseline()
        run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
        run_configuration['cache_directory'] = os.path.join(self.temp_dir, 'eugene')
        self.simulation.prepare_for_simulation(run_configuration)
    def tearDown(self):
        self.simulation.cleanup(remove_cache=True, remove_output_database=True)
        rmtree(self.temp_dir)
           
    def test_simulation(self):
        """Checks that the simulation proceeds without crashing.
        """
        self.simulation.run_simulation()
        logger.disable_file_logging()
       
if __name__ == "__main__":
    opus_unittest.main()