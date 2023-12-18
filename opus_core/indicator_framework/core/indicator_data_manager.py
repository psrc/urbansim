# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.logger import logger

class IndicatorDataManager:
    
    def export_indicator(self, indicator, source_data, year = None):
        self._export_indicator_to_file(indicator, source_data, year)
        
    def _export_indicator_to_file(self, indicator, source_data, year):
        VERSION = 1.0
        '''Writes to a file information about this indicator'''

        if not indicator.write_to_file:
            return
        
        lines = []
        class_name = indicator.__class__.__name__
        
        lines.append('<version>%.1f</version>'%VERSION)
        lines.append('<%s>'%class_name)
        basic_attributes = ['dataset_name',
                            'years',
                            'date_computed', 
                            'name', 
                            'operation',
                            'storage_location']
        
        attrs = '[\'' + '\';\''.join(indicator.attributes) + '\']'
        lines.append('\t<attributes>%s</attributes>'%(
                                     attrs))
        
        for basic_attr in basic_attributes:
            attr_value = indicator.__getattribute__(basic_attr)
            lines.append('\t<%s>%s</%s>'%(basic_attr,
                                     str(attr_value),
                                     basic_attr))
        
        #get additional attributes for child classes...
        for attr,value in indicator.get_additional_metadata():
            lines.append('\t<%s>%s</%s>'%(attr,str(value),attr))
            
        lines += source_data.get_metadata(indentation = 1)
        
        lines.append('</%s>'%class_name)
        
        #write to metadata file
        file = indicator.get_file_name(year = year, extension = 'meta')
        path = os.path.join(indicator.get_storage_location(), file)
        f = open(path, 'w')
        output = '\n'.join(lines)
        f.write(output)
        f.close()
        
        return lines

    def import_indicators(self, indicator_directory):
        return self._import_indicators_from_file(indicator_directory)

    def _import_indicators_from_file(self, indicator_directory):
        '''scans the indicator directory for indicator meta files and 
           recreates the indicators'''
        import fnmatch
        files = [os.path.join(indicator_directory, f) 
                    for f in os.listdir(indicator_directory) 
                        if fnmatch.fnmatch(f,'*.meta')]
        indicators = []
        for f in files:
            try:
                 indicator = self._import_indicator_from_file(f) 
                 indicators.append(indicator)
            except Exception as e:
                logger.log_warning('Could not load indicator from %s: %s'%(f,e))
        return indicators        
    
    '''not in use yet'''
