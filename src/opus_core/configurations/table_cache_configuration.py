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

from enthought.traits import List
from enthought.traits import Instance
from enthought.traits import HasStrictTraits

from opus_core.configurations.table_specification import TableSpecification


class TableCacheConfiguration(HasStrictTraits):
    """
    A TableCacheConfiguration provides the configuration information for caching
    tables.
    """
#===============================================================================
#   Traits
#===============================================================================
    _table_specifications = List(Instance(TableSpecification))


#===============================================================================
#   Functionality
#===============================================================================
    def __init__(self, table_specifications):
        self._table_specifications = table_specifications

    def get_specifications_of_tables_to_cache(self):
        return [i for i in self._table_specifications if i.cache_this_table]


#===============================================================================
#   Events
#===============================================================================
    pass
    
        
from opus_core.tests import opus_unittest

from random import shuffle


class TableCacheConfigurationConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_table_cache_configuration(self):
        expected_table_specifications = [
            TableSpecification(table_name='table1', chunks=5),
            TableSpecification(table_name='table2', cache_this_table=True),
            TableSpecification(table_name='table3', copy_this_table_to_previous_years=True),
            ]
            
        table_cache_configuration = TableCacheConfiguration(
            expected_table_specifications)
            
        self.assertEqual(table_cache_configuration._table_specifications,
            expected_table_specifications)

    def test_get_specifications_of_tables_to_cache(self):
        expected_tables = [
            TableSpecification(table_name='expected1', cache_this_table=True),
            TableSpecification(table_name='expected2', cache_this_table=True, chunks=2),
            TableSpecification(table_name='expected3', cache_this_table=True, chunks=3),
            ]
            
        unexpected_tables = [
            TableSpecification(table_name='unexpected1', cache_this_table=False, chunks=4),
            TableSpecification(table_name='unexpected2', cache_this_table=False, chunks=5),
            TableSpecification(table_name='unexpected3', cache_this_table=False),
            ]
            
        all_tables = expected_tables + unexpected_tables
        shuffle(all_tables)
        
        table_cache_configuration = TableCacheConfiguration(all_tables)
        
        tables_to_cache = table_cache_configuration.get_specifications_of_tables_to_cache()            
        
        for table in expected_tables:
            self.assert_(table in tables_to_cache,
                'Expected table %s not found in tables returned by '
                'get_specifications_of_tables_to_cache.' % table.table_name)
            
        for table in unexpected_tables:
            self.assert_(table not in tables_to_cache,
                'Unexpected table %s found in tables returned by '
                'get_specifications_of_tables_to_cache.' % table.table_name)
        
        number_of_tables_to_cache = len(tables_to_cache)
        expected_number_of_tables = len(expected_tables)
        self.assertEqual(number_of_tables_to_cache, expected_number_of_tables,
            'Different number of tables returned by '
            'get_specifications_of_tables_to_cache than expected! %s received '
            'instead of %s.' 
                % (number_of_tables_to_cache, expected_number_of_tables))
        
if __name__ == '__main__':
    opus_unittest.main()