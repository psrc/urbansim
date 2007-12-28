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

from inprocess.travis.opus_core.indicator_framework.utilities.integrity_error import IntegrityError
from inprocess.travis.opus_core.indicator_framework.representations.computed_indicator import ComputedIndicator
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger


from opus_core.storage_factory import StorageFactory
from opus_core.store.storage import Storage

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
        
        self.storage_location = os.path.join(self.source_data.get_indicator_directory(),
                                             '_stored_data')
        
        if not os.path.exists(self.source_data.get_indicator_directory()):
            os.mkdir(self.source_data.get_indicator_directory())
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
                    
        SimulationState().set_cache_directory(cache_directory) 
        
        self._check_integrity(indicators = indicators, 
                              result_template = result_template)
        
        computed_indicators = self._make_all_indicators(
            indicators = indicators,
            result_template = result_template)
        
        return computed_indicators

    def _make_all_indicators(self, indicators, result_template):
        
        computed_indicators = {}
        indicators_by_dataset = {}
        for year in result_template.years:
            SimulationState().set_current_time(year)
            SessionConfiguration(
                new_instance = True,
                package_order = self.package_order,
                package_order_exceptions = self.package_order_exceptions,
                in_storage = AttributeCache()) 
                    
            for name, indicator in indicators.items():
                dataset_name = indicator.dataset_name
                if dataset_name not in indicators_by_dataset:
                    indicators_by_dataset[dataset_name] = [(name,indicator)]
                else:
                    indicators_by_dataset[dataset_name].append((name,indicator))
                    
            for dataset_name, indicators_in_dataset in indicators_by_dataset.items():
                dataset = SessionConfiguration().get_dataset_from_pool(dataset_name)
                
                self._make_indicators_for_dataset(
                     dataset = dataset,
                     indicators_in_dataset = indicators_in_dataset,
                     result_template = result_template,
                     computed_indicators = computed_indicators,
                     year = year
                )
            
        self.computed_indicators[result_template.name] = computed_indicators
        return computed_indicators
    
    def _make_indicators_for_dataset(self, dataset, 
                                     indicators_in_dataset,
                                     result_template,
                                     computed_indicators,
                                     year):
        
        for name, indicator in indicators_in_dataset:
            computed_indicator = ComputedIndicator(
                indicator = indicator,
                result_template = result_template,
                dataset = dataset)
            
            computed_indicators[name] = computed_indicator
                
        table_name = dataset.get_dataset_name()
        storage_location = os.path.join(self.storage_location,
                                        repr(year))
            
        storage_type = 'flt'
        store = StorageFactory().get_storage(storage_type + '_storage', 
                                             storage_location = storage_location)
        
        already_computed_attributes = []
        if not os.path.exists(storage_location):
            os.mkdir(storage_location)
        else:
            if store.table_exists(table_name = table_name):
                already_computed_attributes = store.get_column_names(table_name = table_name)
                
        attributes = dataset.get_id_name() + [ind.attribute 
                                             for name,ind in indicators_in_dataset
                                             if computed_indicators[name].get_computed_dataset_column_name() 
                                                 not in already_computed_attributes]
        
        dataset.compute_variables(names = attributes)
        
        cols = copy(dataset.get_id_name())
        cols += [computed_indicators[name].get_computed_dataset_column_name() 
                for name, ind in indicators_in_dataset
                if computed_indicators[name].get_computed_dataset_column_name() 
                                                 not in already_computed_attributes]
        
        data = dict([(attribute, dataset.get_attribute(attribute))
                 for attribute in cols])

        store.write_table(
            table_name = table_name, 
            table_data = data,
            mode = Storage.APPEND
        )
        
        del dataset
        collect()

    def _check_integrity(self, indicators, result_template):        
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
                  attribute = 'opus_core.test.attribute')        
        
        maker = Maker()
        maker.create(indicator = indicator, 
                     result_template = self.source_data)
        
        for year in range(1980,1984):
            storage_location = os.path.join(self.source_data.get_indicator_directory(),
                                '_stored_data',
                                repr(year))
            self.assert_(os.path.exists(os.path.join(storage_location, 'test')))

            store = StorageFactory().get_storage(type = 'flt_storage',
                                                 storage_location = storage_location)
            cols = store.get_column_names(table_name = 'test')
            self.assertEqual(sorted(cols), sorted(['attribute','id']))
            
            id_vals = [1,2,3,4]
            attribute_vals = [5,6,7,8]
            attribute_vals_1983 = [10,12,14,16]
            
            data = store.load_table(table_name = 'test',
                                    column_names = cols)
            
            self.assertEqual(id_vals, list(data['id']))
            if year == 1983:
                self.assertEqual(attribute_vals_1983, list(data['attribute']))
            else:
                self.assertEqual(attribute_vals, list(data['attribute']))
            

    def test__indicator_expressions(self):
        maker = Maker()
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute',
            dataset_name = 'test')
        
        computed_indicator = maker.create(indicator = indicator,
                                           result_template = self.source_data)
        
        storage_location = os.path.join(self.source_data.get_indicator_directory(),
                            '_stored_data',
                            '1980')
        self.assert_(os.path.exists(os.path.join(storage_location, 'test')))

        store = StorageFactory().get_storage(type = 'flt_storage',
                                             storage_location = storage_location)
        cols = sorted(store.get_column_names(table_name = 'test'))
        self.assertTrue(len(cols[0])>10)
        truncated_cols = copy(cols)
        truncated_cols[0] = cols[0][:10]
        self.assertEqual(truncated_cols, ['autogenvar','id'])
        
        expected_attribute_vals = [10,12,14,16]
        
        data = store.load_table(table_name = 'test',
                                column_names = [cols[0]])
        
        self.assertEqual(expected_attribute_vals, list(data[cols[0]]))


    def test__indicator_expressions_with_two_variables(self):
        maker = Maker()
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute - opus_core.test.attribute2',
            dataset_name = 'test')
        
        computed_indicator = maker.create(indicator = indicator,
                                           result_template = self.source_data)
        
        storage_location = os.path.join(self.source_data.get_indicator_directory(),
                            '_stored_data',
                            '1980')
        self.assert_(os.path.exists(os.path.join(storage_location, 'test')))

        store = StorageFactory().get_storage(type = 'flt_storage',
                                             storage_location = storage_location)
        cols = store.get_column_names(table_name = 'test')
        attr_col = [col for col in cols if col != 'id'][0]
        
        expected_attribute_vals = [-40,-48,-56,-64]
        
        data = store.load_table(table_name = 'test',
                                column_names = [attr_col])
        
        self.assertEqual(expected_attribute_vals, list(data[attr_col]))

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
