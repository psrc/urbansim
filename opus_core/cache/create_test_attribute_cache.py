# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys

from opus_core.store.attribute_cache import AttributeCache
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
        
        for year, datasets in data.items():
            year_dir = os.path.join(cache_dir, str(year))
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)
            SimulationState().set_current_time(year)
            flt_storage = attr_cache.get_flt_storage_for_year(year)
            for dataset_name, attributes in datasets.items():
                flt_storage.write_table(table_name=dataset_name, table_data=attributes)

from opus_core.tests import opus_unittest
from opus_core.tests.utils.cache_extension_replacements import replacements
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
        
        self.assertTrue(os.path.exists(cache_directory))
        
        cache_directory = os.path.join(self._temp_dir, 'somepath')
        cache_creator.create_attribute_cache_with_data(cache_directory, test_data)
        
        self.assertTrue(os.path.exists(cache_directory))
        # filename is e.g. attr1.li4 for little-endian 32 bit architecture
        filename = 'attr1.%(endian)si%(bytes)u' % replacements
        self.assertTrue(os.path.exists(os.path.join(cache_directory, 
                                                 str(year),
                                                 table_name,
                                                 filename
                                             )))
    

if __name__ == '__main__':
    opus_unittest.main()
