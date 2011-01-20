# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree


from opus_core.resources import Resources
from opus_core.variables.attribute_type import AttributeType
from opus_core.opus_package_info import package
from opus_core.storage_factory import StorageFactory

from numpy import array

class TestWithAttributeData(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_cache_path = tempfile.mkdtemp(prefix='opus_tmp')    
        self.temp_cache_path2 = tempfile.mkdtemp(prefix='opus_tmp')
      
        self.attribute_vals = array([5,6,7,8])
        self.attribute_vals2 = array([50,60,70,80])
        self.id_vals = array([1,2,3,4])
        
        years = [1980, 1981, 1982]
        for year in years:
            self.add_attributes(year, self.attribute_vals,
                                self.attribute_vals2)

        self.attribute_vals_diff = array([10,12,14,16])
        self.attribute_vals2_diff = array([100,120,140,160])
        
        self.add_attributes(1983, self.attribute_vals_diff,
                            self.attribute_vals2_diff)        
        
    def add_attributes(self, year, attribute_vals, attribute_vals2):
        dir = os.path.join(self.temp_cache_path, repr(year))
        storage = StorageFactory().get_storage('flt_storage', storage_location=dir)
        
        storage.write_table(table_name = 'tests',
            table_data = {'id': self.id_vals,
                'attribute': attribute_vals,
                'attribute2': attribute_vals2,}
        )

        copytree(dir,  os.path.join(self.temp_cache_path2, repr(year)))
                
    def tearDown(self):
        rmtree(self.temp_cache_path)
        rmtree(self.temp_cache_path2)