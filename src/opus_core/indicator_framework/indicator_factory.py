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

    
import os, webbrowser
from time import strftime,localtime

from opus_core.indicator_framework.source_data import SourceData
from opus_core.indicator_framework.indicator_results import IndicatorResults
from opus_core.indicator_framework.gui_utilities import display_message_dialog

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
        indicators_directory = source_data.get_indicator_directory()
        if not os.path.exists(indicators_directory):
            os.makedirs(indicators_directory)
            
        ### TODO: Get rid of this junk and get a better logging system
        log_file_path = os.path.join(indicators_directory,'indicators.log')
        logger.enable_file_logging(log_file_path, 'a')
        logger.log_status('\n%s BEGIN %s %s' 
            % ('='*29, strftime('%Y_%m_%d_%H_%M', localtime()), '='*29))
    
        #create indicators
        for indicator in indicators:
            indicator.create(display_error_box = display_error_box)
        
        logger.log_status('%s END %s %s\n' 
            % ('='*30, strftime('%Y_%m_%d_%H_%M', localtime()), '='*30))
        logger.disable_file_logging(log_file_path)
    
        #generate a static html page for browsing outputted indicators and store the path to the html
        results_page_path = None
      
        try:            
            results = IndicatorResults()
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
        else:
            if show_results:
                webbrowser.open_new("file://" + results_page_path)
        
        if results_page_path is not None:        
            results_page_path = 'file://' + results_page_path
        return results_page_path

# unit tests
from opus_core.tests import opus_unittest
from shutil import copytree, rmtree

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.storage_factory import StorageFactory
from numpy import array
import tempfile

class IndicatorFactoryTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_cache_path = tempfile.mkdtemp(prefix='opus_tmp')    
        self.temp_cache_path2 = tempfile.mkdtemp(prefix='opus_tmp')
      
        baseyear_dir = os.path.join(self.temp_cache_path, '1980')
        storage = StorageFactory().get_storage('flt_storage', storage_location=baseyear_dir)
        storage.write_table(table_name='tests',
           table_data= {
               'id': array([1,2,3,4]),
               'attribute': array([5,6,7,8]),
               'attribute2': array([50,60,70,80])
               },
           )
        
        ## TODO: What is this line doing?
        copytree(baseyear_dir,  os.path.join(self.temp_cache_path2, '1980'))
    
        self.source_data = SourceData(
            cache_directory = self.temp_cache_path,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )

    def tearDown(self):
        rmtree(self.temp_cache_path)
                
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
                  attribute = 'package.test.attribute', 
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