# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData
from opus_gui.results_manager.run.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData
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
            )
        )
        self.source_data = SourceData(
            run_id = -1,
            cache_directory = self.temp_cache_path,
            years = [1980],
            name= 'test_source_data',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            )
        )