#    def import_indicator(self):
#        meta_path = os.path.join(indicator_directory, filename)
#        indicator = self._import_indicator_from_file(meta_path)
#        indicators.append(indicator)
                    
    def _import_indicator_from_file(self, file_path):
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
                in_source_data = False
            elif line != '</%s>'%indicator_class:
                (name, value) = self._extract_name_and_value(line)
                
                #TODO: figure out way for each object to know which values to 
                #reinterpret from string
                if name == 'years' or name == 'scale':
                    if value == 'None' or value == '[]':
                        value = []
                    elif name=='scale':
                        value = [float(y) for y in value[1:-1].split(',')]
                    elif name=='years':
                        value = [int(y) for y in value[1:-1].split(',')]
                elif name == 'attributes':
                    if value == 'None' or value == '[]':
                        value = []
                    else: 
                        value = [attr.strip().replace("'",'') for attr in value[1:-1].split(';')]
                
                if in_source_data:
                    if name == 'package_order':
                        order = [eval(p.strip()) for p in value[1:-1].split(',')]
                        
                        pool = DatasetPoolConfiguration(
                            package_order = order,
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
        cache_directory = os.path.split(os.path.dirname(file_path).split()[0])[0]
        source_data_params['cache_directory'] = cache_directory
        indicator = self._create_indicator(indicator_class, 
                                           params,
                                           non_constructor_attr,
                                           source_data_params)
        return indicator
        
    def _create_indicator(self, indicator_class, params, non_constructor_attributes, source_data_params):
        source_data = SourceData(**source_data_params)
        
        for k,v in list(params.items()):
            if v=='None':
                params[k] = None
                
        params['source_data'] = source_data
        module = self._get_module_from_indicator_class(indicator_class)

        if indicator_class != 'DatasetTable':
            params['attribute'] = params['attributes'][0]
            del params['attributes']
                    
        exec('from opus_core.indicator_framework.image_types.%s import %s'%(module, indicator_class))
        indicator = locals()[indicator_class](**params)
        
        for attr, value in list(non_constructor_attributes.items()):
            if value == 'None':
                value = None
            indicator.__setattr__(attr,value)
        return indicator 
    
    def _extract_name_and_value(self, line):
        '''takes a line of xml and returns attr name/value tuple'''
        name_re = re.compile('<\w+>')
        value_re = re.compile('>.*<')
        
        line = line.strip()
        name = name_re.match(line).group()[1:-1]
        value = value_re.search(line).group()[1:-1]
        return (name, value)
    
    def _get_module_from_indicator_class(self, indicator_class):
        modules = {
           'DatasetTable': 'dataset_table',
           'GeotiffMap': 'geotiff_map',
           'Map': 'mapnik_map',
           'Chart': 'matplotlib_chart',
           'LorenzCurve': 'matplotlib_lorenzcurve',
           'Table': 'table'
        }
        return modules[indicator_class]
    
from opus_core.tests import opus_unittest
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
import os

class Tests(AbstractIndicatorTest):  
    def setUp(self):
        self.data_manager = IndicatorDataManager()
        AbstractIndicatorTest.setUp(self)
        
    def test__write_metadata(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
        except: pass
        else:
            table = Table(
                source_data = self.cross_scenario_source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                output_type = 'tab',
                years = [1980,1981] # Indicators are not actually being computed, so the years don't matter here.
            )
            
            table.create(False)
            table.date_computed = None
            output = self.data_manager._export_indicator_to_file(
                 indicator = table,
                 source_data = self.cross_scenario_source_data,
                 year = None)
            
            expected = [
                '<version>1.0</version>',          
                '<Table>',
                '\t<attributes>[\'opus_core.test.attribute\']</attributes>',
                '\t<dataset_name>test</dataset_name>',
                '\t<years>[1980, 1981]</years>',
                '\t<date_computed>None</date_computed>',
                '\t<name>attribute</name>',
                '\t<operation>None</operation>',
                '\t<storage_location>%s</storage_location>'%os.path.join(self.temp_cache_path, 'indicators'),
                '\t<output_type>tab</output_type>',
                '\t<source_data>',
                '\t\t<cache_directory>%s</cache_directory>'%self.temp_cache_path,
                '\t\t<comparison_cache_directory>%s</comparison_cache_directory>'%self.temp_cache_path2, 
                '\t\t<run_description>%s</run_description>'%self.cross_scenario_source_data.get_run_description(),
                '\t\t<years>[1980]</years>',
                '\t\t<package_order>[\'opus_core\']</package_order>',
                '\t</source_data>',
                '</Table>'
            ]
            
            for i in range(len(output)):
                if expected[i] != output[i]:
                    print(expected[i])
                    print(output[i])
                    
            self.assertEqual(output,expected)
  
    def test__read_write_metadata(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
        except: 
            raise
        else:
            
            table = Table(
                source_data = self.source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                output_type = 'tab',
                years = [1980,1981] # Indicators are not actually being computed, so the years don't matter here.
            )
            
            table.create(False)
            self.data_manager._export_indicator_to_file(indicator = table,
                                                        source_data = self.source_data,
                                                        year = None)
            
            metadata_file = table.get_file_name(extension = 'meta')
            metadata_path = os.path.join(table.get_storage_location(),
                                         metadata_file)
            self.assertEqual(os.path.exists(metadata_path), True)
            
            expected_path = 'test__tab__attribute.meta'
            self.assertEqual(metadata_file,expected_path)
            
            new_table = self.data_manager._import_indicator_from_file(metadata_path)
            for attr in ['attributes','dataset_name',
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