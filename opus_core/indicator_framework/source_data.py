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

import os, sys
from opus_core.logger import logger

from copy import copy
from time import strftime, localtime

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

class SourceData(object):
    """Configuration information for computing a set of indicators. """
    
    cache_directory = ''
    comparison_cache_directory = ''
    
    run_description = ''
    datasets_to_preload = []
    
    years = []
    
    def __init__(self, 
                 dataset_pool_configuration,
                 cache_directory, 
                 comparison_cache_directory = None,
                 years = [],
                 run_description = None):
        
        self.dataset_pool_configuration = dataset_pool_configuration
        self.years = years            
        self.cache_directory = cache_directory
        if comparison_cache_directory is not None:
            self.comparison_cache_directory = comparison_cache_directory
        if run_description is not None:
            self.run_description = run_description                             
    
    def get_indicator_directory(self):
        return os.path.join(self.cache_directory, 'indicators')
    
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
            
        metadata_lines.append(indent + '<package_order>[\'opus_core\']</package_order>')
        cur_line = ''
        for i in range(indentation): cur_line += '\t'
        cur_line += ('</source_data>')
        metadata_lines.append(cur_line)
        
        return metadata_lines
        
from opus_core.tests import opus_unittest

class TestSourceData(opus_unittest.OpusTestCase):
    def test__get_indicator_directory(self):
        config = SourceData(
                cache_directory = 'xxxx',
                dataset_pool_configuration = DatasetPoolConfiguration(
                    package_order=['opus_core'],
                    package_order_exceptions={},
                ))
        output = config.get_indicator_directory()
        expected = os.path.join('xxxx','indicators')
        self.assertEqual(output,expected)

    def test__write_self_to_metadata(self):
        config = SourceData(
            cache_directory = 'xxxx',
            comparison_cache_directory = 'yyyy',
            run_description = 'run',
            years = [2006],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            ))
        
        lines = config.get_metadata(indentation = 0)
        expected = [
            '<source_data>',
            '\t<cache_directory>xxxx</cache_directory>',
            '\t<comparison_cache_directory>yyyy</comparison_cache_directory>',  
            '\t<run_description>run</run_description>',
            '\t<years>[2006]</years>',
            '\t<package_order>[\'opus_core\']</package_order>',  
            '</source_data>'
        ]
        self.assertEqual(lines,expected)
                
if __name__ == '__main__':
    opus_unittest.main()