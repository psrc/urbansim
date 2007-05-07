
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

from opus_core.logger import logger

import os, sys, traceback, re
from time import strftime, localtime, time
from copy import copy, deepcopy
from gc import collect

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.dataset_factory import DatasetFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from opus_core.indicator_framework.gui_utilities import display_message_dialog
from opus_core.indicator_framework.source_data import SourceData

from numpy import array, subtract

class AbstractIndicator(object):
    
    def __init__(self, source_data, dataset_name, attribute, 
                 years = None, expression = None, name = None,
                 suppress_file_extension_addition = False ):

        self.dataset_name = dataset_name 
        self.attribute = attribute
        self.expression = expression
        self.source_data = source_data
        self.suppress_file_extension_addition = suppress_file_extension_addition
        
        if expression is None and attribute is None:
            raise Exception, 'Expression and attribute cannot both be None'
         
        self.name = name
        if self.name == None:
            self.name = self.get_attribute_alias()
        
        if years is None:
            self.years = self.source_data.years
        else:
            self.years = years

        self.dataset = None
        self.dataset_state = {
              'current_cache_directory':None,
              'year':None
        }
        
        self.last_computed_attribute = None

        #todo: this logic should be in SourceData
        self.run_description = self.source_data.run_description
        if self.run_description == '':
            self.run_description = self.source_data.cache_directory
            if self.source_data.comparison_cache_directory != '':
                self.run_description = '%s vs.\n%s'%(
                    self.source_data.cache_directory, 
                    self.source_data.comparison_cache_directory)        
                
        #setting indicators directory
        indicators_directory = self.source_data.get_indicator_directory()
        if not os.path.exists(indicators_directory):
            os.makedirs(indicators_directory)
            
        self.date_computed = None

        # Use attribute cache so that can access info from prior years, too.
        self.package_order = self.source_data.dataset_pool_configuration.package_order
        self.package_order_exceptions = self.source_data.dataset_pool_configuration.package_order_exceptions
        
    def _set_cache_directory(self, cache_directory):
        if cache_directory != SimulationState().get_cache_directory():
            SimulationState().set_cache_directory(cache_directory) 
            SessionConfiguration(
                new_instance = True,
                package_order = self.package_order,
                package_order_exceptions = self.package_order_exceptions,
                in_storage = AttributeCache()) 
            
    def create(self, display_error_box):
        '''Computes and outputs the indicator to the cache directory's 'indicators' sub-directory.
        '''
        cache_directory = self.source_data.cache_directory
        self._set_cache_directory(cache_directory)
        self.in_expression = False
        
        if self.is_single_year_indicator_image_type():
            for year in self.years:
                try:
                    self._create_indicator(year = year)
                    self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
                    self._write_metadata(year = year)
                except Exception, e:
                    self._handle_indicator_error(e, display_error_box)
        else:
            try:
                self._create_indicator(years = self.years)
                self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
                self._write_metadata()
            except Exception, e:
                self._handle_indicator_error(e, display_error_box)
        
        del self.dataset
        collect()
                
    ####### Abstract methods that need to be overridden by child classes ############
    def _create_indicator(self):
        '''Image-type specific computations for indicator generation.
        
           Abstract method that needs to be overridden in child classes.
           
           Should return the filepath to the created indicator.
        '''
        
        message = 'abstract_image_type._create_indicator needs to be overridden by child class.'
        raise NotImplementedError(message)
    
    def is_single_year_indicator_image_type(self):
        '''Should this image type be output per year? 
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.is_single_year_indicator_image_type needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_file_extension(self):
        '''Returns the file extension of the outputted indicator 
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.get_file_extension needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_shorthand(self):
        '''Returns the shorthand for this output type
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.get_shorthand needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)
            
    def _get_additional_metadata(self):
        '''returns additional attributes
        
           Child method should override this method if there are any 
           additional attributes that it has. Return a list of
           (attr_name,value) tuples.
        '''
        return []
    
    ####### Helper methods for indicator computations #############

    def _get_indicator_for_years(self, attribute, years):
        """Returns results, years_found where results is a numpy array of the
        depedent data, and years_found is a Python list of the years that had data 
        in the cache.
        """
        results = []
        years_found = []
        for year in years:
            result = self._get_indicator(attribute, year)
            results.append(result)
            years_found.append(year)
        return array(results), years_found

    def _get_indicator(self, attribute, year):
        if attribute is None:
            attribute = self.get_attribute_alias(year)
        
        attribute = attribute.replace('DDDD',repr(year))
        
        indicator_vals = self._get_indicator_helper(attribute, year)
        
        #handle cross-scenario indicator comparisons
        id_attributes = self._get_dataset(year).get_id_name()
        cache_dir2 = self.source_data.comparison_cache_directory
        if cache_dir2 != '' and attribute not in id_attributes:
            if not os.path.exists(cache_dir2):
                raise Exception, 'The second cache directory was not found.'
            short_name = VariableName(attribute).get_alias()
            
            #save cache_dir's dataset
            old_dataset_state = copy(self.dataset_state)
            old_dataset = copy(self._get_dataset(year))
            
            #compute values for cache_dir2 and get the difference
            self._set_cache_directory(cache_dir2)
            indicator_vals2 = self._get_indicator_helper(attribute, year)
            indicator_vals = indicator_vals - indicator_vals2
            
            #reload cache_dir's dataset with the proper values in the attribute
            old_dataset.set_values_of_one_attribute(short_name, indicator_vals)
            self._set_dataset(old_dataset, old_dataset_state)
        return indicator_vals
            

    def _get_indicator_helper(self, attribute, year):
        if self.expression is None or self.in_expression:
            indicator_vals = self._compute_indicator(attribute, year)
        else:
            #this handles indicator expressions
            self.in_expression = True
            try:
                values = []
                for arg_attribute in self.expression['operands']:
                    arg_vals = self._compute_indicator(arg_attribute, year)
                    values.append(arg_vals)
                    
                base_attribute = self.expression['operands'][0]
                cmd = 'self.%s(values, base_attribute)'%self.expression['operation']
                indicator_vals = array(eval(cmd))
                dataset = self._get_dataset(year = year)
                dataset.add_attribute(indicator_vals, attribute)
                self.last_computed_attribute = attribute
            finally:
                self.in_expression = False
            
        return indicator_vals

    def _compute_indicator(self, attribute, year):
        attribute = attribute .replace('DDDD',repr(year))
        
        short_name = VariableName(attribute).get_alias()
        dataset = self._get_dataset(year = year)
        if short_name not in dataset.get_known_attribute_names():
            dataset.compute_variables(attribute)
        v = dataset.get_attribute(short_name)
        self.last_computed_attribute = short_name
        return v
            
    def _set_dataset(self, dataset, dataset_state):
        if self.dataset_state['current_cache_directory'] != dataset_state['current_cache_directory']:
            self._set_cache_directory(dataset_state['current_cache_directory'])
        if self.dataset_state['year'] != dataset_state['year']:
            SimuluationState().set_current_time(dataset_state['year'])
            
        self.dataset = dataset
        self.dataset_state = dataset_state
        
    def _get_dataset(self, year = None):
        
        if year == None: 
            year = SimulationState().get_current_time()
        
        fetch_dataset = (self.dataset == None or
                         self.dataset_state['year'] != year or
                         self.dataset_state['current_cache_directory'] != SimulationState().cache_directory)
                         
        if fetch_dataset:
            #only compute dataset if its necessary
    #        if self.dataset is not None:
                #memory cleanup...
     #           del self.dataset
     #           collect()
            
            SimulationState().set_current_time(year)
            SessionConfiguration().get_dataset_pool().remove_all_datasets()
            
            for dataset_description in self.source_data.datasets_to_preload:
                SessionConfiguration().get_dataset_from_pool(dataset_description.dataset_name)
                
            #exceptions to handle non-standard in_table_names
            exception_in_table_names = {'development_event':'development_events_generated' } 
    
            if SessionConfiguration().exceptions_in_table_names is None:
                SessionConfiguration().set_exceptions_in_table_names(exception_in_table_names)
            else:
                SessionConfiguration().exceptions_in_table_names.update(exception_in_table_names)
    
            storage_location = os.path.join(SimulationState().get_cache_directory(),str(year))
            SessionConfiguration().set_exceptions_in_storage(
                {'development_event':StorageFactory().get_storage(
                      'flt_storage',
                      storage_location = storage_location)
                })
    
            self.dataset = SessionConfiguration().get_dataset_from_pool(self.dataset_name)
            
            self.dataset_state['year'] = SimulationState().get_current_time()
            self.dataset_state['current_cache_directory'] = SimulationState().cache_directory
            
        return self.dataset
    
    def get_attribute_alias(self, year = None):
        if self.attribute is None:
            alias = self.name
        else:
            alias = VariableName(self.attribute).get_alias()
        
        if year is not None:
            alias = alias.replace('DDDD',repr(year))
        return alias
    
    def get_last_computed_attribute(self):
        return self.last_computed_attribute
    
    def get_file_name(self, year = None, 
                      extension = None, 
                      suppress_extension_addition = False):
        
        '''returns the file name for the outputted indicator'''
        if extension == None:
            extension = self.get_file_extension()
            
        short_name = self.name
        if year is not None:
            short_name = short_name.replace('DDDD',repr(year))
            
        file_name = '%s__%s__%s'%(self.dataset_name,
                                  self.get_shorthand(),
                                  short_name
                                  )
        
        if self.is_single_year_indicator_image_type():
            file_name += '__%i'%year
        
        if not suppress_extension_addition:
            file_name += '.%s'%extension
        return file_name
    
    def get_file_path(self, year = None):
        indicator_directory = self.source_data.get_indicator_directory()
        file_name = self.get_file_name(
            year)
        return os.path.join(indicator_directory, file_name)
        
    def _handle_indicator_error(self, e, display_error_box = False):
        ''' sends alert to various forums if there's an error '''
                 
        #todo: improve error message
        message = ('Failed to generate indicator "%s"! Check the indicator log '
                'in the indicators directory of the "%s" cache for further '
                'details.\nError: %s.' % (self.name, self.source_data.cache_directory, e))
        logger.log_warning(message)
        logger.log_stack_trace()
        if display_error_box:
            display_message_dialog(message)
            
    ####### Indicator Operations ##########  
    def size(self, values=None):
        dataset = self._get_dataset()
        dataset.get_id_attribute()
        return dataset.size()
    
    def unplaced(self, values=None):
        dataset = self._get_dataset()
        gid = dataset.get_attribute('grid_id')
        return (where(gid <= 0)[0]).size

    def divide(self, values, attribute):
        return values[0].sum()/float(values[1].sum())

    def times(self, values, attribute):
        return values[0] * values[1]

    def subtract(self, values, attribute):
        return values[0] - values[1]

    def percent_change(self, values, attribute):
        baseyear_values, dummy = self._get_indicator_for_years(attribute, [2000,])

        ret_values = ma.filled(( values[0] - baseyear_values[0,]) * 100 / \
                ma.masked_where(baseyear_values[0,]==0, baseyear_values[0,].astype(float32),0.0))

        return ret_values   #, "change value attached to dataset as attribute %s" % attribute)


    def change(self, values, attribute):
        baseyear_values, dummy = self._get_indicator_for_years(attribute, [2000,])
        ret_values = values[0]-baseyear_values[0,]
        return ret_values   #, "change value attached to dataset as attribute %s" % attribute)

