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
from tempfile import mktemp

from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration


class CreatingBaseyearCacheConfiguration(object):
    """
    A CreatingBaseyearCacheConfiguration provides the configuration information 
    for creating a baseyear cache.
    """

    def __init__(self,
            cache_directory_root = mktemp(prefix='opus_tmp'),
            cache_scenario_database = 'opus_core.cache.cache_scenario_database',
            cache_from_mysql = True,
            baseyear_cache = None,
            tables_to_cache = [],
            tables_to_cache_nchunks = {},
            tables_to_copy_to_previous_years = {},
            scenario_database_configuration = None,
            ):
            
        if baseyear_cache is None and not cache_from_mysql:
            raise TypeError("Parameter 'baseyear_cache' must be specified if "
                "parameter 'cache_from_mysql' is not True!")
        
        self.scenario_database_configuration = scenario_database_configuration
        self.baseyear_cache = baseyear_cache
        self.cache_directory_root = cache_directory_root
        self.cache_from_mysql = cache_from_mysql
        self.cache_scenario_database = cache_scenario_database
        self.tables_to_cache = tables_to_cache
        self.tables_to_cache_nchunks = tables_to_cache_nchunks
        self.tables_to_copy_to_previous_years = tables_to_copy_to_previous_years
    
        
from opus_core.tests import opus_unittest

class CreatingBaseyearCacheConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_creating_baseyear_cache_configuration(self):
        expected_cache_scenario_database = 'opus_core.store.cache_scenario_database'
        expected_cache_directory_root = os.path.join('path','to','cache')
        expected_cache_from_mysql = True
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
        
        cbcc = CreatingBaseyearCacheConfiguration(
            cache_scenario_database = expected_cache_scenario_database,
            cache_directory_root = expected_cache_directory_root,
            cache_from_mysql = expected_cache_from_mysql,
            baseyear_cache = expected_baseyear_cache,
            tables_to_cache = expected_tables_to_cache,
            tables_to_cache_nchunks = expected_tables_to_cache_nchunks,
            tables_to_copy_to_previous_years = expected_tables_to_copy_to_previous_years,
            )
        
        self.assertEqual(cbcc.cache_scenario_database, expected_cache_scenario_database)
        self.assertEqual(cbcc.cache_directory_root, expected_cache_directory_root)
        self.assertEqual(cbcc.cache_from_mysql, expected_cache_from_mysql)
        self.assertEqual(cbcc.baseyear_cache, expected_baseyear_cache)
        self.assertEqual(cbcc.tables_to_cache, expected_tables_to_cache)
        self.assertEqual(cbcc.tables_to_cache_nchunks, expected_tables_to_cache_nchunks)
        self.assertEqual(cbcc.tables_to_copy_to_previous_years, expected_tables_to_copy_to_previous_years)
        
        
if __name__=='__main__':
    opus_unittest.main()