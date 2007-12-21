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

from gc import collect
from copy import copy

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger

from inprocess.travis.opus_core.indicator_framework.utilities.integrity_error import IntegrityError
from inprocess.travis.opus_core.indicator_framework.representations.computed_indicator import ComputedIndicator
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator

from opus_core.storage_factory import StorageFactory
from opus_core.datasets.multiple_year_dataset_view import MultipleYearDatasetView

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

        (self.package_order, self.package_order_exceptions) = \
            self.source_data.get_package_order_and_exceptions()
                    
        self._set_cache_directory(cache_directory)
        
        self._check_integrity(indicators = indicators, 
                              result_template = result_template)
        
        computed_indicators = self._make_all_indicators(
            indicators = indicators,
            result_template = result_template)
        
        return computed_indicators

    def _make_all_indicators(self, indicators, result_template):
        self.in_expression = False
        
        computed_indicators = {}
        indicators_by_dataset = {}
        for name, indicator in indicators.items():
            dataset_name = indicator.dataset_name
            if dataset_name not in indicators_by_dataset:
                indicators_by_dataset[dataset_name] = [(name,indicator)]
            else:
                indicators_by_dataset[dataset_name].append((name,indicator))
                
        for dataset_name, indicators_in_dataset in indicators_by_dataset.items():
            self._make_indicators_for_dataset(
                 dataset_name = dataset_name,
                 indicators_in_dataset = indicators_in_dataset,
                 result_template = result_template,
                 computed_indicators = computed_indicators
            )
            
        self.computed_indicators[result_template.name] = computed_indicators
        return computed_indicators
    
    def _make_indicators_for_dataset(self, dataset_name, 
                                     indicators_in_dataset,
                                     result_template,
                                     computed_indicators):
        in_table_name = dataset_name
        dataset = MultipleYearDatasetView(
            name_of_dataset_to_merge = dataset_name,
            in_table_name = in_table_name,
            attribute_cache = AttributeCache(),
            years_to_merge = result_template.years)
            
        attributes = dataset.base_id_name + [ind.attribute 
                                             for name,ind in indicators_in_dataset]
        dataset.compute_variables(names = attributes)
        
        for name, indicator in indicators_in_dataset:
            computed_indicator = ComputedIndicator(
                indicator = indicator,
                result_template = result_template,
                dataset = dataset)
            
            computed_indicators[name] = computed_indicator
            
        self._write_dataset(
            dataset = dataset, 
            indicators_in_dataset = indicators_in_dataset,
            computed_indicators = computed_indicators)
        
        del dataset
        collect()

    ######## Output #############
    def _write_dataset(self, 
                       dataset, 
                       indicators_in_dataset,
                       computed_indicators):        
        cols = copy(dataset.get_id_name())
        cols += [computed_indicators[name].get_computed_dataset_column_name() 
                for name, ind in indicators_in_dataset]
        data = {}
        for attribute in cols:
            data[attribute] = dataset.get_attribute(attribute)
        
        storage_type = 'csv'
        store = StorageFactory().get_storage(storage_type + '_storage', 
                                             storage_location = self.storage_location)
        
        store.write_table(
            table_name = dataset.get_dataset_name(), 
            table_data = data,
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
            

from opus_core.tests import opus_unittest
from inprocess.travis.opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
        
class Tests(AbstractIndicatorTest):            
    def test_create_indicator_multiple_years(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        self.source_data.years = range(1980,1984)
        indicator = Indicator(
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute',
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
        self.assertEqual(['id:i4','year:i4','attribute:i4'], cols)
        
        lines = f.readlines()
        f.close()
        data = []
        i = 0

        processed_years = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            row = [int(r.strip()) for r in line.split(',')]
            #rows should all be tuples with all cols defined
            self.assertEqual(len(cols), len(row))
            
            id = row[0]
            year = row[1]
            val = row[2]
            if year not in processed_years:
                processed_years.append(year)
                i = 0
            
            self.assertEqual(self.id_vals[i], id)
            if year == 1983:
                self.assertEqual(self.attribute_vals_diff[i], val)
            else:
                self.assertEqual(self.attribute_vals[i],val)

            i += 1
            data.append(row)

        self.assertEqual(len(data),16)
        self.assertEqual(processed_years, self.source_data.years)

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
            (id, year, value) = l.split(',')
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
            (id, year, value) = l.split(',')
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
    
    def skip_test_DDDD(self):
        pass
    
    def skip_baseyear_change_using_DDDD(self):
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
                 

            
if __name__ == '__main__':
    opus_unittest.main()