#methods for reading and writing metadata
    def _write_metadata(self, year = None):
        VERSION = 1.0
        '''Writes to a file information about this indicator'''

        lines = []
        class_name = self.__class__.__name__
        
        lines.append('<version>%.1f</version>'%VERSION)
        lines.append('<%s>'%class_name)
        basic_attributes = ['dataset_name','years','date_computed', 'name']
        if class_name != 'DatasetTable':
            basic_attributes.append('attribute')
        for basic_attr in basic_attributes:
            attr_value = self.__getattribute__(basic_attr)
            lines.append('\t<%s>%s</%s>'%(basic_attr,
                                     str(attr_value),
                                     basic_attr))
        
        #get additional attributes for child classes...
        for attr,value in self._get_additional_metadata():
            lines.append('\t<%s>%s</%s>'%(attr,str(value),attr))
            
        lines += self.source_data.get_metadata(indentation = 1)
        if self.expression != None:
            lines.append('\t<expression>')
            for k,v in self.expression.items():
                lines.append('\t\t<%s>%s</%s>'%(k,str(v),k))
            lines.append('\t</expression>')
        
        lines.append('</%s>'%class_name)
        
        #write to metadata file
        file = self.get_file_name(year = year, extension = 'meta')
        path = os.path.join(self.source_data.get_indicator_directory(),
                            file)
        f = open(path, 'w')
        output = '\n'.join(lines)
        f.write(output)
        f.close()
        
        return lines
    
    def create_from_metadata(cls, file_path):
        '''creates and returns an indicator from the file pointed to in file_path 
        '''

        #TODO: If the additional child parameters are not strings, the current implementation will fail.
        
        f = open(file_path)
        
        version = f.readline()
        indicator_class = f.readline().strip()
        indicator_class = indicator_class[1:-1]
        
        in_expression = False
        in_source_data = False
        
        expression = None
        source_data_params = {}
        
        non_constructor_attr = {
            'date_computed': None
        }
        
        params = {}
        
        for line in f.readlines():
            line = line.strip()
            if line == '<expression>':
                in_expression = True
                expression = {}
            elif line == '</expression>':
                params['expression'] = expression
                in_expression = False
            elif line == '<source_data>':
                in_source_data = True
            elif line == '</source_data>':
                source_data = SourceData(**source_data_params)
                params['source_data'] = source_data
                in_source_data = False
            elif line != '</%s>'%indicator_class:
                (name, value) = AbstractIndicator._extract_name_and_value(line)
                
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
                
                if in_expression:
                    expression[name] = value
                elif in_source_data:
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
                
        #create indicator
        #TODO: better way to comb through and import available image types
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
            from opus_core.indicator_framework.image_types.dbf_export import DbfExport
            from opus_core.indicator_framework.image_types.matplotlib_map import Map
            from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
            from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
            from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
            from opus_core.indicator_framework.image_types.arcgeotiff_map import ArcGeotiffMap
        except:
            pass

        indicator = eval('%s(**params)'%indicator_class)
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

    #makes create_from_metadata and _extract_name_and_value a class method
    create_from_metadata = classmethod(create_from_metadata)
    _extract_name_and_value = classmethod(_extract_name_and_value)
    
    
