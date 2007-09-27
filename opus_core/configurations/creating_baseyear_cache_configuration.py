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

from sets import Set
from tempfile import mktemp

from enthought.traits.api import Any
from enthought.traits.api import Str
from enthought.traits.api import Bool
from enthought.traits.api import Dict
from enthought.traits.api import List
from enthought.traits.api import Event
from enthought.traits.api import Trait
from enthought.traits.api import ListStr
from enthought.traits.api import Instance
from enthought.traits.api import Undefined
from enthought.traits.api import DictStrInt
from enthought.traits.api import HasStrictTraits

from opus_core.configurations.database_configuration import DatabaseConfiguration
from opus_core.configurations.table_cache_configuration import TableCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration


class CreatingBaseyearCacheConfiguration(HasStrictTraits):
    """
    A CreatingBaseyearCacheConfiguration provides the configuration information 
    for creating a baseyear cache.
    """
#===============================================================================
#   Traits
#===============================================================================
    cache_directory_root = Str
    cache_from_mysql = Bool
    baseyear_cache = Instance(BaseyearCacheConfiguration)
    cache_mysql_data = Str
    tables_to_cache = ListStr
    tables_to_cache_nchunks = DictStrInt
    tables_to_copy_to_previous_years = DictStrInt
    input_configuration = Instance(DatabaseConfiguration)
    
        
#===============================================================================
#   Functionality
#===============================================================================
    def __init__(self,
            cache_directory_root = mktemp(prefix='opus_tmp'),
            cache_mysql_data = 'opus_core.cache.cache_mysql_data',
            cache_from_mysql = True,
            baseyear_cache = Undefined,
            tables_to_cache = [],
            tables_to_cache_nchunks = {},
            tables_to_copy_to_previous_years = {},
            input_configuration = Undefined,
            ):
        
        if baseyear_cache is not Undefined:
            self.baseyear_cache = baseyear_cache
            
        if input_configuration is not Undefined:
            self.input_configuration = input_configuration
            
        if baseyear_cache is Undefined and not cache_from_mysql:
            raise TypeError("Parameter 'baseyear_cache' must be specified if "
                "parameter 'cache_from_mysql' is not True!")
                
        self.cache_directory_root = cache_directory_root
        self.cache_from_mysql = cache_from_mysql
        self.cache_mysql_data = cache_mysql_data
        self.tables_to_cache = tables_to_cache
        self.tables_to_cache_nchunks = tables_to_cache_nchunks
        self.tables_to_copy_to_previous_years = tables_to_copy_to_previous_years
        
            
#===============================================================================
#   Events
#===============================================================================
    pass
    
        
from opus_core.tests import opus_unittest

from enthought.traits.api import TraitError


class CreatingBaseyearCacheConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_creating_baseyear_cache_configuration(self):
        expected_cache_mysql_data = 'opus_core.store.cache_mysql_data'
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
            cache_mysql_data = expected_cache_mysql_data,
            cache_directory_root = expected_cache_directory_root,
            cache_from_mysql = expected_cache_from_mysql,
            baseyear_cache = expected_baseyear_cache,
            tables_to_cache = expected_tables_to_cache,
            tables_to_cache_nchunks = expected_tables_to_cache_nchunks,
            tables_to_copy_to_previous_years = expected_tables_to_copy_to_previous_years,
            )
        
        self.assertEqual(cbcc.cache_mysql_data, expected_cache_mysql_data)
        self.assertEqual(cbcc.cache_directory_root, expected_cache_directory_root)
        self.assertEqual(cbcc.cache_from_mysql, expected_cache_from_mysql)
        self.assertEqual(cbcc.baseyear_cache, expected_baseyear_cache)
        self.assertEqual(cbcc.tables_to_cache, expected_tables_to_cache)
        self.assertEqual(cbcc.tables_to_cache_nchunks, expected_tables_to_cache_nchunks)
        self.assertEqual(cbcc.tables_to_copy_to_previous_years, expected_tables_to_copy_to_previous_years)
        
        
if __name__=='__main__':
    opus_unittest.main()