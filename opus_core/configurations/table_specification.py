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

from enthought.traits import Int
from enthought.traits import Str
from enthought.traits import Bool
from enthought.traits import HasStrictTraits 


class TableSpecification(HasStrictTraits):
    """
    A TableSpecification provides information about a table to cache, such as
    the name of the table, whether to cache the table or copy it to a previous 
    year, or the number of chunks.
    """

#===============================================================================
#   Traits
#===============================================================================
    table_name = Str
    copy_this_table_to_previous_years = Bool
    how_many_years = Int
    cache_this_table = Bool
    chunks = Int
    
    
#===============================================================================
#   Functionality
#===============================================================================
    def __init__(self, table_name, copy_this_table_to_previous_years=False, 
            how_many_years=0, cache_this_table=False, chunks=1):
        self.table_name = table_name
        self.copy_this_table_to_previous_years = copy_this_table_to_previous_years
        self.how_many_years = how_many_years
        self.cache_this_table = cache_this_table
        self.chunks = chunks
    
        
#===============================================================================
#   Events
#===============================================================================
    pass
    
        
from opus_core.tests import opus_unittest


class TableSpecificationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_table_specification(self):
        expected_table_name = 'Bob'
        expected_copy_this_table_to_previous_years = True
        expected_how_many_years = 1800
        expected_cache_this_table = True
        expected_chunks = 50
        
        table_specification = TableSpecification(
            table_name=expected_table_name,
            cache_this_table=expected_cache_this_table,
            chunks=expected_chunks,
            copy_this_table_to_previous_years =
                expected_copy_this_table_to_previous_years,
            how_many_years = expected_how_many_years,
            )
            
        self.assertEqual(table_specification.table_name,
            expected_table_name)
        self.assertEqual(table_specification.cache_this_table,
            expected_cache_this_table)
        self.assertEqual(table_specification.chunks,
            expected_chunks)
        self.assertEqual(table_specification.copy_this_table_to_previous_years,
            expected_copy_this_table_to_previous_years)
        self.assertEqual(table_specification.how_many_years,
            expected_how_many_years)
            

if __name__=='__main__':
    opus_unittest.main()