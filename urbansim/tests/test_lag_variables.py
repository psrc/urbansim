# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest

from shutil import copytree

from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.session_configuration import SessionConfiguration

from urbansim.model_coordinators.cache_scenario_database import CacheScenarioDatabase
from urbansim.data.test_cache_configuration import TestCacheConfiguration
        
class TestLagVariables(opus_unittest.OpusTestCase):
    
    def setUp(self):
        self.config = TestCacheConfiguration()

        self.simulation_state = SimulationState(new_instance=True)
        SessionConfiguration(self.config, new_instance=True, 
                             package_order=['urbansim', 'opus_core'],
                             in_storage=AttributeCache()) 

        self.base_year = self.config['base_year']
        creating_baseyear_cache_configuration = self.config['creating_baseyear_cache_configuration']
        
        self.simulation_state.set_current_time(self.base_year)

        cache_directory = self.simulation_state.get_cache_directory()
        copytree(os.path.join(creating_baseyear_cache_configuration.baseyear_cache.existing_cache_to_copy, 
                              str(self.base_year)),
                 os.path.join(cache_directory, str(self.base_year)))
        cacher = CacheScenarioDatabase()
        cacher.prepare_data_before_baseyear(cache_directory, self.base_year, creating_baseyear_cache_configuration)
        
        self.config['cache_directory'] = cache_directory
        
        cache_storage = AttributeCache().get_flt_storage_for_year(self.base_year)
        cache_directory = self.simulation_state.get_cache_directory()
        flt_directory = os.path.join(cache_directory, str(self.base_year))
        self.gridcell = DatasetFactory().get_dataset('gridcell', 
            package='urbansim',
            subdir='datasets',
            arguments={'in_storage':StorageFactory().get_storage('flt_storage', storage_location=flt_directory)}
            )
        
    def tearDown(self):
        self.simulation_state.remove_singleton(delete_cache=True)
        
    def test_lag_variables(self):
        """Test lag variables"""
        # A weak test that computing a lag variable on a realistic dataset does not crash.
        self.gridcell.compute_variables('urbansim.gridcell.n_recent_transitions_to_developed',
                                        resources=self.config)
       
        # The following tests are fragile, since they need to know exactly what values are being
        # subtracted, and ignore any negative amount that is truncated at zero.
        # If you change the "subset" dataset to a different region, you will
        # have to update the expected value.
        self.gridcell.compute_variables('urbansim.gridcell.commercial_sqft',
                                        resources=self.config)
        self.gridcell.compute_variables('urbansim.gridcell.commercial_sqft_lag1',
                                        resources=self.config)
        self.gridcell.compute_variables('urbansim.gridcell.commercial_sqft_lag2',
                                        resources=self.config)

        sqft = self.gridcell.get_attribute('commercial_sqft').sum()
        sqft_lag1 = self.gridcell.get_attribute('commercial_sqft_lag1').sum()
        sqft_lag2 = self.gridcell.get_attribute('commercial_sqft_lag2').sum()

        logger.log_status('sqft = %s' % sqft)
        logger.log_status('sqft_lag1 = %s' % sqft_lag1)
        logger.log_status('sqft_lag2 = %s' % sqft_lag2)
        logger.log_status('base_year = %s' % self.base_year)
        
        self.assertEqual(self.base_year, SimulationState().get_current_time())
        self.assertEqual(sqft, sqft_lag1)
        self.assertEqual(578+2083+1103+87, sqft_lag1 - sqft_lag2)
       
        # Do lag variables produce different results for derived attributes?
        self.gridcell.compute_variables('urbansim.gridcell.n_recent_development_projects',
                                        resources=self.config)
        self.gridcell.compute_variables('urbansim.gridcell.n_recent_development_projects_lag1',
                                        resources=self.config)
        n_recent_projects = self.gridcell.get_attribute('n_recent_development_projects').sum()
        n_recent_projects_lag1 = self.gridcell.get_attribute('n_recent_development_projects_lag1').sum()
        
        self.assertEqual(n_recent_projects, 11)
        self.assertEqual(n_recent_projects_lag1, 15)
       
        # Do lag_variables produce different results for derived attributes without lags?
        self.gridcell.compute_variables('urbansim.gridcell.ln_commercial_sqft',
                                        resources=self.config)
        self.gridcell.compute_variables('urbansim.gridcell.ln_commercial_sqft_lag4',
                                        resources=self.config)
        sqft = self.gridcell.get_attribute('ln_commercial_sqft').sum()
        sqft_lag4 = self.gridcell.get_attribute('ln_commercial_sqft_lag4').sum()
        
        self.assertNotEqual(sqft, sqft_lag4)

        
if __name__ == "__main__":
    opus_unittest.main()