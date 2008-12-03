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

import os, re, sys, time, traceback
from copy import copy
from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator

from opus_core.logger import logger

class Map(AbstractIndicator):

    def __init__(self, source_data, dataset_name, 
                 attribute = None, 
                 years = None, operation = None, name = None,
                 scale = None,
                 storage_location = None):
        if dataset_name == 'parcel':
            raise Exception('Cannot create a Matplotlib map for parcel dataset. Please plot at a higher geographic aggregation')
        AbstractIndicator.__init__(self, source_data, dataset_name, 
                                   [attribute], years, operation, name,
                                   storage_location)
        self.scale = scale

    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'png'
    
    def get_visualization_shorthand(self):
        return 'map'

    def get_additional_metadata(self):
        return  [('scale',self.scale)]
    
    def _create_indicator(self, year):
        """Create a map for the given indicator, save it to the cache
        directory's 'indicators' sub-directory.
        """

        values = self._get_indicator(year, wrap = False)
        
        min_value = None; max_value = None
            
        if self.scale is not None:
            min_value, max_value = self.scale
          
        attribute_alias = self.get_attribute_alias(attribute = self.attributes[0], 
                                                   year=year)
            
        title = self.name + ' ' + str(year)
        if self.run_description is not None:
            title += '\n' + self.run_description
        
        file_path = self.get_file_path(year = year) 

        dataset = self._get_dataset(year)  
        dataset.plot_map(attribute_alias, my_title=title, file=file_path,
                         filter='urbansim.gridcell.is_fully_in_water',
                         min_value=min_value, max_value=max_value)
        
        return file_path


from opus_core.tests import opus_unittest
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
        
    def skip_test_create_indicator(self):
        ####NOTE: THIS TEST FAILS BECAUSE THE OPUS_CORE DATASET DOES NOT HAVE 2D ATTRIBUTES, X/Y AXES
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        map = Map(
                  source_data = self.source_data,
                  attribute = 'opus_core.test.attribute',
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
