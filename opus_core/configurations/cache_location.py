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

from time import strftime
from time import localtime

from enthought.traits import HasStrictTraits, Str, Bool, Event


class CacheLocation(HasStrictTraits):
    """A CacheLocation provides cache directory information."""

#===============================================================================
#   Traits
#===============================================================================
    cache_directory_root = Str
    cache_directory = Str
    _default_cache_directory = Str
    
    use_standard_template_for_cache_directory = Event
    
#===============================================================================
#   Functionality
#===============================================================================
    def __init__(self, cache_directory_root, cache_directory=None):
        self._default_cache_directory = '%Y_%m_%d_%H_%M'
        
        if cache_directory is None:
            self.cache_directory = self._default_cache_directory
        else:
            self.cache_directory = cache_directory
        
        self.cache_directory_root = cache_directory_root


    def get_cache_location(self):
        return os.path.join(self.cache_directory_root,
            strftime(self.cache_directory, localtime()))
        
        
#===============================================================================
#    Events
#===============================================================================
    def _use_standard_template_for_cache_directory_fired(self):
        self.cache_directory = self._default_cache_directory


from opus_core.tests import opus_unittest


class CacheLocationTests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_cache_location(self):
        expected_cache_directory_root = 'path'
        expected_cache_directory = 'dir'
        cache_loc = CacheLocation(
            cache_directory_root = expected_cache_directory_root,
            cache_directory = expected_cache_directory,
            )
            
        self.assertEqual(cache_loc.cache_directory_root, 
            expected_cache_directory_root)
            
        self.assertEqual(cache_loc.cache_directory,
            expected_cache_directory)
            
    def test_get_cache_location(self):
        expected_cache_directory_root = 'path'
        expected_cache_directory = 'dir'
        cache_loc = CacheLocation(
            cache_directory_root = expected_cache_directory_root,
            cache_directory = expected_cache_directory,
            )
            
        expected_location = os.path.join(expected_cache_directory_root,
            expected_cache_directory)
            
        self.assertEqual(cache_loc.get_cache_location(), expected_location)
        

if __name__=='__main__':
    opus_unittest.main()