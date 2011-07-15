# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
import os

from opus_core.storage_factory import StorageFactory
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.abstract_visualization import Visualization
from opus_core.database_management.database_server import DatabaseServer


from numpy import array

class Table(Visualization):
    ALL = 1
    PER_YEAR = 2
    PER_ATTRIBUTE = 3

    def __init__(self,
                 indicator_directory,
                 name = None,
                 output_type = None,
                 storage_location = None,
                 output_style = ALL,
                 fixed_field_format = None  # Only used with the 'fixed_field' output type
                ):

        if output_type == 'sql' and not isinstance(storage_location, DatabaseConfiguration):
            raise Exception("If Table output_type is 'sql', a Database object must be passed as storage_location.")
        elif output_type in ['dbf', 'csv', 'tab', 'esri', 'fixed_field'] and \
               storage_location is not None and \
               not isinstance(storage_location,str):
            raise Exception("If Table output_type is %s, storage_location must be a path to the output directory"%output_type)
        elif output_type not in ['dbf', 'csv', 'tab', 'sql', 'esri', 'fixed_field']:
            raise Exception("Table output_type must be either dbf, csv, tab, sql, esri, fixed_field, not %s"%output_type)

        if output_type == "fixed_field" and not fixed_field_format:
            raise ValueError("If Table output_type is 'fixed_field', an XML format string must be passed as fixed_field_format.")
        
        self.fixed_field_format = fixed_field_format

        if output_style not in [Table.ALL,
                                Table.PER_YEAR,
                                Table.PER_ATTRIBUTE]:
            raise Exception(('%s output_style is not appropriate.'%output_style,
                   'Choose from Table.ALL, Table.PER_YEAR, ',
                   'and Table.PER_ATTRIBUTE'))

        self.output_type = output_type
        self.output_style = output_style

        if storage_location is None:
            storage_location = indicator_directory
        elif output_type == 'sql':
            server = DatabaseServer(database_server_configuration = storage_location)
            if not server.has_database(database_name = storage_location.database_name):
                server.create_database(database_name = storage_location.database_name)
            storage_location = server.get_database(
                                   database_name = storage_location.database_name)
        self.storage_location = storage_location

        self.output_storage = StorageFactory().get_storage(
            type = '%s_storage'%(self.output_type),
            storage_location = storage_location
        )

        self.name = name
        self.indicator_directory = indicator_directory

    def get_file_extension(self):
        if self.output_type == 'sql':
            return None
        elif self.output_type == 'fixed_field':
            return self.output_storage.get_file_extension()
        else:
            return self.output_type

    def get_additional_metadata(self):
        metadata =  {'output_type':self.output_type,
                     'output_style': self.output_style}
        if self.output_type == 'fixed_field':
            metadata['fixed_field_format'] = self.fixed_field_format
        return metadata

    def get_visualization_type(self):
        return 'table-%i'%self.output_style

    def visualize(self,
                  indicators_to_visualize,
                  computed_indicators):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory."""

        #TODO: eliminate this example indicator stuff
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        source_data = example_indicator.source_data
        dataset_to_attribute_map = {}

        self._create_input_stores(years = source_data.years)
        for name, computed_indicator in computed_indicators.items():
            if name not in indicators_to_visualize: continue

            if computed_indicator.source_data != source_data:
                raise Exception('result templates in indicator batch must all be the same.')
            dataset_name = computed_indicator.indicator.dataset_name
            if dataset_name not in dataset_to_attribute_map:
                dataset_to_attribute_map[dataset_name] = []
            dataset_to_attribute_map[dataset_name].append(name)

        for dataset_name, indicator_names in dataset_to_attribute_map.items():
            visualization_representations = []
            attributes = [(name,computed_indicators[name].get_computed_dataset_column_name())
                          for name in indicator_names]
            example_indicator = computed_indicators[indicator_names[0]]
            primary_keys = example_indicator.primary_keys

            if self.output_style == Table.ALL:
                output_method = self.output_ALL
            elif self.output_style == Table.PER_YEAR:
                output_method = self.output_PER_YEAR
            elif self.output_style == Table.PER_ATTRIBUTE:
                output_method = self.output_PER_ATTRIBUTE

            viz_metadata = output_method(
                dataset_name = dataset_name,
                attributes = attributes,
                primary_keys = primary_keys,
                years = source_data.years,
                computed_indicators = computed_indicators)

            for indicator_names, table_name, years in viz_metadata:
                visualization_representations.append(
                    self._get_visualization_metadata(
                        computed_indicators = computed_indicators,
                        indicators_to_visualize = indicator_names,
                        table_name = table_name,
                        years = years))
                

        return visualization_representations

    def output_PER_YEAR(self,
                        dataset_name,
                        attributes,
                        primary_keys,
                        years, computed_indicators):

        per_year_data = self._get_PER_YEAR_form(
            dataset_name = dataset_name,
            attributes = attributes,
            primary_keys = primary_keys,
            years = years)

        viz_metadata = []
        for year, data_subset in per_year_data.items():
            if self.name is not None:
                table_name = self.name + '_%i'%year
            else:
                table_name = self.get_name(
                    dataset_name = dataset_name,
                    years = [year],
                    attribute_names = [name for name, computed_name in attributes])
            
            self._write_to_storage(
                table_name = table_name,
                table_data = data_subset,
                column_names = primary_keys + sorted([col for col in data_subset.keys()
                                                      if col not in primary_keys]),
                computed_indicators = computed_indicators,
                years = [year],
                primary_keys = primary_keys,
                dataset_name = dataset_name)

            viz_metadata.append(([name for name, computed_name in attributes],
                                 table_name,
                                 [year]))

        return viz_metadata

    def output_PER_ATTRIBUTE(self,
                            dataset_name,
                            attributes,
                            primary_keys,
                            years, computed_indicators):

        per_attribute_data = self._get_PER_ATTRIBUTE_form(
            dataset_name = dataset_name,
            attributes = attributes,
            primary_keys = primary_keys,
            years = years)

        viz_metadata = []
        for name, data_subset in per_attribute_data.items():
            if self.name is not None:
                table_name = self.name + '_%s'%name
            else:
                table_name = self.get_name(
                    dataset_name = dataset_name,
                    years = years,
                    attribute_names = [name])

            self._write_to_storage(
                table_name = table_name,
                table_data = data_subset,
                column_names = primary_keys + sorted([col for col in data_subset.keys()
                                                     if col not in primary_keys]),
                computed_indicators = computed_indicators,
                years = years,
                primary_keys = primary_keys,
                dataset_name = dataset_name
            )

            viz_metadata.append(([name], table_name, years))

        return viz_metadata

    def output_ALL(self,
                   dataset_name,
                   attributes,
                   primary_keys,
                   years, computed_indicators):

        new_data = self._get_ALL_form(
            dataset_name = dataset_name,
            attributes = attributes,
            primary_keys = primary_keys,
            years = years
        )

        table_name = self.get_name(
            dataset_name = dataset_name,
            years = years,
            attribute_names = [name for name, computed_name in attributes])
        if self.name is not None:
            table_name = '%s__%s'%(self.name, table_name)
            
	cols = [col for col in new_data.keys()
                                               if col not in primary_keys]
	cols.sort()
        self._write_to_storage(
            table_name = table_name,
            table_data = new_data,
            column_names = primary_keys + cols,
            computed_indicators = computed_indicators,
            years = years,
            primary_keys = primary_keys,
            dataset_name = dataset_name
        )
        return [([name for name, computed_name in attributes], table_name, years)]


    def _write_to_storage(self,
                          table_name,
                          table_data,
                          column_names, 
                          computed_indicators,
                          primary_keys,
                          years,
                          dataset_name):
        kwargs = {}
        if self.output_type in ['csv','tab']:
            kwargs['fixed_column_order'] = column_names
            #kwargs['append_type_info'] = False
        elif self.output_type in ['fixed_field']:
            if isinstance(self.fixed_field_format, str):
                format = self.fixed_field_format
            else:
                format = self.build_format_string(computed_indicators = computed_indicators, 
                                     column_names = column_names,
                                     years = years,
                                     primary_keys = primary_keys)
            kwargs['format'] = format
            
        self.output_storage.write_table(
            table_name = table_name,
            table_data = table_data,
        #    column_names = column_names,
            **kwargs)
        
        if self.output_type == 'sql':
            try:
                from opus_core.tools.create_view import create_view
                db = self.output_storage._get_db()
                if db.database_server_config.protocol != 'sqlite':
                    create_view(database = db,
                        table_to_link_name = table_name,
                        dataset_name = dataset_name)
            except:
                import traceback
                traceback.print_exc()
                
    
    def build_format_string(self, computed_indicators, column_names, years, primary_keys):
        format_list = []
        name_mapping = {}
        for name, computed_indicator in computed_indicators.items():
            for year in years:
                col_name = computed_indicator.get_computed_dataset_column_name(year = year)
                try:
                    i_name = computed_indicator.gui_indicator_name
                except:
                    i_name = computed_indicator.indicator.name
                    
                if i_name not in name_mapping:
                    name_mapping[i_name] = [col_name]
                else:
                    name_mapping[i_name].append(col_name)
       
        for (name, format) in self.fixed_field_format:
            if name == 'id':
                for key in primary_keys:
                    format_list.append((key,format))
            else:
                for col_name in name_mapping[name]:
                    if col_name in column_names:
                        format_list.append((col_name,format))
      
        return format_list            

    
from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
from opus_gui.results_manager.run.indicator_framework.maker.maker import Maker
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator

class Tests(AbstractIndicatorTest):
    def test_create_indicator(self):

        indicator_path = self.source_data.get_indicator_directory()
        self.assert_(not os.path.exists(indicator_path))

        self.source_data.years = range(1980,1984)
        indicator = Indicator(
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute'
        )

        indicator2 = Indicator(
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute2'
        )

        maker = Maker(project_name = 'test', test = True)
        computed_indicators = maker.create_batch(
            indicators = {'attr1':indicator,
                          'attr2':indicator2},
            source_data = self.source_data)

        for style in [Table.ALL, Table.PER_YEAR, Table.PER_ATTRIBUTE]:
            table = Table(indicator_directory = self.source_data.get_indicator_directory(),
                          output_type = 'csv',
                          output_style = style)
            table._create_input_stores(range(1980,1984))

            viz_results = table.visualize(
                            indicators_to_visualize = ['attr1',
                                                       'attr2'],
                            computed_indicators = computed_indicators)


            for viz_result in viz_results:
                if style == Table.ALL:
                    file_name = 'test_table-%i_1980-1983_attr1-attr2.csv'%style
                elif style == Table.PER_YEAR:
                    file_name = 'test_table-%i_%i_attr1-attr2.csv'%(style,viz_result.years[0])
                elif style == Table.PER_ATTRIBUTE:
                    if viz_result.indicators[0].indicator.name == 'attribute':
                        name = 'attr1'
                    else:
                        name = 'attr2'
                    file_name = 'test_table-%i_1980-1983_%s.csv'%(style, name)

                self.assertEqual(
                     os.path.join(viz_result.storage_location,
                                  viz_result.table_name + '.' + viz_result.file_extension),
                     os.path.join(indicator_path, file_name))

    def test__output_PER_ATTRIBUTE(self):
        indicator_directory = self.source_data.get_indicator_directory()
        table = Table(indicator_directory = indicator_directory,
                      output_type = 'csv')

        table._create_input_stores([2000,2002])

        input_2000 = {
            'id':array([1,2,3]),
            'id2':array([3,4,5]),
            'attr1':array([1,2,3]),
            'attr2':array([2,3,4]),
        }

        input_2002 = {
            'id':array([1,2,4]),
            'id2':array([3,4,5]),
            'attr1':array([10,20,30]),
            'attr2':array([20,30,40]),
        }

        expected1 = {
            'id':array([1,2,3,4]),
            'id2':array([3,4,5,5]),
            'attr1_2000':array([1,2,3,-1]),
            'attr1_2002':array([10,20,-1,30]),
        }

        expected2 = {
            'id':array([1,2,3,4]),
            'id2':array([3,4,5,5]),
            'attr2_2000':array([2,3,4,-1]),
            'attr2_2002':array([20,30,-1,40]),
        }

        for year in [2000,2002]:
            input_storage = StorageFactory().get_storage(
                type = 'flt_storage',
                storage_location = os.path.join(
                                    self.source_data.get_indicator_directory(),
                                    '_stored_data',
                                    repr(year)))
            if year == 2000:
                data = input_2000
            else:
                data = input_2002

            input_storage.write_table(
                table_name = 'test',
                table_data = data
            )

        viz_metadata = table.output_PER_ATTRIBUTE(
            dataset_name = 'test',
            attributes = [('attr1','attr1'),('attr2','attr2')],
            primary_keys = ['id','id2'],
            years = [2000,2002],
            computed_indicators = [])

        storage = StorageFactory().get_storage(
            type = 'csv_storage',
            storage_location = indicator_directory
        )

        for attributes, table_name, years in viz_metadata:
            self.assertEqual(years, [2000,2002])
            self.assertTrue(attributes in [['attr1'],['attr2']])
            self.assertTrue(os.path.exists(os.path.join(indicator_directory,
                                                        table_name + '.csv')))
            output = storage.load_table(table_name = table_name)
            if attributes == ['attr1']:
                expected = expected1
            else:
                expected = expected2

            self.assertEqual(len(expected.keys()), len(output.keys()))
            for k,v in expected.items():
                self.assertEqual(list(v), list(output[k]))

    def test__output_PER_YEAR(self):
        indicator_directory = self.source_data.get_indicator_directory()
        table = Table(indicator_directory = indicator_directory,
                      output_type = 'csv')
        table._create_input_stores([2000,2002])

        input_2000 = {
            'id':array([1,2,3]),
            'id2':array([3,4,5]),
            'attr1':array([1,2,3]),
            'attr2':array([2,3,4]),
        }

        input_2002 = {
            'id':array([1,2,4]),
            'id2':array([3,4,5]),
            'attr1':array([10,20,30]),
            'attr2':array([20,30,40]),
        }

        expected_2000 = {
            'id':array([1,2,3]),
            'id2':array([3,4,5]),
            'attr1_2000':array([1,2,3]),
            'attr2_2000':array([2,3,4]),
        }

        expected_2002 = {
            'id':array([1,2,4]),
            'id2':array([3,4,5]),
            'attr1_2002':array([10,20,30]),
            'attr2_2002':array([20,30,40]),
        }

        for year in [2000,2002]:
            input_storage = StorageFactory().get_storage(
                type = 'flt_storage',
                storage_location = os.path.join(
                                    self.source_data.get_indicator_directory(),
                                    '_stored_data',
                                    repr(year)))
            if year == 2000:
                data = input_2000
            else:
                data = input_2002

            input_storage.write_table(
                table_name = 'test',
                table_data = data
            )

        viz_metadata = table.output_PER_YEAR(
            dataset_name = 'test',
            attributes = [('attr1','attr1'),('attr2','attr2')],
            primary_keys = ['id','id2'],
            years = [2000,2002],
            computed_indicators = [])

        storage = StorageFactory().get_storage(
            type = 'csv_storage',
            storage_location = indicator_directory
        )

        for attributes, table_name, years in viz_metadata:
            self.assertTrue(years in [[2000],[2002]])
            self.assertEqual(attributes, ['attr1','attr2'])
            self.assertTrue(os.path.exists(os.path.join(indicator_directory,
                                                        table_name + '.csv')))
            output = storage.load_table(table_name = table_name)
            if years == [2000]:
                expected = expected_2000
            else:
                expected = expected_2002

            self.assertEqual(len(expected.keys()), len(output.keys()))
            for k,v in expected.items():
                self.assertEqual(list(v), list(output[k]))

    def test__output_types(self):
        output_types = ['csv','tab','fixed_field']
        try:
            import dbfpy
        except ImportError:
            pass
        else:
            output_types.append('dbf')

        try:

            test_db_name = 'test_db_for_indicator_framework'
            database_config = DatabaseConfiguration(
                 database_name = test_db_name,
                 test = True,
            )

            server = DatabaseServer(database_config)
            server.drop_database(database_name = test_db_name)
            server.create_database(database_name = test_db_name)

        except:
            has_sql = False
        else:
            has_sql = True
            output_types.append('sql')

        indicator = Indicator(
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute'
        )

        maker = Maker(project_name = 'test', test = True)
        computed_indicators = maker.create_batch(
            indicators = {'attr1':indicator},
            source_data = self.source_data)

        for output_type in output_types:
            kwargs = {}
            if output_type == 'sql':
                kwargs['storage_location'] = database_config
            elif output_type == 'fixed_field':
                kwargs['fixed_field_format'] = '<fixed_field><field name="attribute_1980" format="10f" /></fixed_field>'

            table = Table(
                        indicator_directory = self.source_data.get_indicator_directory(),
                        output_type = output_type,
                        **kwargs)
            table._create_input_stores(self.source_data.years)
            viz_result = table.visualize(
                        indicators_to_visualize = ['attr1'],
                        computed_indicators = computed_indicators)[0]
            if output_type in ['csv','dbf','tab','fixed_field']:
                self.assertTrue(os.path.exists(
                   os.path.join(viz_result.storage_location,
                   viz_result.table_name + '.' + viz_result.file_extension)))
            elif output_type == 'sql':
                self.assertTrue(server.has_database(test_db_name))
                db = server.get_database(test_db_name)
                self.assertTrue(db.table_exists(table_name = viz_result.table_name))
        if has_sql:
            server.drop_database(database_name = test_db_name)

if __name__ == '__main__':
    opus_unittest.main()
