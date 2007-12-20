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

import os

from copy import copy
from gc import collect

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger

from inprocess.travis.opus_core.indicator_framework.utilities.integrity_error import IntegrityError
from inprocess.travis.opus_core.indicator_framework.representations.computed_indicator import ComputedIndicator
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator

from numpy import array, subtract, concatenate
from opus_core.storage_factory import StorageFactory

from inprocess.travis.opus_core.indicator_framework.maker.dataset_junior import DatasetJunior

class Maker(object):
    def __init__(self):
        self.computed_indicators = {}
    
    def create(self, indicator, result_template):
        computed_indicators = self.create_batch(
                                indicators = {indicator.name:indicator}, 
                                result_template = result_template)
        return computed_indicators[indicator.name]
        
    def create_batch(self, indicators, result_template):
        self.source_data = result_template

        cache_directory = self.source_data.cache_directory
        
        self.storage_location = self.source_data.get_indicator_directory()
        if not os.path.exists(self.storage_location):
            os.mkdir(self.storage_location)
                
        self.dataset = None
        self.dataset_state = {
              'current_cache_directory':None,
              'year':None,
              'dataset_name':None
        }
                
        # Use attribute cache so that can access info from prior years, too.
        (self.package_order, self.package_order_exceptions) = \
            self.source_data.get_package_order_and_exceptions()
                    
        self._set_cache_directory(cache_directory)
        
        self._check_integrity(indicators = indicators, 
                              result_template = result_template)
        
        computed_indicators = self._make_all_indicators(indicators = indicators,
                                                        result_template = result_template)
        
        return computed_indicators

    def _make_all_indicators(self, indicators, result_template):
        self.in_expression = False
        
        computed_indicators = {}
        datasets = {}
        
        for year in self.source_data.years:
            for name, indicator in indicators.items():
                dataset_junior = self._get_indicator_values_for_year(
                        year = year, 
                        indicator = indicator)
                dataset_junior.reduce()
                unique_dataset_identifier = indicator.dataset_name
                if unique_dataset_identifier in datasets:
                    datasets[unique_dataset_identifier].join(
                             dataset = dataset_junior, 
                             fill_value = -1)
                else:
                    datasets[unique_dataset_identifier] = dataset_junior
                
            self._release_dataset()
                        
        for name, indicator in indicators.items():
            computed_indicator = ComputedIndicator(
                indicator = indicator,
                result_template = self.source_data,
                dataset_metadata = {'dataset_name':indicator.dataset_name,
                                    'primary_keys':datasets[indicator.dataset_name].primary_keys})
            
            computed_indicators[name] = computed_indicator
                        
        for dataset_name, dataset in datasets.items():
            self._write_dataset(dataset = dataset)
                
        self.computed_indicators[result_template.name] = computed_indicators
        return computed_indicators
                    
    ####### Helper methods for indicator computations #############

    def _get_indicator_values_for_year(self, year, indicator):
        '''Returns a dataset_junior with the appropriate columns'''
        
        dataset = self._get_indicator_helper(indicator, year)
        
        #handle cross-scenario indicator comparisons
        cache_dir2 = self.source_data.comparison_cache_directory
        if cache_dir2 != '' and indicator.attribute not in dataset.primary_keys:
            #save old dataset
            old_dataset_state = copy(self.dataset_state)
            
            #compute values for cache_dir2 and get the difference
            self._set_cache_directory(cache_dir2)
            dataset2 = self._get_indicator_helper(indicator, year)
            
            #reload cache_dir's dataset with the proper values in the attribute            
            short_name = VariableName(indicator.attribute.replace('DDDD',repr(year))).get_alias()

            dataset.binary_operation(
                dataset = dataset2,
                column = short_name,
                operation = 'subtract')
            
            self._set_dataset(dataset, old_dataset_state)

        return dataset
            
    def _get_indicator_helper(self, indicator, year):
        '''Returns a dataset_junior with the appropriate columns'''
            
        dataset = self._get_dataset(year = year, 
                                    dataset_name = indicator.dataset_name)
        dataset.compute(indicator = indicator, year = year)
        
        if indicator.operation is not None and not self.in_expression:
            self.in_expression = True
            try:
                replacement_vals = self._perform_operation(indicator, indicator.operation, dataset)
                dataset.replace(indicator, replacement_vals)
            finally:
                self.in_expression = False
        
        return dataset

    def _perform_operation(self, indicator, operation, dataset):
        results = None
        #TODO: baseyear shouldn't be hardcoded
        #TODO: update operations        
        baseyear = 2000
        
        if operation == 'percent_change':
            baseyear_values = self._get_indicator_values_for_year(
              year = baseyear, 
              indicator = indicator)
            numerator = ( values - baseyear_values) * 100
            denominator = ma.masked_where(baseyear_values==0, 
                                          baseyear_values.astype(float32), 0.0)
            results = ma.filled( numerator / denominator )
            
        elif operation == 'change':
            baseyear_values = self._get_indicator_values_for_year(
              year = baseyear, 
              indicator = indicator)
            results = values - baseyear_values
            
        return results
    
    ######## Output #############
    def _write_dataset(self, dataset):
        storage_type = 'csv'
        store = StorageFactory().get_storage(storage_type + '_storage', 
                                             storage_location = self.storage_location) 
        
        non_primary_keys = sorted([col for col in dataset.get_columns() if col not in dataset.primary_keys])
        cols = dataset.primary_keys + non_primary_keys

        store.write_table(
            table_name = dataset.name, 
            table_data = dataset.get_column_representation(), 
            fixed_column_order = cols)
    
    ######## Cache management #########
        
    def _set_cache_directory(self, cache_directory):
        if cache_directory != SimulationState().get_cache_directory():
            SimulationState().set_cache_directory(cache_directory) 
            SessionConfiguration(
                new_instance = True,
                package_order = self.package_order,
                package_order_exceptions = self.package_order_exceptions,
                in_storage = AttributeCache()) 
                        
    def _set_dataset(self, dataset, dataset_state):
        if self.dataset_state['current_cache_directory'] != dataset_state['current_cache_directory']:
            self._set_cache_directory(dataset_state['current_cache_directory'])
        if self.dataset_state['year'] != dataset_state['year']:
            SimulationState().set_current_time(dataset_state['year'])
            
        self.dataset = dataset
        self.dataset_state = dataset_state
        
    def _release_dataset(self):
        del self.dataset
        collect()
        self.dataset = None
               
    def _get_dataset(self, dataset_name, year = None):
        
        if year == None: 
            year = SimulationState().get_current_time()
        
        fetch_dataset = (self.dataset == None or
                         self.dataset_state['year'] != year or
                         self.dataset_state['current_cache_directory'] != SimulationState().cache_directory or
                         self.dataset_state['dataset_name'] != dataset_name)

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
            self.dataset_state['year'] = SimulationState().get_current_time()
            self.dataset_state['current_cache_directory'] = SimulationState().cache_directory
            self.dataset_state['dataset_name'] = dataset_name
                
            self.dataset = DatasetJunior(dataset = SessionConfiguration().get_dataset_from_pool(dataset_name),
                                         name = dataset_name)
        return self.dataset
    

        
    ########### Error and integrity checking ##############
    def _handle_indicator_error(self, e, display_error_box = False):
        ''' sends alert to various forums if there's an error '''
                 
        message = ('Failed to generate indicator "%s"! Check the indicator log '
                'in the indicators directory of the "%s" cache for further '
                'details.\nError: %s.' % (self.name, self.source_data.cache_directory, e))
        logger.log_warning(message)
        logger.log_stack_trace()
