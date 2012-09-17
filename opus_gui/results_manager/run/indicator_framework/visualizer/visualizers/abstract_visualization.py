# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_gui.results_manager.run.indicator_framework.representations.visualization import Visualization as VisualizationRepresentation
from numpy import array, where
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger

class Visualization(object):

    def get_name(self,
                 dataset_name,
                 years,
                 attribute_names = None):
        
        if self.name is None:
            
            years = self._get_year_string(years = years)
            
            components = [dataset_name,
                          self.get_visualization_type(),
                          years]
            if attribute_names is not None:
                names = '-'.join(sorted(attribute_names))
                components.append(names)
            name = '_'.join(components)
        else:
            name = self.name
            
        return name
    
    def _get_visualization_metadata(self, computed_indicators,
                           indicators_to_visualize,
                           table_name,
                           years):
        try:
            additional_metadata = self.get_additional_metadata()
            viz = VisualizationRepresentation(
                     indicators = [computed_indicators[ind] 
                                   for ind in indicators_to_visualize],
                     visualization_type = self.get_visualization_type(),
                     name = self.name,
                     years = years,
                     table_name = table_name,
                     storage_location = self.storage_location,
                     file_extension = self.get_file_extension(),
                     **additional_metadata
                    )
        except:
            raise
        
        return viz
        
    def _get_year_string(self, years):
        year_agg = []
        years_string = []
        for year in sorted(years):
            if len(year_agg) > 0 and year == year_agg[-1] + 1:
                year_agg.append(year)
            else:
                if len(year_agg) == 1:
                    years_string.append(repr(year_agg[0]))
                elif len(year_agg) > 0:
                    years_string.append('%i-%i'%(year_agg[0],year_agg[-1]))
                year_agg = [year]

        if len(year_agg) == 1:
            years_string.append(repr(year_agg[0]))                    
        elif len(year_agg) > 0:
            years_string.append('%i-%i'%(year_agg[0],year_agg[-1]))
    
        return '_'.join(years_string)

    def _get_ALL_form(self,
                      dataset_name,
                      attributes,
                      primary_keys,
                      years):
        

