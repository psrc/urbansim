# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable_name import VariableName
import os 
from time import strftime, localtime, time
from opus_gui.results_manager.run.indicator_framework.utilities.indicator_data_manager import IndicatorDataManager
from copy import copy

class ComputedIndicator:
    def __init__(self, 
                 indicator, 
                 source_data, 
                 dataset_name,
                 primary_keys):

        self.indicator = indicator
        self.source_data = source_data
        
        cache_directory = self.source_data.cache_directory
        self.storage_location = os.path.join(cache_directory, 'indicators')
        self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        
        self.computed_dataset_column_name = self.get_attribute_alias()
        
        self.dataset_name = dataset_name
        self.primary_keys = primary_keys
    
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
    
    def get_computed_dataset_column_name(self, year = None):
        name = self.computed_dataset_column_name
        if year is not None:
            if name.find('DDDD') == -1:
                name = '%s_%i'%(name, year)
            else:
                name = name.replace('DDDD', repr(year))
        return name
    
#    def export(self):
#        data_manager = IndicatorDataManager()
#        data_manager.export_indicator(
#           indicator = self, 
#           source_data = self.source_data)
        
            
from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator
from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class ComputedIndicatorTests(AbstractIndicatorTest):  
    def test__get_indicator_path(self):
                
        indicator = Indicator(
            attribute = 'opus_core.test.population',
            dataset_name = 'test')
        
        computed_indicator = ComputedIndicator(
            source_data = self.source_data,
            indicator = indicator,
            dataset_name = 'test',
            primary_keys = ['id']                                       
        )
        returned_path = computed_indicator.get_file_name()
        expected_path = 'test__population.csv'
        
        self.assertEqual(returned_path, expected_path)                    
    
if __name__ == '__main__':
    opus_unittest.main()