import os
import tempfile
from opus_core.tests import opus_unittest

from shutil import copytree, rmtree

from opus_core.resources import Resources
from opus_core.variables.attribute_type import AttributeType
from opus_core.opus_package_info import package

from numpy import array

class AbstractIndicatorTest(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_cache_path = tempfile.mkdtemp(prefix='opus_tmp')    
        self.temp_cache_path2 = tempfile.mkdtemp(prefix='opus_tmp')
      
        baseyear_dir = os.path.join(self.temp_cache_path, '1980')
        storage = StorageFactory().get_storage('flt_storage', storage_location=baseyear_dir)
        storage.write_dataset(Resources({
           'out_table_name': 'tests',
           'values': {
               'id': array([1,2,3,4]),
               'attribute': array([5,6,7,8]),
               'attribute2': array([50,60,70,80])
               },
           'attrtype':{
               'id': AttributeType.PRIMARY,
               'attribute': AttributeType.PRIMARY,
               'attribute2': AttributeType.PRIMARY, 
               }
           }))
        
        copytree(baseyear_dir,  os.path.join(self.temp_cache_path2, '1980'))
        
        self.cross_scenario_source_data = SourceData(
            cache_directory = self.temp_cache_path,
            comparison_cache_directory = self.temp_cache_path2,
            years = [1980],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['opus_core'],
                package_order_exceptions={},
            )
        )
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
        rmtree(self.temp_cache_path2)
    

