
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

import os, sys, re
from time import strftime, localtime, time
from copy import copy
from gc import collect

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger

from opus_core.indicator_framework.utilities.gui_utilities import display_message_dialog
from opus_core.indicator_framework.core.indicator_data_manager import IndicatorDataManager
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.utilities.integrity_error import IntegrityError

from numpy import array, subtract, concatenate

class AbstractIndicator(object):
    
    def __init__(self, source_data, dataset_name, attribute, 
                 years = None, operation = None, name = None,
                 suppress_file_extension_addition = False ):

        self.dataset_name = dataset_name 
        self.attribute = attribute
        self.operation = operation
        self.source_data = source_data
        self.suppress_file_extension_addition = suppress_file_extension_addition

        self.name = name
        if self.name == None:
            self.name = self.get_attribute_alias()
            if self.operation is not None:
                self.name = '%s_%s'%(self.operation,self.name)
        
        if years is None:
            self.years = self.source_data.years
        else:
            self.years = years

        self.dataset = None
        self.dataset_state = {
              'current_cache_directory':None,
              'year':None
        }
        
        self.date_computed = None    
        self.run_description = self.source_data.get_run_description()

        # Use attribute cache so that can access info from prior years, too.
        (self.package_order, self.package_order_exceptions) = \
            self.source_data.get_package_order_and_exceptions()
            
        self.data_manager = IndicatorDataManager()
        
        cache_directory = self.source_data.cache_directory
        self._set_cache_directory(cache_directory)
        
        self._check_integrity()

    def _check_integrity(self):
        #do all years exist in cache dirs?
        cross_scenario_comparison = self.source_data.comparison_cache_directory != ''
        for year in self.years:
            year_dir = os.path.join(self.source_data.cache_directory, repr(year))
            if not os.path.exists(year_dir):
                raise IntegrityError('Year %i does not exist in cache directory %s'%
                                     (year, self.source_data.cache_directory))
            if cross_scenario_comparison:
                year_dir = os.path.join(self.source_data.comparison_cache_directory, repr(year))
                if not os.path.exists(year_dir):
                    raise IntegrityError('Year %i does not exist in comparison cache directory %s'%
                                         (year, self.source_data.comparison_cache_directory))
                    
        '''package does not exist'''
        if self.attribute != '':
            package = VariableName(self.attribute).get_package_name()
            if package != None and package not in self.package_order:
                raise IntegrityError('Package %s is not available'%package)
            
        '''dataset does not exist'''     
        try:
            dataset = self._get_dataset(year = self.years[0])
        except:
            raise IntegrityError('Dataset %s is not available'%self.dataset_name)
        
        '''attribute is not available for this dataset'''
