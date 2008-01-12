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

from enthought.traits.api import ListInt, Str, Trait, Constant, HasStrictTraits


class BaseyearCacheConfiguration(HasStrictTraits):
    """A BaseyearCacheConfiguration provides the configuration information 
    of the directory and years to cache."""

#===============================================================================
#   Constants
#===============================================================================
    ALL_YEARS = 'all'

#===============================================================================
#   Traits
#===============================================================================
    existing_cache_to_copy = Str
    years_to_cache = Trait(ALL_YEARS, ALL_YEARS, ListInt)
    
#===============================================================================
#   Functionality
#===============================================================================

    def __init__(self, existing_cache_to_copy, years_to_cache=ALL_YEARS):
        self.existing_cache_to_copy = existing_cache_to_copy
        self.years_to_cache = years_to_cache
        
        
#===============================================================================
#   Events
#===============================================================================
    pass
        

import os
from opus_core.tests import opus_unittest

from enthought.traits.api import TraitError


class DatabaseConfigurationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_baseyear_configuration(self):
        expected_existing_cache_to_copy = os.path.join('path', 'to', 'cache')
        expected_years_to_cache = [1999, 2000, 2001, 2002, 2003, 2004]
        
        bcc = BaseyearCacheConfiguration(
            existing_cache_to_copy = expected_existing_cache_to_copy,
            years_to_cache = expected_years_to_cache,
            )
        
        self.assertEqual(bcc.existing_cache_to_copy, expected_existing_cache_to_copy)
        self.assertEqual(bcc.years_to_cache, expected_years_to_cache)

        expected_existing_cache_to_copy = os.path.join('path', 'to', 'other', 'cache')
        expected_years_to_cache = range(1, 2000)

        bcc.existing_cache_to_copy = expected_existing_cache_to_copy
        bcc.years_to_cache = expected_years_to_cache
        
        self.assertEqual(bcc.existing_cache_to_copy, expected_existing_cache_to_copy)
        self.assertEqual(bcc.years_to_cache, expected_years_to_cache)
        
        try:
            bcc.years_to_cache = 'a'
        except TraitError:
            pass
        else:
            self.fail("The years_to_cache accepted something other than a"
                " list of integers or BaseyearCacheConfiguration.ALL_YEARS!")

        try:
            bcc.years_to_cache = BaseyearCacheConfiguration.ALL_YEARS
        except TraitError:
            self.fail("The years_to_cache did not accept "
                "BaseyearCacheConfiguration.ALL_YEARS")
            

        try:
            bcc.years_to_cache = ['a', 1900]
        except TraitError:
            pass
        else:
            self.fail('The years_to_cache accepted a list with '
                'non-integers!')

        try:
            bcc.years_to_cache = [1, 1900]
        except TraitError:
            self.fail('The years_to_cache did not accept a list of integers!')


if __name__=='__main__':
    opus_unittest.main()