class Tests(AbstractIndicatorTest):                
    def test__get_indicator_path(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: pass
        else:
            
            table = Table(
                source_data = self.source_data,
                attribute = 'xxx.yyy.population',
                dataset_name = 'yyy',
                output_type = 'tab')
            returned_path = table.get_file_name()
            expected_path = 'yyy__tab__population.tab'
            
            self.assertEqual(returned_path, expected_path)

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
            
            lines = table._write_metadata()
            output = '\n'.join(lines)
            
            expected = (
                '<version>1.0</version>\n'          
                '<Table>\n'
                '\t<dataset_name>yyy</dataset_name>\n'
                '\t<years>[0, 1]</years>\n'
                '\t<date_computed>None</date_computed>\n'
                '\t<name>population</name>\n'
                '\t<attribute>xxx.yyy.population</attribute>\n'
                '\t<output_type>tab</output_type>\n'
                '\t<source_data>\n'
                '\t\t<cache_directory>%s</cache_directory>\n'
                '\t\t<comparison_cache_directory>%s</comparison_cache_directory>\n' 
                '\t\t<run_description></run_description>\n'
                '\t\t<years>[1980]</years>\n'
                '\t\t<package_order>[\'opus_core\']</package_order>\n'
                '\t</source_data>\n'
                '</Table>'
            )%(self.temp_cache_path,
               self.temp_cache_path2)
            
            self.assertEqual(output,expected)
            
    def test__read_write_metadata(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: pass
        else:
            
            table = Table(
                source_data = self.source_data,
                attribute = 'xxx.yyy.population',
                dataset_name = 'yyy',
                output_type = 'tab',
                years = [0,1] # Indicators are not actually being computed, so the years don't matter here.
            )
            
#            table.create(False)
            table._write_metadata()
            metadata_file = table.get_file_name(extension = 'meta')
            metadata_path = os.path.join(self.source_data.get_indicator_directory(),
                                         metadata_file)
            self.assertEqual(os.path.exists(metadata_path), True)
            
            expected_path = 'yyy__tab__population.meta'
            self.assertEqual(metadata_file,expected_path)
            
            new_table = AbstractIndicator.create_from_metadata(metadata_path)
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

    def test__output_types(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: pass

        else:
            for output_type in ['dbf','csv','tab']:
                table = Table(
                    source_data = self.cross_scenario_source_data,
                    attribute = 'package.test.attribute',
                    dataset_name = 'test',
                    output_type = output_type)
                
                
                table.create(False)
                path = table.get_file_path()
                self.assertEqual(os.path.exists(path), True)
                
    def test__cross_scenario_indicator(self):
        try:
            from opus_core.indicator_framework.image_types.table import Table
            from opus_core.indicator_framework.source_data import SourceData
        except: pass

        else:
            table = Table(
                source_data = self.cross_scenario_source_data,
                attribute = 'package.test.attribute',
                dataset_name = 'test',
                output_type = 'csv')
            
            
            table.create(False)
            path = table.get_file_path()
            f = open(path)
            f.readline() #chop off header
            for l in f.readlines():
                (id, value) = l.split(',')
                self.assertEqual(0, int(value.strip()))
    
    
if __name__ == '__main__':
    opus_unittest.main()