#        try:
#            import pydevd;pydevd.settrace()
#        except:
#            pass
        
        attribute_data = {}
        id_subsets = {}
        old_key_to_index_map = dict([(year,{}) for year in years])
 
        cols = [computed_name.lower() for _, computed_name in attributes]
                        
        for year in years:

            table_data = self.input_stores[year].load_table(
                table_name = dataset_name,
                column_names = primary_keys + cols)
            
            data_subset = {}
            id_subset = {}
            for col in cols:
                col_name = self._get_year_replaced_attribute(attribute = col, 
                                                  year = year)
                data_subset[col_name] = table_data[col]
            for key in primary_keys:                    
                id_subset[key] = table_data[key]
                
            num_rows = len(id_subset[id_subset.keys()[0]])

            for row in range(num_rows):
                key = tuple([id_subset[key][row] for key in primary_keys])
                old_key_to_index_map[year][key] = row
                
            attribute_data[year] = data_subset    
            id_subsets[year] = id_subset
        
        key_set = set([])        
        for id_subset in id_subsets.values():
            new_keys = [id_subset[key] for key in primary_keys]
            key_set.update(zip(*new_keys))

        keys = sorted(list(key_set))
        new_key_to_index_map = dict([(keys[i],i) for i in range(len(keys))])
        default_array = [-1 for i in range(len(keys))]
        
        i = 0
        new_data = {}
        
        for key in primary_keys:
            new_data[key] = array(default_array)

        for col_names in attribute_data.values():
            for col_name in col_names:
                dtype = col_names[col_name].dtype.type
                new_data[col_name] = array(default_array, dtype = dtype)

        for i in range(len(keys)):
            key = keys[i]
            
            index_in_new = new_key_to_index_map[key]
            for year, col_names in attribute_data.items():
                if key in old_key_to_index_map[year]:
                    index_in_old = old_key_to_index_map[year][key]
                    for col_name in col_names:
                        new_data[col_name][index_in_new] = attribute_data[year][col_name][index_in_old]
                              
            for j in range(len(primary_keys)):
                new_data[primary_keys[j]][index_in_new] = key[j]
        
        return new_data

    def _get_PER_ATTRIBUTE_form(self,
                           dataset_name,
                           attributes,
                           primary_keys,
                           years):
        
        new_data = self._get_ALL_form(
                            dataset_name = dataset_name,
                            attributes = attributes, 
                            primary_keys = primary_keys, 
                            years = years)                                      

        col_name_attribute_map = {}
        
        for name, computed_name in attributes:
            col_name_attribute_map[name] = [self._get_year_replaced_attribute(
                                                  attribute = computed_name, 
                                                  year = year)
                                                for year in years]
            
        per_attribute_data = {}
        for name, cols in col_name_attribute_map.items():
            data_subset = dict([(col, new_data[col]) for col in primary_keys+cols])
            per_attribute_data[name] = data_subset
            
        return per_attribute_data
    
    def _get_PER_YEAR_form(self,
                        dataset_name,
                        attributes,
                        primary_keys,
                        years):

        
        per_year_data = {}
        cols = [computed_name for name, computed_name in attributes]
        for year in years:
            
            table_data = self.input_stores[year].load_table(
                table_name = dataset_name,
                column_names = primary_keys + cols)
            
            data_subset = {}
            for col in cols: 
                col_name = self._get_year_replaced_attribute(attribute = col, 
                                                      year = year)
                if col in table_data:
                    data_subset[col_name] = table_data[col]
                else:
                    logger.log_warning('No indicator %s loaded!'%col)
            for key in primary_keys:
                data_subset[key] = table_data[key]

            per_year_data[year] = data_subset
        return per_year_data    

    def _get_year_replaced_attribute(self, attribute, year):
        if attribute.find('DDDD') == -1:
            new_name = '%s_%i'%(attribute, year)
        else:
            new_name = attribute.replace('DDDD', repr(year))

        return new_name
    
    def _create_input_stores(self, years):        
        self.input_stores = {}
        for year in years:
            input_storage = StorageFactory().get_storage(
                type = 'flt_storage',
                storage_location = os.path.join(
                                    self.indicator_directory,
                                    '_stored_data',
                                    repr(year)))
            self.input_stores[year] = input_storage


    def visualize(self):
        '''Visualizes the given indicators and returns a dictionary
           with the visualized indicators. 
        '''
        message = ('visualization.visualize needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_file_extension(self):
        '''Returns the file extension of the outputted indicator 
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('visualization.get_file_extension needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_visualization_shorthand(self):
        '''Returns the shorthand for this output type
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('visualization.get_visualization_shorthand needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)
            
    def get_additional_metadata(self):
        '''returns additional attributes
        
           Child method should override this method if there are any 
           additional attributes that it has. Return a dictionary of
           (attr_name,value) pairs.
        '''
        return {}

from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest


class Tests(AbstractIndicatorTest):
    def test__get_ALL_form(self):
        from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.table import Table
        
        table = Table(indicator_directory = self.source_data.get_indicator_directory(),
                      output_type = 'csv')
        
        table._create_input_stores([2000,2002])
        old_data_2000 = {
            'id':array([1,2,3]),
            'id2':array([3,4,5]),
            'attr1':array([1,2,3]),
            'attr2':array([2,3,4]),
        }
        old_data_2002 = {
            'id':array([1,2,4]),
            'id2':array([3,4,5]),
            'attr1':array([10,20,30]),
            'attr2':array([20,30,40]),
        }
        for year in [2000, 2002]:
            if year == 2000:
                data = old_data_2000
            else:
                data = old_data_2002
            input_storage = StorageFactory().get_storage(
                type = 'flt_storage',
                storage_location = os.path.join(
                                    self.source_data.get_indicator_directory(),
                                    '_stored_data',
                                    repr(year)))
            input_storage.write_table(
                table_name = 'test',
                table_data = data
            )

        expected = {
            'id':array([1,2,3,4]),
            'id2':array([3,4,5,5]),
            'attr1_2000':array([1,2,3,-1]),
            'attr1_2002':array([10,20,-1,30]),
            'attr2_2000':array([2,3,4,-1]),
            'attr2_2002':array([20,30,-1,40]),
        }
               
        output = table._get_ALL_form(
            dataset_name = 'test',
            attributes = [('attr1','attr1'),('attr2','attr2')], 
            primary_keys = ['id','id2'], 
            years = [2000,2002])
                
        self.assertEqual(len(expected.keys()), len(output.keys()))
        for k,v in expected.items():
            self.assertEqual(list(v), list(output[k]))    
if __name__ == '__main__':
    opus_unittest.main()