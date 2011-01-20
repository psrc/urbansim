# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from gc import collect
from copy import copy

from opus_gui.results_manager.run.indicator_framework.utilities.integrity_error import IntegrityError
from opus_gui.results_manager.run.indicator_framework.representations.computed_indicator import ComputedIndicator
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator

from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger

from time import strftime,localtime
from opus_core.storage_factory import StorageFactory
from opus_core.store.storage import Storage
from opus_core.variables.variable_factory import VariableFactory

from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.services.run_server.results_manager import ResultsManager

class Maker(object):
    def __init__(self, project_name, test = False, expression_library = None):
        self.computed_indicators = {}
        self.test = test
        self.project_name = project_name
        self.expression_library = expression_library

    def create(self, indicator, source_data):
        computed_indicators = self.create_batch(
                                indicators = {indicator.name:indicator},
                                source_data = source_data)
        return computed_indicators[indicator.name]

    def create_batch(self, indicators, source_data):
        self.source_data = source_data
        cache_directory = self.source_data.cache_directory

        self.storage_location = os.path.join(self.source_data.get_indicator_directory(),
                                             '_stored_data')

        if not os.path.exists(self.source_data.get_indicator_directory()):
            os.mkdir(self.source_data.get_indicator_directory())
        if not os.path.exists(self.storage_location):
            os.mkdir(self.storage_location)

        log_file_path = os.path.join(cache_directory,
                                     'indicators',
                                     'indicators.log')
        logger.enable_file_logging(log_file_path, 'a')
        logger.log_status('\n%s Indicator Generation BEGIN %s %s'
            % ('='*10, strftime('%Y_%m_%d_%H_%M', localtime()), '='*10))

        self.dataset = None
        self.dataset_state = {
              'current_cache_directory':None,
              'year':None,
              'dataset_name':None
        }

        self.package_order = self.source_data.get_package_order()

        SimulationState().set_cache_directory(cache_directory)

        self._check_integrity(indicators = indicators,
                              source_data = source_data)

        computed_indicators = self._make_all_indicators(
            indicators = indicators,
            source_data = source_data)

        if not self.test:
            self.write_computed_indicators_to_db(computed_indicator_group = computed_indicators,
                                                 project_name = self.project_name)

        logger.log_status('%s Indicator Generation END %s %s\n'
            % ('='*11, strftime('%Y_%m_%d_%H_%M', localtime()), '='*11))
        logger.disable_file_logging(log_file_path)

        return computed_indicators

    def _make_all_indicators(self, indicators, source_data):

        computed_indicators = {}
        indicators_by_dataset = {}
        for year in source_data.years:
            SimulationState().set_current_time(year)
            SessionConfiguration(
                new_instance = True,
                package_order = self.package_order,
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
                     source_data = source_data,
                     computed_indicators = computed_indicators,
                     year = year
                )

        self.computed_indicators[source_data.name] = computed_indicators
        return computed_indicators

    def _make_indicators_for_dataset(self, dataset,
                                     indicators_in_dataset,
                                     source_data,
                                     computed_indicators,
                                     year):

        for name, indicator in indicators_in_dataset:
            computed_indicator = ComputedIndicator(
                indicator = indicator,
                source_data = source_data,
                dataset_name = dataset.get_dataset_name(),
                primary_keys = copy(dataset.get_id_name()))

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
        if self.expression_library is not None:
            VariableFactory().set_expression_library(self.expression_library)
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

    def write_computed_indicators_to_db(self, computed_indicator_group, project_name):
        options = ServicesDatabaseConfiguration()
        results_manager = ResultsManager(options)

        for name, indicator in computed_indicator_group.items():
            results_manager.add_computed_indicator(
                    indicator_name = indicator.indicator.name,
                    dataset_name = indicator.dataset_name,
                    expression = indicator.indicator.attribute,
                    run_id = indicator.source_data.run_id,
                    data_path = indicator.get_file_path(),
                    project_name = project_name)

        results_manager.close()

    def _check_integrity(self, indicators, source_data):
        for name, indicator in indicators.items():
            attribute = indicator.attribute
            package = VariableName(attribute).get_package_name()
            if package != None and package not in self.package_order:
                raise IntegrityError('Package %s is not available'%package)


from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    def test_create_indicator_multiple_years(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        self.source_data.years = range(1980,1984)
        indicator = Indicator(
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute')

        maker = Maker(project_name = 'test', test = True)
        maker.create(indicator = indicator,
                     source_data = self.source_data)

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
        maker = Maker(project_name = 'test', test = True)
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute',
            dataset_name = 'test')

        computed_indicator = maker.create(indicator = indicator,
                                           source_data = self.source_data)

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
        maker = Maker(project_name = 'test', test = True)
        indicator = Indicator(
            attribute = '2 * opus_core.test.attribute - opus_core.test.attribute2',
            dataset_name = 'test')

        computed_indicator = maker.create(indicator = indicator,
                                           source_data = self.source_data)

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
        from opus_gui.results_manager.run.indicator_framework.visualizers.table import Table
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
        maker = Maker(project_name = 'test', test = True)

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