#        if display_error_box:
#            display_message_dialog(message)

    def _check_integrity(self, indicators, result_template):
        '''package does not exist'''
        
        for name, indicator in indicators.items():
            attribute = indicator.attribute
            package = VariableName(attribute).get_package_name()
            if package != None and package not in self.package_order:
                raise IntegrityError('Package %s is not available'%package)
            
        '''dataset does not exist'''     
#        try:
#            dataset = self._get_dataset(year = self.years[0])
#        except:
#            raise IntegrityError('Dataset %s is not available'%self.dataset_name)
        
        '''attribute is not available for this dataset'''
#        this is disabled because it is unclear how expressions would work
#        if not dataset.has_attribute(self.attribute):
#            raise IntegrityError('Variable %s is not available'%self.attribute)


from opus_core.tests import opus_unittest
from inprocess.travis.opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
        
class Tests(AbstractIndicatorTest):            
    def test_create_indicator_multiple_years(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        self.source_data.years = range(1980,1984)
        indicator = Indicator(
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute'
        )        
        
        maker = Maker()
        maker.create(indicator = indicator, 
                     result_template = self.source_data)
        
        path = os.path.join(self.source_data.get_indicator_directory(),
                            'test.csv')
        
        #file_path = os.path.join(indicator_path, 'test__attribute__1980-1981-1982-1983.csv')
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(path))
        
        f = open(path)
        cols = [col.strip() for col in f.readline().split(',')]
        lines = f.readlines()
        f.close()
        data = []
        i = 0
        for line in lines:
            line = line.strip()
            if line == '': continue
            row = [int(r.strip()) for r in line.split(',')]
            #rows should all be tuples with all cols defined
            self.assertEqual(len(cols), len(row))
            #rows should be ordered by primary id
            self.assertEqual(row[0],self.id_vals[i])
            for col_index in range(1,len(cols)):
                #each attribute value should be correct
                if cols[col_index] == 'opus_core.test.attribute_1983:i4':
                    self.assertEqual(row[col_index],self.attribute_vals_diff[i])
                else:
                    self.assertEqual(row[col_index],self.attribute_vals[i])
            i += 1
            data.append(row)
        self.assertEqual(len(data),4)

    def test__indicator_expressions(self):
        maker = Maker()
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute',
            dataset_name = 'test')
        
        computed_indicator = maker.create(indicator = indicator,
                                           result_template = self.source_data)
        
        path = os.path.join(self.source_data.get_indicator_directory(),
                            'test.csv') #computed_indicator.get_file_path(years = self.source_data.years)
        f = open(path)
        f.readline() #chop off header
    
        computed_vals = {}
        for l in f.readlines():
            (id, value) = l.split(',')
            computed_vals[int(id)] = int(value)
        
        f.close()
        true_vals = {}
        for i in range(len(self.id_vals)):
            true_vals[self.id_vals[i]] = 2 * self.attribute_vals[i]
        
        self.assertEqual(computed_vals,true_vals)

    def test__indicator_expressions_with_two_variables(self):
        maker = Maker()
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute - opus_core.test.attribute2',
            dataset_name = 'test')
        
        computed_indicator = maker.create(indicator = indicator,
                                           result_template = self.source_data)
        
        path = os.path.join(self.source_data.get_indicator_directory(),
                    'test.csv')
