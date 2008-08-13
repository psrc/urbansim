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
from opus_gui.results.indicator_framework.maker.source_data import SourceData
from opus_gui.results.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

class AbstractIndicatorTest(TestWithAttributeData):
    def setUp(self):
        TestWithAttributeData.setUp(self)
        
        self.cross_scenario_source_data = SourceData(
            cache_directory = self.temp_cache_path,
            run_id = -1,
            comparison_cache_directory = self.temp_cache_path2,
            years = [1980],
            name = 'test_cross_scenario_source_data',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )
        self.source_data = SourceData(
            run_id = -1,
            cache_directory = self.temp_cache_path,
            years = [1980],
            name= 'test_source_data',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )