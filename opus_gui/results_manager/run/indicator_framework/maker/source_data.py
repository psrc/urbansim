# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os, sys
from opus_core.logger import logger

from copy import copy
from time import strftime, localtime

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_gui.results_manager.run.indicator_framework.utilities.integrity_error import IntegrityError

class SourceData(object):
    """Configuration information for computing a set of indicators. """
    
    def __init__(self, 
                 dataset_pool_configuration,
                 cache_directory, 
                 name,
                 run_id,
                 comparison_cache_directory = '',
                 years = [],
                 run_description = ''):
        
        self.dataset_pool_configuration = dataset_pool_configuration
        self.years = years            
        self.cache_directory = cache_directory
        self.comparison_cache_directory = comparison_cache_directory
        self.run_description = run_description       
        self.name = name  
        self.run_id = run_id
            
        self._check_integrity()
        
    def get_indicator_directory(self):
        return os.path.join(self.cache_directory, 'indicators')
            
    def get_run_description(self):
        if self.run_description == '':
            self.run_description = self.cache_directory
            if self.comparison_cache_directory != '':
                self.run_description = '%s vs.\n%s'%(
                    self.cache_directory, 
                    self.comparison_cache_directory)  
                 
        return self.run_description         
        
    def get_metadata(self, indentation = 1):
        '''gets list based representation of self outputable to a metadata file
        
           indentation is the number of tabs to output self
        '''
        metadata_lines = []
        cur_line = ''
        for i in range(indentation): cur_line += '\t'
        cur_line += ('<source_data>')
        metadata_lines.append(cur_line)
        
        basic_attributes = ['cache_directory','comparison_cache_directory',
                            'run_description', 'years']
        
        indent = ''
        for i in range(indentation+1): indent += '\t'
        
        for attr in basic_attributes:
            attr_value = self.__getattribute__(attr)
            cur_line = indent + '<%s>%s</%s>'%(attr,str(attr_value),attr)
            metadata_lines.append(cur_line)
            
        package_order = self.dataset_pool_configuration.package_order
        package_order_output = repr(package_order).replace("'","\'")
        
        metadata_lines.append(indent + '<package_order>%s</package_order>'%package_order_output)
        cur_line = ''
        for i in range(indentation): cur_line += '\t'
        cur_line += ('</source_data>')
        metadata_lines.append(cur_line)
        
        return metadata_lines
    
    def get_package_order(self):
        return self.dataset_pool_configuration.package_order
        
    def _check_integrity(self):
        cross_scenario_comparison = self.comparison_cache_directory != ''
        #test if cache dir exists
        if not os.path.exists(self.cache_directory):
            raise IntegrityError('Cache directory %s does not exist'%self.cache_directory)
        
        #if comparison_cache dir set, does it exist
        if cross_scenario_comparison and not os.path.exists(self.comparison_cache_directory):
            raise IntegrityError('Comparison cache directory %s does not exist'%self.comparison_cache_directory)
        
        #do all years exist in cache dirs?
        for year in self.years:
            year_dir = os.path.join(self.cache_directory, repr(year))
            if not os.path.exists(year_dir):
                raise IntegrityError('Year %i does not exist in cache directory %s'%
                                     (year, self.cache_directory))
            if cross_scenario_comparison:
                year_dir = os.path.join(self.comparison_cache_directory, repr(year))
                if not os.path.exists(year_dir):
                    raise IntegrityError('Year %i does not exist in comparison cache directory %s'%
                                         (year, self.comparison_cache_directory))
    
from opus_gui.results_manager.run.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData


class TestSourceData(TestWithAttributeData):
    def setUp(self):
        TestWithAttributeData.setUp(self)
        self.source_data = SourceData(
            cache_directory = self.temp_cache_path,
            years = [1980],
            run_id = -1,
            name = 'test',
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
            )
        )

    def test__write_self_to_metadata(self):
        self.source_data.comparison_cache_directory = self.temp_cache_path2
        self.source_data.run_description = 'run'
        
        lines = self.source_data.get_metadata(indentation = 0)
        expected = [
            '<source_data>',
            '\t<cache_directory>%s</cache_directory>'%self.temp_cache_path,
            '\t<comparison_cache_directory>%s</comparison_cache_directory>'%self.temp_cache_path2,  
            '\t<run_description>run</run_description>',
            '\t<years>[1980]</years>',
            '\t<package_order>[\'opus_core\']</package_order>',  
            '</source_data>'
        ]
        self.assertEqual(lines,expected)

    def test__integrity_checker(self):
        try:
            source_data = SourceData(
                cache_directory = self.temp_cache_path,
                run_id = -1,
                years = [1980],
                name = 'test2',
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order=['opus_core'],
                )
            )
        except IntegrityError:
            self.assertTrue(False)
        
        '''don't have data available for year 1970'''
        try:
            source_data = SourceData(
                cache_directory = self.temp_cache_path,
                run_id = -1,
                years = [1970],
                name = 'test3',
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order=['opus_core'],
                )
            )
        except IntegrityError:
            pass
        else:
            self.assertTrue(False)                                 

        '''cache dir doesn't exist'''
        try:
            source_data = SourceData(
                cache_directory = 'null',
                run_id = -1,
                years = [1980],
                name = 'test4',
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order=['opus_core'],
                )
            )
        except IntegrityError:
            pass
        else:
            self.assertTrue(False)                             

        '''comparison cache dir doesn't exist'''
        try:
            source_data = SourceData(
                cache_directory = self.temp_cache_path,
                run_id = -1,
                comparison_cache_directory = 'null',
                years = [1980],
                name = 'test5',
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order=['opus_core'],
                )
            )
        except IntegrityError:
            pass
        else:
            self.assertTrue(False)       
            
from opus_core.tests import opus_unittest
if __name__ == '__main__':
    opus_unittest.main()