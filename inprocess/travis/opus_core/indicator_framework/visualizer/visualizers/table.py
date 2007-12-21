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
from inprocess.travis.opus_core.indicator_framework.representations.visualization import Visualization

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
        kwargs = {}
        if self.output_type == 'sql':
            kwargs['protocol'] = storage_location.protocol
            kwargs['username'] = storage_location.user_name
            kwargs['password'] = storage_location.password
            kwargs['hostname'] = storage_location.host_name
            kwargs['database_name'] = storage_location.database_name
        else:
            kwargs['storage_location'] = indicator_directory
                
        self.output_storage = StorageFactory().get_storage(
            type = '%s_storage'%(self.output_type),
            **kwargs
        )
        
        self.input_storage = StorageFactory().get_storage(
            type = 'csv_storage',
            storage_location = indicator_directory)
        self.indicator_directory = indicator_directory
        self.name = name
                
    def is_single_year_indicator_image_type(self):
        return False
    
    def get_file_extension(self):
        return self.output_type
    
    def get_visualization_shorthand(self):
        if self.output_type == 'csv':
            return 'table'
        elif self.output_type == 'tab':
            return 'tab'
        elif self.output_type == 'dbf':
            return 'dbf'
        elif self.output_type == 'sql':
            return 'sql'
        
    def get_additional_metadata(self):
        return  [('output_type',self.output_type)]
        
    def get_visualization_type(self):
        return 'table'
    
    def get_name(self,
                 indicators_to_visualize,
                 computed_indicators,
                 dataset_name,
                 result_template):
        if self.name is None:
            years = []
            year_agg = []
            for year in sorted(result_template.years):
                if len(year_agg) > 0 and year == year_agg[-1] + 1:
                    year_agg.append(year)
                else:
                    if len(year_agg) > 0:
                        years.append('%i-%i'%(year_agg[0],year_agg[-1]))
                    year_agg = [year]
                        
            if len(year_agg) > 0:
                years.append('%i-%i'%(year_agg[0],year_agg[-1]))
            years = '_'.join(years)
            
#            indicator_names = [i.indicator.get_indicator_name()
#                               for i in [computed_indicators[name]
#                                for name in indicators_to_visualize]]
#            indicator_names = '*'.join(indicator_names)
            name = '|'.join([dataset_name,
                             self.get_visualization_type(),
                             #indicator_names, 
                             years])
        else:
            name = self.name
        
        return name
    
    def visualize(self, 
           indicators_to_visualize,
           computed_indicators):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory."""
        
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        dataset_name = example_indicator.dataset_metadata['dataset_name']
        primary_keys = example_indicator.dataset_metadata['primary_keys']
        result_template = example_indicator.result_template
        
        attributes = [computed_indicators[name].get_computed_dataset_column_name()
                      for name in indicators_to_visualize]
             
        cols = primary_keys + sorted(attributes)
        table = self.input_storage.load_table(
            table_name = dataset_name,
            column_names = cols)
            
        table_name = self.get_name(
            indicators_to_visualize = indicators_to_visualize,
            computed_indicators = computed_indicators,
            dataset_name = dataset_name,
            result_template = result_template)

        
        #convert from id, year, attr representation to id, attr_year
        new_data, cols = self._convert_to_tabular_form(
            old_data = table,
            attributes = attributes,
            primary_keys = primary_keys,
            years = result_template.years
        )

        kwargs = {}
        if self.output_type in ['csv','tab']:
            kwargs['fixed_column_order'] = cols
            kwargs['append_type_info'] = False
                    
        self.output_storage.write_table(
            table_name = table_name, 
            table_data = new_data, 
            **kwargs)
        
        viz_metadata = Visualization(
                 indicators = [computed_indicators[ind] 
                               for ind in indicators_to_visualize],
                 visualization_type = self.get_visualization_type(),
                 result_path = os.path.join(self.indicator_directory,
                                            table_name + '.csv'),
                 name = self.name,
                 years = result_template.years
                )
        
        return [viz_metadata]
    
    def _convert_to_tabular_form(self,
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
        for id_col in id_cols:
            new_data[id_col] = array(default_array)
        
        for attribute in attributes:
            for year in years:
                if attribute.find('DDDD') == -1:
                    new_name = '%s_%i'%(attribute, year)
                else:
                    new_name = attribute.replace('DDDD', repr(year))
                new_names[(i,year)] = new_name                
                new_data[new_name] = array(default_array)
            i += 1
        new_names = dict(new_names)

        for i in range(len(old_data[primary_keys[0]])):
            key = tuple([old_data[col][i] for col in id_cols])
            index_in_new = key_to_index_map[key]
            year = old_data['year'][i]
            j = 0
            for attribute in attributes:  
                new_name = new_names[(j,year)]
                new_data[new_name][index_in_new] = old_data[attribute][i]
                j += 1          
            for id_col in id_cols:
                new_data[id_col][index_in_new] = old_data[id_col][i]
        
        return new_data, id_cols + sorted(new_names.values())
        
        
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
        
        table = Table(indicator_directory = self.source_data.get_indicator_directory(),
                      output_type = 'csv')
        viz_result = table.visualize(
                        indicators_to_visualize = ['attr1',
                                                   'attr2'], 
                        computed_indicators = computed_indicators)[0]
                        
        self.assertEqual(viz_result.result_path, os.path.join(indicator_path, 'test|table|1980-1983.csv'))
        
        
        self.assert_(os.path.exists(viz_result.result_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test|table|1980-1983.csv')))        
        

    def test__convert_to_tabular_form(self):
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
               
        output, cols = table._convert_to_tabular_form(
            old_data = old_data,     
            attributes = ['attr1','attr2'], 
            primary_keys = ['id','id2', 'year'], 
            years = [2000,2002])
        
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

        indicator = Indicator(
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute'
        )        

        maker = Maker()
        computed_indicators = maker.create_batch(
            indicators = {'attr1':indicator}, 
            result_template = self.source_data)

        for output_type in output_types:
            table = Table(
                        indicator_directory = self.source_data.get_indicator_directory(),
                        output_type = output_type)
            viz_result = table.visualize(
                        indicators_to_visualize = ['attr1'], 
                        computed_indicators = computed_indicators)[0]
                                    
            self.assertTrue(os.path.exists(viz_result.result_path))
            
if __name__ == '__main__':
    opus_unittest.main()