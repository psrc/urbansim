# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

class BaseyearCacheConfiguration(object):
    """A BaseyearCacheConfiguration provides the configuration information 
    of the directory and years to cache."""

    ALL_YEARS = 'all'

    def __init__(self, existing_cache_to_copy, years_to_cache=ALL_YEARS):
        self.existing_cache_to_copy = existing_cache_to_copy
        self.years_to_cache = years_to_cache
        
        
import os
from opus_core.tests import opus_unittest

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


if __name__=='__main__':
    opus_unittest.main()