# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.tests import opus_unittest
import tempfile

from numpy import array
from shutil import rmtree

from opus_core.logger import logger
from opus_core.opus_package import OpusPackage
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.export_storage import ExportStorage
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory


class TestIndicators(opus_unittest.OpusIntegrationTestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_test_indicators')
        storage = StorageFactory().get_storage('dict_storage')
        
        tables_data = {
            'large_areas': {
                "large_area_id":array([1, 2, 3])
                },
            'fazes': {
                "faz_id":array([1,2,3,4]),
                "large_area_id":array([1,2,3,3]),
                },
            'zones': {
                "zone_id":array([1,2,3,4,5]),
                "faz_id":array([1,2,2,3,4]),
                },
            'gridcells': {
                "grid_id":array([1,2,3,4,5,6,7,8,9]),
                "zone_id":array([1,1,1,2,2,3,3,4,5]),
                "total_land_value":array([10, 11, 12, 13, 14, 15, 16, 17, 18]),
                "is_in_plan_type_group_residential":array([1, 1, 1, 1, 0, 0, 1, 0, 1])    
            },
           'urbansim_constants':{
                'acres': array([1.5]),
            },
        }
        
        self.year = 1000
        SimulationState().set_current_time(self.year)
        exporter = ExportStorage()
        for table_name, table_data in tables_data.iteritems():
            storage.write_table(table_name=table_name, table_data=table_data)
            exporter.export_dataset(dataset_name=table_name, 
                                    in_storage=storage, 
                                    out_storage=AttributeCache(cache_directory=self.temp_dir))
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_one_indicator(self):
        source_data = SourceData(
            cache_directory = self.temp_dir,
            run_description = 'test',
            years = [self.year],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc','urbansim','opus_core'],
                ),
            )       
                
        indicator_defs = [
            Table(
                  attribute = 'psrc.large_area.average_land_value_for_plan_type_group_residential',
                  dataset_name = 'large_area',
                  source_data = source_data,
                  ),
            ]
        
        IndicatorFactory().create_indicators(
            indicators = indicator_defs,
            display_error_box = False, 
            show_results = False)   
            

if __name__ == "__main__":
    opus_unittest.main()