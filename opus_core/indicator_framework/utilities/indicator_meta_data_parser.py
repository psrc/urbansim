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

import re
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework import SourceData

class IndicatorMetaDataParser:
    def write_indicator_metadata(cls, indicator, year = None):
        VERSION = 1.0
        '''Writes to a file information about this indicator'''

        lines = []
        class_name = indicator.__class__.__name__
        
        lines.append('<version>%.1f</version>'%VERSION)
        lines.append('<%s>'%class_name)
        basic_attributes = ['dataset_name','years','date_computed', 'name', 'operation']
        if class_name != 'DatasetTable':
            basic_attributes.append('attribute')
        for basic_attr in basic_attributes:
            attr_value = indicator.__getattribute__(basic_attr)
            lines.append('\t<%s>%s</%s>'%(basic_attr,
                                     str(attr_value),
                                     basic_attr))
        
        #get additional attributes for child classes...
        for attr,value in indicator.get_additional_metadata():
            lines.append('\t<%s>%s</%s>'%(attr,str(value),attr))
            
        lines += indicator.source_data.get_metadata(indentation = 1)
        
        lines.append('</%s>'%class_name)
        
        #write to metadata file
        file = indicator.get_file_name(year = year, extension = 'meta')
        path = os.path.join(indicator.source_data.get_indicator_directory(),
                            file)
        f = open(path, 'w')
        output = '\n'.join(lines)
        f.write(output)
        f.close()
        
        return lines
    def create_indicator_from_metadata(cls, file_path):
        '''creates and returns an indicator from the file pointed to in file_path 
        '''
        #TODO: If the additional child parameters are not strings, the current implementation will fail.
        
        f = open(file_path)
        
        version = f.readline()
        indicator_class = f.readline().strip()
        indicator_class = indicator_class[1:-1]
        
        in_source_data = False
        
        source_data_params = {}
        
        non_constructor_attr = {
            'date_computed': None
        }
        
        params = {}
        
        for line in f.readlines():
            line = line.strip()
            if line == '<source_data>':
                in_source_data = True
            elif line == '</source_data>':
                source_data = SourceData(**source_data_params)
                params['source_data'] = source_data
                in_source_data = False
            elif line != '</%s>'%indicator_class:
                (name, value) = IndicatorMetaDataParser._extract_name_and_value(line)
                
                #TODO: figure out way for each object to know which values to 
                #reinterpret from string
                if name == 'years' or name == 'scale':
                    if value == 'None' or value == '[]':
                        value = []
                    else:
                        value = [int(y) for y in value[1:-1].split(',')]
                elif name == 'attributes':
                    if value == 'None' or value == '[]':
                        value = []
                    else: 
                        value = [attr.strip().replace("'",'') for attr in value[1:-1].split(',')]
                
                if in_source_data:
                    if name == 'package_order':
                        order = [eval(p) for p in value[1:-1].split(',')]
                        
                        pool = DatasetPoolConfiguration(
                            package_order = order,
                            package_order_exceptions = {},
                        )
                        source_data_params['dataset_pool_configuration'] = pool
                    else:
                        source_data_params[name] = value
                else:
                    if name == 'dataset_name':
                        params['dataset_name'] = value
                    elif name in non_constructor_attr:
                        non_constructor_attr[name] = value
                    else:
                        params[name] = value

        f.close()
        
        exec('from opus_core.indicator_framework.image_types import %s'%indicator_class)
        indicator = locals()[indicator_class](**params)
        
        for attr, value in non_constructor_attr.items():
            if value == 'None':
                value = None
            indicator.__setattr__(attr,value)
        return indicator 
    
    def _extract_name_and_value(cls, line):
        '''takes a line of xml and returns attr name/value tuple'''
        name_re = re.compile('<\w+>')
        value_re = re.compile('>.*<')
        
        line = line.strip()
        name = name_re.match(line).group()
        name = name[1:-1]
        value = value_re.search(line).group()
        value = value[1:-1]
        return (name, value)

    #make class methods
    write_indicator_metadata = classmethod(write_indicator_metadata)
    create_indicator_from_metadata = classmethod(create_indicator_from_metadata)
    _extract_name_and_value = classmethod(_extract_name_and_value)


from opus_core.tests import opus_unittest
from opus_core.indicator_framework.utilities import AbstractIndicatorTest
import os

class Tests(AbstractIndicatorTest):  
    def test__write_metadata(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: pass
        else:
            table = Table(
                source_data = self.cross_scenario_source_data,
                attribute = 'xxx.yyy.population',
                dataset_name = 'yyy',
                output_type = 'tab',
                years = [0,1] # Indicators are not actually being computed, so the years don't matter here.
            )
            
            lines = IndicatorMetaDataParser.write_indicator_metadata(indicator = table)
            output = '\n'.join(lines)
            
            expected = (
                '<version>1.0</version>\n'          
                '<Table>\n'
                '\t<dataset_name>yyy</dataset_name>\n'
                '\t<years>[0, 1]</years>\n'
                '\t<date_computed>None</date_computed>\n'
                '\t<name>population</name>\n'
                '\t<operation>None</operation>\n'
                '\t<attribute>xxx.yyy.population</attribute>\n'
                '\t<output_type>tab</output_type>\n'
                '\t<source_data>\n'
                '\t\t<cache_directory>%s</cache_directory>\n'
                '\t\t<comparison_cache_directory>%s</comparison_cache_directory>\n' 
                '\t\t<run_description>%s</run_description>\n'
                '\t\t<years>[1980]</years>\n'
                '\t\t<package_order>[\'opus_core\']</package_order>\n'
                '\t</source_data>\n'
                '</Table>'
            )%(self.temp_cache_path,
               self.temp_cache_path2,
               self.cross_scenario_source_data.get_run_description())
            
            self.assertEqual(output,expected)
  
    def test__read_write_metadata(self):
        try:
            from opus_core.indicator_framework.image_types import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: 
            raise
        else:
            
            table = Table(
                source_data = self.source_data,
                attribute = 'xxx.yyy.population',
                dataset_name = 'yyy',
                output_type = 'tab',
                years = [0,1] # Indicators are not actually being computed, so the years don't matter here.
            )
            
#            table.create(False)
            IndicatorMetaDataParser.write_indicator_metadata(indicator = table)
            metadata_file = table.get_file_name(extension = 'meta')
            metadata_path = os.path.join(self.source_data.get_indicator_directory(),
                                         metadata_file)
            self.assertEqual(os.path.exists(metadata_path), True)
            
            expected_path = 'yyy__tab__population.meta'
            self.assertEqual(metadata_file,expected_path)
            
            new_table = IndicatorMetaDataParser.create_indicator_from_metadata(metadata_path)
            for attr in ['attribute','dataset_name',
                         'output_type','date_computed',
                         'years']:
                old_val = table.__getattribute__(attr)
                new_val = new_table.__getattribute__(attr)
                self.assertEqual(old_val,new_val)
            
            self.assertEqual(table.source_data.cache_directory,
                             new_table.source_data.cache_directory)
            self.assertEqual(table.source_data.dataset_pool_configuration.package_order,
                             new_table.source_data.dataset_pool_configuration.package_order)
            
            
if __name__ == '__main__':
    opus_unittest.main()