#        path = computed_indicator.get_file_path(years = self.source_data.years)

        f = open(path)
        f.readline() #chop off header
    
        computed_vals = {}
        for l in f.readlines():
            (id, value) = l.split(',')
            computed_vals[int(id)] = int(value)
            
        f.close()
        true_vals = {}
        for i in range(len(self.id_vals)):
            true_vals[self.id_vals[i]] = 2 * self.attribute_vals[i] - self.attribute_vals2[i]
        
        self.assertEqual(computed_vals,true_vals)

    def skip_test__cross_scenario_indicator(self):
        from inprocess.travis.opus_core.indicator_framework.visualizers.table import Table
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

    def skip_test__change_expression(self):
        pass
                        
    def test__integrity_checker(self):
        maker = Maker()

        '''package does not exist'''
        indicator = Indicator(
            attribute = 'package.test.attribute',
            dataset_name = 'test')       
        
        self.assertRaises(IntegrityError,
                          maker.create,
                          indicator,
                          self.source_data)
        
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
        
#        '''test2 is incorrect dataset'''     
#        try:
#            table = Table(
#                source_data = self.source_data,
#                attribute = 'opus_core.test.attribute',
#                dataset_name = 'test2',
#                output_type = 'csv')
#        except IntegrityError:
#            pass
#        else:
#            self.assertTrue(False)  
                 

            
if __name__ == '__main__':
    opus_unittest.main()
