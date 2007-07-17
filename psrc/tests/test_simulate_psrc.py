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
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree

from opus_core.logger import logger
from opus_core.misc import get_distinct_list
from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.simulation_state import SimulationState
from opus_core.misc import does_database_server_exist_for_this_hostname

from urbansim.simulation.run_simulation_from_mysql import RunSimulationFromMysql

from psrc.configs.subset_configuration import SubsetConfiguration


if does_database_server_exist_for_this_hostname(
        module_name = __name__, 
        hostname = SubsetConfiguration()['input_configuration'].host_name):

    class PSRCSimulationTest(opus_unittest.OpusTestCase):
        
        def setUp(self):
            self.simulation = RunSimulationFromMysql()
            self.run_configuration = SubsetConfiguration()
            self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
            self.run_configuration['creating_baseyear_cache_configuration'].cache_directory_root = self.temp_dir
            self.run_configuration['seed'] = 1,#(1,1)  # always start with same random seed
            self.simulation.prepare_for_simulation(self.run_configuration)
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
    
            
        def test_psrc_opus_simulation(self):
            """Checks that the simulation proceeds without caching.
            """
            self.simulation.run_simulation()
            self._check_simulation_produces_changes()
            logger.disable_file_logging()
            self.completed_without_error = True
            
        def _get_data(self, year, dataset_name, attribute_name):
            current_year = SimulationState().get_current_time()
            SimulationState().set_current_time(year)
            dataset = DatasetFactory().get_dataset(dataset_name, package='urbansim',
                                                   subdir='datasets',
                                                   arguments={'in_storage':AttributeCache()})
            dataset.compute_variables(attribute_name,
                                      resources=self.simulation.config)
            variable_name = VariableName(attribute_name)
            short_name = variable_name.get_short_name()
            
            values = dataset.get_attribute(short_name)
            SimulationState().set_current_time(current_year)
            return values
            
        def _check_simulation_produces_changes(self):
            # Test for primary attribute:
            # Does _lag2 in 2002 get the 2000 data, when the 2002 data is different from the 2000 data?
            primary_attributes_that_should_have_changed = [
                'urbansim.gridcell.commercial_sqft',
                'urbansim.gridcell.industrial_sqft',
                'urbansim.gridcell.residential_units',
                ]
            
            for primary_attribute_that_should_have_changed in primary_attributes_that_should_have_changed:
                value_2000 = self._get_data(2000, 'gridcell', primary_attribute_that_should_have_changed).sum()
                value_2002 = self._get_data(2002, 'gridcell', primary_attribute_that_should_have_changed).sum()
                
                self.assertNotEqual(value_2002, value_2000, msg='expected %s <> %s' % (value_2002, value_2000))
        
                # confirm lag
                value_2002_lag2 = self._get_data(2002, 'gridcell', '%s_lag2' % primary_attribute_that_should_have_changed).sum()
                self.assertEqual(value_2002_lag2, value_2000, msg='expected %s == %s' % (value_2002_lag2, value_2000))
    
            # Test for derived attribute:
            sqft_2000 = self._get_data(2000, 'gridcell', 'urbansim.gridcell.commercial_and_industrial_sqft').sum()
            sqft_2002 = self._get_data(2002, 'gridcell', 'urbansim.gridcell.commercial_and_industrial_sqft').sum()
            self.assertNotEqual(sqft_2002, sqft_2000, msg='expected %s <> %s' % (sqft_2002, sqft_2000))
    
            sqft_2002_lag2 = self._get_data(2002, 'gridcell', 'urbansim.gridcell.commercial_and_industrial_sqft_lag2').sum()
            self.assertEqual(sqft_2002_lag2, sqft_2000, msg='expected %s == %s' % (sqft_2002_lag2, sqft_2000))
            
           
if __name__ == "__main__":
    opus_unittest.main()