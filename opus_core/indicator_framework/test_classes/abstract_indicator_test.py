#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.tests import opus_unittest
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

class AbstractIndicatorTest(TestWithAttributeData):
    def setUp(self):
        TestWithAttributeData.setUp(self)
        
        self.cross_scenario_source_data = SourceData(
            cache_directory = self.temp_cache_path,
            comparison_cache_directory = self.temp_cache_path2,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            )
        )
        self.source_data = SourceData(
            cache_directory = self.temp_cache_path,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            )
        )