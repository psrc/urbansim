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

from opus_core.variables.variable_name import VariableName
import os 
from time import strftime, localtime, time
from inprocess.travis.opus_core.indicator_framework.utilities.indicator_data_manager import IndicatorDataManager

class ComputedIndicator:
    def __init__(self, 
                 indicator, 
                 result_template, 
                 dataset_metadata):

        self.indicator = indicator
        self.result_template = result_template
        
        cache_directory = self.result_template.cache_directory
        self.storage_location = os.path.join(cache_directory, 'indicators')
        self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        self.dataset_metadata = dataset_metadata
        
    def get_attribute_alias(self, year = None):
        return self.indicator.get_attribute_alias(year)
    
    def get_file_extension(self):
        return 'csv'
    
    def get_file_name(self, years = None, 
                      extension = 'csv', 
                      suppress_extension_addition = False):
            
        short_name = self.indicator.name
            
        file_name = '%s__%s'%(self.indicator.dataset_name,
                              short_name)
        
        if years is not None:
            file_name += '__%s'%('-'.join([str(year) for year in years]))
        
        if not suppress_extension_addition:
            if extension == None:
                extension = self.get_file_extension()
            file_name += '.%s'%extension
        return file_name
    
    def get_file_path(self, years = None):
        file_name = self.get_file_name(years)
        return os.path.join(self.storage_location, file_name)
        
    def export(self):
        data_manager = IndicatorDataManager()
        data_manager.export_indicator(
           indicator = self, 
           source_data = self.result_template)
        
from opus_core.tests import opus_unittest
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator
from inprocess.travis.opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class ComputedIndicatorTests(AbstractIndicatorTest):  
    def test__get_indicator_path(self):
                
        indicator = Indicator(
            attribute = 'opus_core.test.population',
            dataset_name = 'test')
        
        computed_indicator = ComputedIndicator(
            result_template = self.source_data,
            indicator = indicator,
            dataset_metadata = {
                'dataset_name':indicator.dataset_name,
                'primary_keys':['id']                    
            }                                       
        )
        returned_path = computed_indicator.get_file_name()
        expected_path = 'test__population.csv'
        
        self.assertEqual(returned_path, expected_path)                    
    
if __name__ == '__main__':
    opus_unittest.main()
