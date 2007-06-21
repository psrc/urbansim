#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree

from opus_core.indicator_framework import SourceData
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.resources import Resources
from opus_core.variables.attribute_type import AttributeType
from opus_core.opus_package_info import package
from opus_core.storage_factory import StorageFactory

from numpy import array

class AbstractIndicatorTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_cache_path = tempfile.mkdtemp(prefix='opus_tmp')    
        self.temp_cache_path2 = tempfile.mkdtemp(prefix='opus_tmp')
      
        baseyear_dir = os.path.join(self.temp_cache_path, '1980')
        storage = StorageFactory().get_storage('flt_storage', storage_location=baseyear_dir)
        storage.write_dataset(Resources({
           'out_table_name': 'tests',
           'values': {
               'id': array([1,2,3,4]),
               'attribute': array([5,6,7,8]),
               'attribute2': array([50,60,70,80])
               },
           'attrtype':{
               'id': AttributeType.PRIMARY,
               'attribute': AttributeType.PRIMARY,
               'attribute2': AttributeType.PRIMARY, 
               }
           }))
        
        copytree(baseyear_dir,  os.path.join(self.temp_cache_path2, '1980'))
        
        self.cross_scenario_source_data = SourceData(
            cache_directory = self.temp_cache_path,
            comparison_cache_directory = self.temp_cache_path2,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )
        self.source_data = SourceData(
            cache_directory = self.temp_cache_path,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )
                
    def tearDown(self):
        rmtree(self.temp_cache_path)
        rmtree(self.temp_cache_path2)