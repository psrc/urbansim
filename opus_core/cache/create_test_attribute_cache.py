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

import os, sys

from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.attribute_type import AttributeType
from opus_core.simulation_state import SimulationState
from opus_core.resources import Resources

class CreateTestAttributeCache(object):
    """Create and populate an attribute cache with test data.
    """ 
    def create_attribute_cache_with_data(self, cache_dir, data):
        """Populate the cache_dir with the given datasets for the given years.
        
        data is a dictionary with year as key.
        The value of each year is a dictionary with dataset name as key.
        The value for each dataset name is a dictionary with attribute name as key.
        The value for each attribute name is a numpy array of values.
        
        cache_dir must exist.
        """
        
        SimulationState().set_cache_directory(cache_dir)
        attr_cache = AttributeCache()
        
        for year, datasets in data.iteritems():
            year_dir = os.path.join(cache_dir, str(year))
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)
            SimulationState().set_current_time(year)
            flt_storage = attr_cache.get_flt_storage_for_year(year)
            for dataset_name, attributes in datasets.iteritems():
                flt_storage.write_table(table_name=dataset_name, table_data=attributes)

from opus_core.tests import opus_unittest

from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self._temp_dir = mkdtemp(prefix='opus_tmp_create_test_attribute_cache')
        
    def tearDown(self):
        if os.path.exists(self._temp_dir):
            rmtree(self._temp_dir)
            
    def test(self):
        table_name = 'tests'
        year = 1000
        test_data = {
            year:{
                table_name:{
                    'attr1':array([10]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_directory = os.path.join(self._temp_dir, 'some', 'path', 'cache')
        cache_creator.create_attribute_cache_with_data(cache_directory, test_data)
        
        self.assert_(os.path.exists(cache_directory))
        
        cache_directory = os.path.join(self._temp_dir, 'somepath')
        cache_creator.create_attribute_cache_with_data(cache_directory, test_data)
        
        self.assert_(os.path.exists(cache_directory))
        if sys.byteorder=='little':
            filename = 'attr1.li4'
        else:
            filename = 'attr1.bi4'
        self.assert_(os.path.exists(os.path.join(cache_directory, 
                                                 str(year),
                                                 table_name,
                                                 filename
                                             )))
    

if __name__ == '__main__':
    opus_unittest.main()
