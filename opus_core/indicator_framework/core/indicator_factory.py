# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

    
import os, webbrowser
from time import strftime,localtime

from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.core.indicator_results import IndicatorResults
from opus_core.indicator_framework.utilities.gui_utilities import display_message_dialog

from opus_core.logger import logger

class IndicatorFactory(object):
    '''A factory that manages the computation of indicators.
       Indicators to compute should be specified in an 
       SourceData.'''
              
    def create_indicators(self, indicators,
                          file_name_for_indicator_results = 'indicator_results.html',
                          display_error_box = False, 
                          show_results = False):
        '''Handles the computation of a list of indicators.'''
        if (len(indicators) == 0):
            return
        
        source_data = indicators[0].source_data
        
            
        log_file_path = os.path.join(source_data.cache_directory, 'indicators.log')
        logger.enable_file_logging(log_file_path, 'a')
        logger.log_status('\n%s BEGIN %s %s' 
            % ('='*29, strftime('%Y_%m_%d_%H_%M', localtime()), '='*29))
    
        ####### create indicators #########
        # JLM: create is inherited from abstract_indicator.py
        for indicator in indicators:
            indicator.create(display_error_box = display_error_box)
        ###################################
        
        logger.log_status('%s END %s %s\n' 
            % ('='*30, strftime('%Y_%m_%d_%H_%M', localtime()), '='*30))
        logger.disable_file_logging(log_file_path)
    
        results_page_path = self._write_results(indicators, 
                                                source_data, 
                                                file_name_for_indicator_results,
                                                display_error_box)
        
        if show_results:
            self.show_results(results_page_path)
            
        return results_page_path
    
    def _write_results(self,
                       indicators, 
                       source_data, 
                       file_name_for_indicator_results,
                       display_error_box):
        
        #generate a static html page for browsing outputted indicators and store the path to the html
        results_page_path = None
        results = IndicatorResults()
        try:            
            results_page_path = results.create_page(
                source_data = source_data,
                page_name = file_name_for_indicator_results,
                indicators = indicators)
        except:
            message = 'failed to generate indicator results page'
            if display_error_box:
                display_message_dialog(message)
            logger.enable_hidden_error_and_warning_words()
            logger.log_warning(message)
            logger.disable_hidden_error_and_warning_words()
    
        if results_page_path is not None:        
            results_page_path = 'file://' + results_page_path
            
        return results_page_path
    
    def show_results(self, path):
        webbrowser.open_new(path)
        
# unit tests
from opus_core.tests import opus_unittest
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class IndicatorFactoryTests(AbstractIndicatorTest):
                
    def test__create_indicators(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
        except:
            pass
        else:
            indicator_path = os.path.join(self.temp_cache_path, 'indicators')
            self.assert_(not os.path.exists(indicator_path))
            
            indicators = [
               Table(
                  source_data = self.source_data,
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute', 
                  output_type = 'tab'
               )
            ]
            
            factory = IndicatorFactory()
            
            factory.create_indicators(indicators = indicators)
            
            self.assert_(os.path.exists(indicator_path))
            self.assert_(os.path.exists(os.path.join(indicator_path, 'test__tab__attribute.tab')))
            #self.assert_(os.path.exists(os.path.join(indicator_path, 'indicator_results.html')))
            

if __name__=='__main__':
    opus_unittest.main()