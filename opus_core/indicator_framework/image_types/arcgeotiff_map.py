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

from opus_core.logger import logger
try:
    from opus_core.opus_gdal import OpusGDAL
except:
    raise ImportError, 'failed to import OpusGDAL from opus_core.opus_gdal'

import os, re, sys, time, traceback
from copy import copy
from opus_core.misc import directory_path_from_opus_path

from opus_core.indicator_framework.image_types import GeotiffMap
from opus_core.indicator_framework import AbstractIndicator

class ArcGeotiffMap(AbstractIndicator):

    def __init__(self, source_data, dataset_name, 
                 package,
                 attribute = None, 
                 years = None, operation = None, name = None, 
                 prototype_dataset = None, arcmap_args = None,
                 layer_file = '', transparency = 0, 
                 exit_after_export = False, export_type = 'jpg'):
        
       AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, operation, name)
       self.geotiff_map = GeotiffMap(source_data = source_data, 
                                     dataset_name = dataset_name, 
                                     package = package,
                                     attribute = attribute, 
                                     years = years,
                                     prototype_dataset = prototype_dataset)
       self.layer_file = layer_file
       self.transparency = transparency
       self.exit_after_export = exit_after_export
       self.export_type = export_type
       self.package = package
    
    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return self.export_type
    
    def get_visualization_shorthand(self):
        return 'arcmap'

    def get_additional_metadata(self):
        return  [('layer_file',self.layer_file),
                 ('transparency',self.transparency),
                 ('exit_after_export',self.self.exit_aafter_export),
                 ('export_type',self.export_type)]
                
    def _create_indicator(self, year):
        self.geotiff_map.source_data = self.source_data
        geotiff_path = self.geotiff_map._create_indicator(year = year)
        if not 'ARCGISHOME' in os.environ:
            message = 'Could not find arcmap on your system'
            logger.log_warning(message)
            raise Exception, message
        
        #launch arcmap
        dir = directory_path_from_opus_path('%s.indicators.geotiff_files'%self.package)
        template = os.path.join(dir,'IndicatorViewerTemplate_testing.mxt')
        exe = os.path.join(os.environ['ARCGISHOME'],'Bin','ArcMap.exe')
        
        export_path = self.source_data.get_indicator_directory()
        export_name = self.get_file_name(year = year)
        
        title = self.get_attribute_alias(year)
        
        if self.exit_after_export:
            exit_after_export = 'y'
        else:
            exit_after_export = ''

        args = '"%s" -r:"%s" -l:"%s" -x:"%s" -n:"%s" -t:"%i" -z:"%s" -c:"%s"'%(
             template,
             geotiff_path,
             self.layer_file, 
             export_path, 
             export_name,
             self.transparency, 
             title, 
             exit_after_export)        

        spawn_args = ('"%s"'%exe, args)
        os.spawnv(os.P_NOWAIT, exe, spawn_args)
        
        return self.get_file_path(year)
    

from opus_core.tests import opus_unittest
from opus_core.indicator_framework import SourceData
from opus_core.indicator_framework.utilities import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    
    def skip_test_create_indicator(self):
        #THIS TEST WON'T WORK BECAUSE WE DON'T HAVE SAMPLE ARCMAP FILES
        if not 'ARCGISHOME' in os.environ:
            pass
        else:
            indicator_path = os.path.join(self.temp_cache_path, 'indicators')
            self.assert_(not os.path.exists(indicator_path))
            
            map = ArcGeotiffMap(
                  source_data = self.source_data,
                  dataset_name = 'test', 
                  package = 'package',
                  attribute = 'package.test.attribute', 
                  prototype_dataset = None,
                  layer_file = 'D:/ArcMap_automation/6_RedClassBreaks_noZeroValues.lyr', #(optional); will default to ''
                  transparency = 0, 
                  exit_after_export = True,
                  export_type = 'jpg', 
            )

            map.create(False)
            
            self.assert_(os.path.exists(indicator_path))
            #self.assert_(os.path.exists(os.path.join(indicator_path, 'test__arcmap__attribute__1980.jpg')))
                    
if __name__ == '__main__':
    opus_unittest.main()