#        this is disabled because it is unclear how expressions would work
#        if not dataset.has_attribute(self.attribute):
#            raise IntegrityError('Variable %s is not available'%self.attribute)
        
              
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
        self.in_expression = False
        
        if self.is_single_year_indicator_image_type():
            for year in self.years:
                try:
                    self._create_indicator(year = year)
                    self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
                    self.data_manager.export_indicator(indicator = self, 
                                                       source_data = self.source_data,
                                                       year = year)
                except Exception, e:
                    self._handle_indicator_error(e, display_error_box)
        else:
            try:
                self._create_indicator(years = self.years)
                self.date_computed = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
                self.data_manager.export_indicator(indicator = self,
                                                   source_data = self.source_data)
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

    def get_visualization_shorthand(self):
        '''Returns the shorthand for this output type
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.get_visualization_shorthand needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)
            
    def get_additional_metadata(self):
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
            
        #if sizes of the results differ across years, fill in missing data
        #TODO: investigate the use of lag variables to account for this issue
        sizes = [len(year_data) for year_data in results]
        min_size, max_size = (min(sizes),max(sizes))
        if min_size != max_size:
            for year in range(len(results)):
                filler = [-1 for i in range(max_size - len(results[year]))]
                results[year] = concatenate((results[year],filler))
                
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
        indicator_vals = self._compute_indicator(attribute, year)
        if self.operation is not None and not self.in_expression:
            #TODO: clean up this code with new style expressions in mind
            self.in_expression = True
            try:
                indicator_vals = self.perform_operation(self.operation, indicator_vals)
                dataset = self._get_dataset(year = year)
                dataset.add_attribute(indicator_vals, self.name)
            finally:
                self.in_expression = False
            
        return indicator_vals

    def _compute_indicator(self, attribute, year):
        attribute = attribute.replace('DDDD',repr(year))
        
        short_name = VariableName(attribute).get_alias()
        dataset = self._get_dataset(year = year)
        if short_name not in dataset.get_known_attribute_names():
            dataset.compute_variables(attribute)
        v = dataset.get_attribute(short_name)
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

        #only get dataset if its necessary                 
        if fetch_dataset: 
            SimulationState().set_current_time(year)
            SessionConfiguration().get_dataset_pool().remove_all_datasets()
                
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
        #TODO: less hacky way to do this
        if self.attribute[:10] == 'autogenvar':
            alias = VariableName(self.attribute).get_squished_expression()
        else:
            alias = VariableName(self.attribute).get_alias()
        
        if year is not None:
            alias = alias.replace('DDDD',repr(year))
           
        return alias
    
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
                                  self.get_visualization_shorthand(),
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
                 
        #TODO: improve error message
        message = ('Failed to generate indicator "%s"! Check the indicator log '
                'in the indicators directory of the "%s" cache for further '
                'details.\nError: %s.' % (self.name, self.source_data.cache_directory, e))
        logger.log_warning(message)
        logger.log_stack_trace()
        if display_error_box:
            display_message_dialog(message)

    def perform_operation(self, operation, values = None):
        results = None
        
        if operation == 'size':
            dataset = self._get_dataset()
            dataset.get_id_attribute()
            results = dataset.size()
            
        elif operation == 'percent_change':
            baseyear_values, years_found = self._get_indicator_for_years(self.attribute, [2000,])
            numerator = ( values[0] - baseyear_values[0,]) * 100
            denominator = ma.masked_where(baseyear_values[0,]==0, 
                                          baseyear_values[0,].astype(float32), 0.0)
            results = ma.filled( numerator / denominator )
            
        elif operation == 'change':
            baseyear_values, years_found = self._get_indicator_for_years(attribute, [2000,])
            results = values[0] - baseyear_values[0,]
            
        return results


from opus_core.tests import opus_unittest
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
        
class Tests(AbstractIndicatorTest):                
    def test__get_indicator_path(self):
        from opus_core.indicator_framework.image_types.table import Table
        table = Table(
            source_data = self.source_data,
            attribute = 'opus_core.test.population',
            dataset_name = 'test',
            output_type = 'tab')
        returned_path = table.get_file_name()
        expected_path = 'test__tab__population.tab'
        
        self.assertEqual(returned_path, expected_path)            

    def test__output_types(self):
        from opus_core.indicator_framework.image_types.table import Table
        for output_type in ['dbf','csv','tab']:
            table = Table(
                source_data = self.cross_scenario_source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                output_type = output_type)
            
            table.create(False)
            path = table.get_file_path()
            self.assertEqual(os.path.exists(path), True)
                
    def test__cross_scenario_indicator(self):
        from opus_core.indicator_framework.image_types.table import Table
        table = Table(
            source_data = self.cross_scenario_source_data,
            attribute = 'opus_core.test.attribute',
            dataset_name = 'test',
            output_type = 'csv')
        
        table.create(False)
        path = table.get_file_path()
        f = open(path)
        f.readline() #chop off header
        for l in f.readlines():
            (id, value) = l.split(',')
            self.assertEqual(0, int(value.strip()))

    def test__indicator_expressions(self):
        from opus_core.indicator_framework.image_types.table import Table
        table = Table(
            source_data = self.source_data,
            attribute = '2 * opus_core.test.attribute',
            dataset_name = 'test',
            output_type = 'csv')
        
        table.create(False)
        path = table.get_file_path()
        f = open(path)
        f.readline() #chop off header
    
        computed_vals = {}
        for l in f.readlines():
            (id, value) = l.split(',')
            computed_vals[int(id)] = int(value)
            
        true_vals = {}
        for i in range(len(self.id_vals)):
            true_vals[self.id_vals[i]] = 2 * self.attribute_vals[i]
        
        self.assertEqual(computed_vals,true_vals)

    def test__indicator_expressions_with_two_variables(self):
        from opus_core.indicator_framework.image_types.table import Table
        table = Table(
            source_data = self.source_data,
            attribute = '2 * opus_core.test.attribute - opus_core.test.attribute2',
            dataset_name = 'test',
            output_type = 'csv')
        
        table.create(False)
        path = table.get_file_path()
        f = open(path)
        f.readline() #chop off header
    
        computed_vals = {}
        for l in f.readlines():
            (id, value) = l.split(',')
            computed_vals[int(id)] = int(value)
            
        true_vals = {}
        for i in range(len(self.id_vals)):
            true_vals[self.id_vals[i]] = 2 * self.attribute_vals[i] - self.attribute_vals2[i]
        
        self.assertEqual(computed_vals,true_vals)
    
    def test__integrity_checker(self):
        from opus_core.indicator_framework.image_types.table import Table
        try:
            table = Table(
                source_data = self.source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                output_type = 'csv')
        except IntegrityError:
            self.assertTrue(False)
        
#        '''attribute3 is not available'''
#        try:
#            table = Table(
#                source_data = self.source_data,
#                attribute = 'package.test.attribute3',
#                dataset_name = 'test',
#                output_type = 'csv')
#        except IntegrityError:
#            pass
#        else:
#            self.assertTrue(False)   
        
        '''test2 is incorrect dataset'''     
        try:
            table = Table(
                source_data = self.source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test2',
                output_type = 'csv')
        except IntegrityError:
            pass
        else:
            self.assertTrue(False)  
                 
        '''package does not exist'''
        try:
            table = Table(
                source_data = self.source_data,
                attribute = 'package.test.attribute',
                dataset_name = 'test',
                output_type = 'csv')
        except IntegrityError:
            pass
        else:
            self.assertTrue(False)           

        bad_source = self.source_data
        bad_source.years = [1970]

        '''don't have data available for year 1970'''
        try:
            table = Table(
                source_data = self.source_data,
                attribute = 'opus_core.test.attribute',
                dataset_name = 'test',
                years = [1970],
                output_type = 'csv')
        except IntegrityError:
            pass
        else:
            self.assertTrue(False) 
            
if __name__ == '__main__':
    opus_unittest.main()
