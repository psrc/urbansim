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

import os, re, sys, time, traceback
from copy import copy
from opus_core.indicator_framework.abstract_indicator import AbstractIndicator

from opus_core.logger import logger

class Map(AbstractIndicator):

    def __init__(self, source_data, dataset_name, 
                 attribute = None, 
                 years = None, expression = None, name = None,
                 scale = None):
        AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, expression, name)
        self.scale = scale

    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'png'
    
    def get_shorthand(self):
        return 'map'

    def _get_additional_metadata(self):
        return  [('scale',self.scale)]
    
    def _create_indicator(self, year):
        """Create a map for the given indicator, save it to the cache
        directory's 'indicators' sub-directory.
        """
        
        values = self._get_indicator(self.attribute, year)
        
        min_value = None; max_value = None
            
        if self.scale is not None:
            min_value, max_value = self.scale
          
        attribute_short = self.get_attribute_alias(year)
        #special handling for dram/empal variable name (ending with year)
        if re.search('_\d+$', attribute_short):
            attribute_short = re.compile('_\d+$').sub('', attribute_short)
            
        title = attribute_short + ' ' + str(year)
        if self.run_description is not None:
            title += '\n' + self.run_description
        
        file_path = self.get_file_path(year = year)          
    
        var_name = self.get_attribute_alias(year)
            
        dataset = self._get_dataset(year)  
        dataset.plot_map(var_name, my_title=title, file=file_path,
                         filter='urbansim.gridcell.is_fully_in_water',
                         min_value=min_value, max_value=max_value)
        
        return file_path


import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree

from opus_core.opus_package_info import package
from opus_core.configurations.dataset_description import DatasetDescription

from opus_core.indicator_framework.source_data import SourceData
from opus_core.indicator_framework.abstract_indicator import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
        
    def skip_test_create_indicator(self):
        ####NOTE: THIS TEST FAILS BECAUSE THE OPUS_CORE DATASET DOES NOT HAVE 2D ATTRIBUTES, X/Y AXES
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        map = Map(
                  source_data = self.source_data,
                  attribute = 'package.test.attribute',
                  dataset_name = 'test',
                  years = None, 
                  scale = [1,1000], 
                  name = 'my_name'
        )
                
        map.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__map__my_name__1980.png')))

if __name__ == '__main__':
    try: 
        import matplotlib
    except:
        print 'could not import matplotlib'
    else:
        opus_unittest.main()
