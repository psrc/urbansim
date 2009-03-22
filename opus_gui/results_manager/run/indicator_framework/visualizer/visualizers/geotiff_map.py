# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
try:
    from opus_core.opus_gdal import OpusGDAL
except:
    raise ImportError, 'failed to import OpusGDAL from opus_core.opus_gdal'

import os, re, sys, time, traceback
from copy import copy
from opus_core.misc import directory_path_from_opus_path
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.abstract_visualization import Visualization
    
class GeotiffMap(Visualization):

    def __init__(self, source_data, dataset_name,
                 attribute = None, 
                 years = None, 
                 operation = None, 
                 name = None,
                 package = None,
                 prototype_dataset = None,
                 storage_location = None):
        
        Visualizer.__init__(self, source_data, 
                                   dataset_name, [attribute], 
                                   years, operation, name,
                                   storage_location)
        
        
        
        if prototype_dataset is None:
            dir = directory_path_from_opus_path('%s.indicators.geotiff_files'%package)
            #todo: check indicator package and find appropriate prototype image
            prototype_dataset = os.path.join(dir,'idgrid.tif')
            if not os.path.exists(prototype_dataset):
                raise 'Error: %s does not exist. Cannot compute GeotiffMap'%prototype_dataset
        
        self.prototype_dataset = prototype_dataset
        
    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'tif'
    
    def get_visualization_shorthand(self):
        return 'geotiff'
    
    def get_additional_metadata(self):
        return  {'prototype_dataset':self.prototype_dataset}
    
    def _create_indicator(self, year):
        """Create a geotiff image for the given indicator"""            
 
        values = self._get_indicator(year, wrap = False)
        
        dataset = self._get_dataset(year = year)
        values_in_2d_array = dataset.get_2d_attribute(
              attribute=None,
              attribute_data=values,
              )
        
        file_name = self.get_file_name(year = year)   
        indicator_directory = self.get_storage_location()
        
        OpusGDAL().input_numpy_array_output_geotiff(
             values_in_2d_array,
             prototype_dataset = self.prototype_dataset,
             output_directory = indicator_directory,
             output_file_name = file_name)
        
        return self.get_file_path(year)
    
from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.maker.source_data import SourceData
from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    
    def skip_test_create_indicator(self):
        ####NOTE: THIS TEST FAILS BECAUSE THE OPUS_CORE DATASET DOES NOT HAVE 2D ATTRIBUTES, X/Y AXES
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        map = GeotiffMap(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
                  dataset_name = 'test',
                  prototype_dataset = None,
                  years = None
        )
        
        map.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__geotiff__attribute__1980.tif')))
                
if __name__ == '__main__':
    try: import gdal
    except: print "Could not import gdal library."
    else:
        opus_unittest.main()
