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
import os
    
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_configuration import DatabaseConfiguration
from inprocess.travis.opus_core.indicator_framework.visualizer.visualizers.abstract_visualization import Visualization

from numpy import where, array

class Table(Visualization):
    ALL = 1
    PER_YEAR = 2
    PER_ATTRIBUTE = 3
    
    def __init__(self, 
                 indicator_directory,
                 name = None,
                 output_type = None,
                 storage_location = None,
                 output_style = ALL):
        
        if output_type == 'sql' and not isinstance(storage_location, DatabaseConfiguration): 
            raise "If Table output_type is 'sql', a Database object must be passed as storage_location."
        elif output_type in ['dbf', 'csv', 'tab'] and \
               storage_location is not None and \
               not isinstance(storage_location,str):
            raise "If Table output_type is %s, storage_location must be a path to the output directory"%output_type
        elif output_type not in ['dbf', 'csv', 'tab', 'sql']:
            raise "Table output_type must be either dbf, csv, tab, or sql"
        
        if output_style not in [Table.ALL, 
                                Table.PER_YEAR, 
                                Table.PER_ATTRIBUTE]:
            raise ('%s output_style is not appropriate.'%output_style, 
                   'Choose from Table.ALL, Table.PER_YEAR, ',
                   'and Table.PER_ATTRIBUTE')
            
        self.output_type = output_type
        self.output_style = output_style
        
        if storage_location is None:
            storage_location = indicator_directory
        self.storage_location = storage_location
                    
        self.output_storage = StorageFactory().get_storage(
            type = '%s_storage'%(self.output_type),
            storage_location = storage_location
        )
        
        self.input_storage = StorageFactory().get_storage(
            type = 'csv_storage',
            storage_location = indicator_directory)
        self.indicator_directory = indicator_directory
        self.name = name
    
    def get_file_extension(self):
        if self.output_type == 'sql':
            return None
        else:
            return self.output_type
    
    def get_visualization_shorthand(self):
        viz_map = {
           'csv':'table',
           'tab':'tab',
           'dbf':'dbf',
           'sql':'sql'
        }
        return viz_map[self.output_type]
              
    def get_additional_metadata(self):
        return  [('output_type',self.output_type)]
        
    def get_visualization_type(self):
        return 'table-%i'%self.output_style
    
    def visualize(self, 
                  indicators_to_visualize,
                  computed_indicators):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory."""
        
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        dataset_name = example_indicator.dataset_metadata['dataset_name']
        primary_keys = example_indicator.dataset_metadata['primary_keys']
        result_template = example_indicator.result_template
        
        attributes = [(name,computed_indicators[name].get_computed_dataset_column_name())
                      for name in indicators_to_visualize]
        
        cols = primary_keys + sorted([col_name for name, col_name in attributes])
        table_data = self.input_storage.load_table(
            table_name = dataset_name,
            column_names = cols)
        
        if self.output_style == Table.ALL:
            output_method = self.output_ALL
        elif self.output_style == Table.PER_YEAR:
            output_method = self.output_PER_YEAR
        elif self.output_style == Table.PER_ATTRIBUTE:
            output_method = self.output_PER_ATTRIBUTE
        
        viz_metadata = output_method(
            dataset_name = dataset_name,
            old_data = table_data,
            attributes = attributes,
            primary_keys = primary_keys,
            years = result_template.years) 
        
        visualization_representations = []
        for indicator_names, table_name, years in viz_metadata:
            visualization_representations.append(
                self._get_visualization_metadata(
                    computed_indicators = computed_indicators,
                    indicators_to_visualize = indicator_names,
                    table_name = table_name,
                    years = years
            ))                   
        
        return visualization_representations

    def output_PER_YEAR(self,
                        dataset_name,
                        old_data,
                        attributes,
                        primary_keys,
                        years):
        
        id_cols = [id_col for id_col in primary_keys if id_col != 'year']
        cols = [computed_name for name, computed_name in attributes]
        viz_metadata = []
        for year in years:
            data_subset = {}
            for col in cols + id_cols:
                if col not in id_cols:
                    if col.find('DDDD') == -1:
                        col_name = '%s_%i'%(col, year)
                    else:
                        col_name = col.replace('DDDD', repr(year))
                else: col_name = col

                data_subset[col_name] = old_data[col][where(old_data['year']==year)]

            table_name = self.get_name(
                dataset_name = dataset_name,
                years = [year],
                attribute_names = [name for name, computed_name in attributes])
                    
            self._write_to_storage(
                table_name = table_name,
                table_data = data_subset,
                column_names = id_cols + sorted([col for col in data_subset.keys() 
                                                      if col not in id_cols])
            )
            
            viz_metadata.append(([name for name, computed_name in attributes], 
                                 table_name, 
                                 [year])) 
                       
        return viz_metadata
            
    def output_PER_ATTRIBUTE(self,
                            dataset_name,
                            old_data,
                            attributes,
                            primary_keys,
                            years):
        
        id_cols = [id_col for id_col in primary_keys if id_col != 'year']
        new_data, cols, col_name_attribute_map = self._convert_to_tabular_form_for_ALL(
                                old_data = old_data, 
                                attributes = attributes, 
                                primary_keys = primary_keys, 
                                years = years)                                      
        
        viz_metadata = []
        for name, cols in col_name_attribute_map.items():
            data_subset = dict([(col, new_data[col]) for col in id_cols+cols])
            table_name = self.get_name(
                dataset_name = dataset_name,
                years = years,
                attribute_names = [name])
                    
            self._write_to_storage(
                table_name = table_name,
                table_data = data_subset,
                column_names = id_cols + sorted(cols)
            )
            
            viz_metadata.append(([name], table_name, years))
            
        return viz_metadata
                         
    def output_ALL(self,
                   dataset_name,
                   old_data,
                   attributes,
                   primary_keys,
                   years):

        new_data, cols, col_name_attribute_map = self._convert_to_tabular_form_for_ALL(
            old_data = old_data,
            attributes = attributes,
            primary_keys = primary_keys,
            years = years
        )

        table_name = self.get_name(
            dataset_name = dataset_name,
            years = years,
            attribute_names = col_name_attribute_map.keys())
                
        self._write_to_storage(
            table_name = table_name,
            table_data = new_data,
            column_names = cols
        )
        
        return [(col_name_attribute_map.keys(), table_name, years)]
                                              
    def _convert_to_tabular_form_for_ALL(self,
                                old_data,
                                attributes,
                                primary_keys,
                                years):
        #TODO: make sure that column types are properly handled
        id_cols = [id_col for id_col in primary_keys if id_col != 'year']
        
        keys = set(zip(
                   *[list(old_data[col]) for col in id_cols]))
        
        keys = sorted(list(keys))
        default_array = [-1 for i in range(len(keys))]

        key_to_index_map = dict([(keys[i],i) for i in range(len(keys))])
        
        i = 0
        new_names = {}
        new_data = {}
        col_name_attribute_map = {}
        
        for id_col in id_cols:
            new_data[id_col] = array(default_array)
        
        for name, attribute in attributes:
            col_name_attribute_map[name] = []
            for year in years:
                if attribute.find('DDDD') == -1:
                    new_name = '%s_%i'%(attribute, year)
                else:
                    new_name = attribute.replace('DDDD', repr(year))
                new_names[(i,year)] = new_name
                col_name_attribute_map[name].append(new_name)                
                new_data[new_name] = array(default_array)
            i += 1
        new_names = dict(new_names)

        for i in range(len(old_data[primary_keys[0]])):
            key = tuple([old_data[col][i] for col in id_cols])
            index_in_new = key_to_index_map[key]
            year = old_data['year'][i]
            j = 0
            for name, attribute in attributes:  
                new_name = new_names[(j,year)]
                new_data[new_name][index_in_new] = old_data[attribute][i]
                j += 1          
            for id_col in id_cols:
                new_data[id_col][index_in_new] = old_data[id_col][i]
        
        return new_data, id_cols + sorted(new_names.values()), col_name_attribute_map
        
    def _write_to_storage(self, 
                          table_name,
                          table_data,
                          column_names):
        kwargs = {}
        if self.output_type in ['csv','tab']:
            kwargs['fixed_column_order'] = column_names
            kwargs['append_type_info'] = False
            
        self.output_storage.write_table(
            table_name = table_name, 
            table_data = table_data, 
            **kwargs)    
            
        
from opus_core.tests import opus_unittest
from inprocess.travis.opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
from inprocess.travis.opus_core.indicator_framework.maker.maker import Maker
from inprocess.travis.opus_core.indicator_framework.representations.indicator import Indicator

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
                
        maker = Maker()
        computed_indicators = maker.create_batch(
            indicators = {'attr1':indicator, 
                          'attr2':indicator2}, 
            result_template = self.source_data)
        
        for style in [Table.ALL, Table.PER_YEAR, Table.PER_ATTRIBUTE]:
            table = Table(indicator_directory = self.source_data.get_indicator_directory(),
                          output_type = 'csv',
                          output_style = style)
            viz_results = table.visualize(
                            indicators_to_visualize = ['attr1',
                                                       'attr2'], 
                            computed_indicators = computed_indicators)
            
            for viz_result in viz_results:
                if style == Table.ALL:
                    file_name = 'test|table-%i|1980-1983|attr1-attr2.csv'%style
                elif style == Table.PER_YEAR:
                    file_name = 'test|table-%i|%i|attr1-attr2.csv'%(style,viz_result.years[0])
                elif style == Table.PER_ATTRIBUTE:
                    if viz_result.indicators[0].indicator.name == 'attribute':
                        name = 'attr1'
                    else:
                        name = 'attr2'
                    file_name = 'test|table-%i|1980-1983|%s.csv'%(style, name)
                    
                self.assertEqual(
                     os.path.join(viz_result.storage_location,
                                  viz_result.table_name + '.' + viz_result.file_extension), 
                     os.path.join(indicator_path, file_name))     
        

    def test__convert_to_tabular_form_for_ALL(self):
        table = Table(indicator_directory = self.source_data.get_indicator_directory(),
                      output_type = 'csv')
        
        old_data = {
            'id':array([1,2,3,1,2,4]),
            'id2':array([3,4,5,3,4,5]),
            'year':array([2000,2000,2000,2002,2002,2002]),
            'attr1':array([1,2,3,10,20,30]),
            'attr2':array([2,3,4,20,30,40]),
        }

        expected = {
            'id':array([1,2,3,4]),
            'id2':array([3,4,5,5]),
            'attr1_2000':array([1,2,3,-1]),
            'attr1_2002':array([10,20,-1,30]),
            'attr2_2000':array([2,3,4,-1]),
            'attr2_2002':array([20,30,-1,40]),
        }
               
        output, cols, dummy = table._convert_to_tabular_form_for_ALL(
            old_data = old_data,     
            attributes = [('attr1','attr1'),('attr2','attr2')], 
            primary_keys = ['id','id2', 'year'], 
            years = [2000,2002])
        
        self.assertEqual(len(expected.keys()), len(output.keys()))
        for k,v in expected.items():
            self.assertEqual(list(v), list(output[k]))
            
    def test__output_PER_ATTRIBUTE(self):
        indicator_directory = self.source_data.get_indicator_directory() 
        table = Table(indicator_directory = indicator_directory,
                      output_type = 'csv')
        
        old_data = {
            'id':array([1,2,3,1,2,4]),
            'id2':array([3,4,5,3,4,5]),
            'year':array([2000,2000,2000,2002,2002,2002]),
            'attr1':array([1,2,3,10,20,30]),
            'attr2':array([2,3,4,20,30,40]),
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
                       
        viz_metadata = table.output_PER_ATTRIBUTE(
            dataset_name = 'test',
            old_data = old_data,     
            attributes = [('attr1','attr1'),('attr2','attr2')], 
            primary_keys = ['id','id2', 'year'], 
            years = [2000,2002])

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
        
        old_data = {
            'id':array([1,2,3,1,2,4]),
            'id2':array([3,4,5,3,4,5]),
            'year':array([2000,2000,2000,2002,2002,2002]),
            'attr1':array([1,2,3,10,20,30]),
            'attr2':array([2,3,4,20,30,40]),
        }

        expected1 = {
            'id':array([1,2,3]),
            'id2':array([3,4,5]),
            'attr1_2000':array([1,2,3]),
            'attr2_2000':array([2,3,4]),
        }

        expected2 = {
            'id':array([1,2,4]),
            'id2':array([3,4,5]),
            'attr1_2002':array([10,20,30]),
            'attr2_2002':array([20,30,40]),
        }
                       
        viz_metadata = table.output_PER_YEAR(
            dataset_name = 'test',
            old_data = old_data,     
            attributes = [('attr1','attr1'),('attr2','attr2')], 
            primary_keys = ['id','id2', 'year'], 
            years = [2000,2002])

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
                expected = expected1
            else:
                expected = expected2
                                
            self.assertEqual(len(expected.keys()), len(output.keys()))
            for k,v in expected.items():
                self.assertEqual(list(v), list(output[k]))
                
    def test__output_types(self):        
        output_types = ['csv','tab']
        try:        
            import dbfpy
        except ImportError:
            pass
        else:
            output_types.append('dbf')

        try:
            from opus_core.database_management.database_configuration import DatabaseConfiguration
            from opus_core.database_management.database_server import DatabaseServer

            test_db_name = 'test_db_for_indicator_framework'
            database_config = DatabaseConfiguration(
                 database_name = test_db_name,
                 test = True,
                 use_environment_variables = True 
            )
                        
            server = DatabaseServer(database_config)
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

        maker = Maker()
        computed_indicators = maker.create_batch(
            indicators = {'attr1':indicator}, 
            result_template = self.source_data)

        for output_type in output_types:
            kwargs = {}
            if output_type == 'sql':
                kwargs['storage_location'] = database_config
                
            table = Table(
                        indicator_directory = self.source_data.get_indicator_directory(),
                        output_type = output_type,
                        **kwargs)
            viz_result = table.visualize(
                        indicators_to_visualize = ['attr1'], 
                        computed_indicators = computed_indicators)[0]
            if output_type in ['csv','dbf','tab']:                        
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