# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree

from stat import S_IWRITE, S_IREAD

from numpy import array

from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.opus_package_info import package
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

from urbansim.model_coordinators.unroll_gridcells import UnrollGridcells

from urbansim.data.test_cache_configuration import TestCacheConfiguration

class TestGridcellUnrolling(opus_unittest.OpusTestCase):
    
    def setUp(self):
        run_configuration = TestCacheConfiguration()
        SimulationState(new_instance=True)
        SessionConfiguration(run_configuration, new_instance=True, 
                             package_order=['urbansim', 'opus_core'],
                             in_storage=AttributeCache())
        
        self.base_year = run_configuration['base_year']
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
        # Use the test cache.
        opus_core_path = package().get_opus_core_path()
        test_cache_path = os.path.join(opus_core_path, 'data', 'test_cache')
        new_cache_path = os.path.join(self.temp_dir, 'cache')
        copytree(test_cache_path, new_cache_path)
        
        # Make sure the copied files are writable.
        for (dirpath, dirnames, filenames) in os.walk(new_cache_path):
            for file_name in filenames:
                full_path = os.path.join(dirpath, file_name)
                os.chmod(full_path, S_IWRITE | S_IREAD)
        
        SimulationState().set_cache_directory(new_cache_path)
        SimulationState().set_current_time(self.base_year)
        self.config = Resources(run_configuration)
        
        cache_directory = SimulationState().get_cache_directory()
        self.assertEqual(self.temp_dir, os.path.split(cache_directory)[0])

    def tearDown(self):
        SimulationState().remove_singleton(delete_cache=True)
        rmtree(self.temp_dir)
        
    def test_gridcell_unrolling(self):
        """Checks that the unrolling of the gridcells by CacheScenarioDatabase worked correctly.
        """
        cache_directory = SimulationState().get_cache_directory()
        gridcells = SessionConfiguration().get_dataset_from_pool('gridcell')
        development_event_history = SessionConfiguration().get_dataset_from_pool('development_event_history')
        unroller = UnrollGridcells()
        unroller.unroll_gridcells_to_cache(gridcells, development_event_history,
                                           cache_directory, self.base_year)
                   
        self.assertEqual(self.temp_dir, os.path.split(cache_directory)[0])
        
        gridcell = {}
        for year in [1976, 1977, 1979, 1980]:
            #current_year = SimulationState().get_current_time()
            #SimulationState().set_current_time(year)
            #gridcell[year] = SessionConfiguration().get_dataset_from_pool('gridcell')
            #SimulationState().set_current_time(current_year)
            flt_directory = os.path.join(cache_directory, str(year))
            gridcell[year] = DatasetFactory().get_dataset('gridcell', 
                package='urbansim',
                subdir='datasets',
                arguments={'in_storage':StorageFactory().get_storage('flt_storage', storage_location=flt_directory)}
                )
        diff = gridcell[1980].get_attribute('residential_units') - gridcell[1979].get_attribute('residential_units')
        self.assertEqual(1, sum(diff))
        diff = gridcell[1977].get_attribute('commercial_sqft') - gridcell[1976].get_attribute('commercial_sqft')
        self.assertEqual(2255+199+332+2785, sum(diff))
        
    def tmp_skip_test_gridcell_unrolling_changes_development_type_id(self):
        """Does unrolling update development_type_id?
        """
        # Force one grid cell to be "vacant", so can check that development_type_id changes.
        cache_directory = SimulationState().get_cache_directory()
        flt_directory = os.path.join(cache_directory, str(self.base_year))
        development_event_history = DatasetFactory().get_dataset('development_event_history', 
            package='urbansim',
            subdir='datasets',
            arguments={'in_storage':StorageFactory().get_storage('flt_storage', storage_location=flt_directory)}
            )
        changed_grid_id = 10123
        new_row = {
            'grid_id':array([changed_grid_id]),
            'scheduled_year':array([self.base_year - 1]),
            'residential_units':array([1000]),
            'commercial_sqft':array([10000000]),
            'industrial_sfft':array([10000000]),
            'governmental_sqft':array([10000000]),
            'starting_development_type_id':array([1000]),
            }
        development_event_history.add_elements(new_row, require_all_attributes=False)
        development_event_history.flush_dataset()

        gridcells = SessionConfiguration().get_dataset_from_pool('gridcell')
        development_event_history = SessionConfiguration().get_dataset_from_pool('development_event_history')
        unroller = UnrollGridcells()
        unroller.unroll_gridcells_to_cache(gridcells, development_event_history,
                                           cache_directory, self.base_year)
                   
        cache_directory = SimulationState().get_cache_directory()
        self.assertEqual(self.temp_dir, os.path.split(cache_directory)[0])
        
        gridcell = {}
        for year in [1978, 1979]:
            flt_directory = os.path.join(cache_directory, str(year))
            gridcell[year] = DatasetFactory().get_dataset('gridcell', 
                package='urbansim',
                subdir='datasets',
                arguments={'in_storage':StorageFactory().get_storage('flt_storage', storage_location=flt_directory)}
                )
        self.assertEqual(gridcell[1978].get_attribute_by_id('development_type_id', changed_grid_id),
                         1000)
        self.assertNotEqual(gridcell[1979].get_attribute_by_id('development_type_id', changed_grid_id),
                            gridcell[1978].get_attribute_by_id('development_type_id', changed_grid_id))
        
if __name__ == "__main__":
    opus_unittest.main()
