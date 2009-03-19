# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os

from tempfile import mktemp

from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.creating_baseyear_cache_configuration \
    import CreatingBaseyearCacheConfiguration \
    as CoreCreatingBaseyearCacheConfiguration


class CreatingBaseyearCacheConfiguration(CoreCreatingBaseyearCacheConfiguration):
    
    def __init__(self, 
            unroll_gridcells=True,
            cache_directory_root = mktemp(prefix='urbansim_tmp'),
            cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
            *args, **kwargs
            ):
        self.unroll_gridcells = unroll_gridcells
        
        CoreCreatingBaseyearCacheConfiguration.__init__(self,
            cache_directory_root = cache_directory_root,
            cache_scenario_database = cache_scenario_database,
            *args, **kwargs
            )
        

from opus_core.tests import opus_unittest


class TestCreatingBaseyearCacheConfiguration(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_creating_baseyear_cache_configuration(self):
        expected_cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database'
        expected_cache_directory_root = os.path.join('path','to','cache')
        expected_cache_from_database = True
        expected_baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = os.path.join('path','to','baseyear','cache'),
            years_to_cache = BaseyearCacheConfiguration.ALL_YEARS,
            )
        expected_tables_to_cache = [
            'table1',
            'table2',
            'table3',
            ]
        expected_tables_to_cache_nchunks = {
            'table1':5
            }
        expected_tables_to_copy_to_previous_years = {
            'table3':1995
            }
        expected_unroll_gridcells = True
        
        cbcc = CreatingBaseyearCacheConfiguration(
            cache_scenario_database = expected_cache_scenario_database,
            cache_directory_root = expected_cache_directory_root,
            cache_from_database = expected_cache_from_database,
            baseyear_cache = expected_baseyear_cache,
            tables_to_cache = expected_tables_to_cache,
            tables_to_cache_nchunks = expected_tables_to_cache_nchunks,
            tables_to_copy_to_previous_years = expected_tables_to_copy_to_previous_years,
            unroll_gridcells = expected_unroll_gridcells,
            )
        
        self.assertEqual(cbcc.cache_scenario_database, expected_cache_scenario_database)
        self.assertEqual(cbcc.cache_directory_root, expected_cache_directory_root)
        self.assertEqual(cbcc.cache_from_database, expected_cache_from_database)
        self.assertEqual(cbcc.baseyear_cache, expected_baseyear_cache)
        self.assertEqual(cbcc.tables_to_cache, expected_tables_to_cache)
        self.assertEqual(cbcc.tables_to_cache_nchunks, expected_tables_to_cache_nchunks)
        self.assertEqual(cbcc.tables_to_copy_to_previous_years, expected_tables_to_copy_to_previous_years)
        self.assertEqual(cbcc.unroll_gridcells, expected_unroll_gridcells)
        
        
if __name__ == '__main__':
    opus_unittest.main()