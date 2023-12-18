# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from copy import copy

from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger

from numpy import array, subtract, concatenate

class DatasetJunior(object):
    
    def __init__(self, dataset, name):
        self.dataset = dataset
        self.primary_keys = dataset.get_id_name()
        self.computed = []
        self.column_representation = {}
        self.row_representation = {}
        self.name = name
        
        self.reduced = False

    def compute(self, indicator, year):        
        year_replaced_attribute = indicator.attribute.replace('DDDD',repr(year))
        name = VariableName(year_replaced_attribute)
        
        if name.get_alias() not in self.dataset.get_known_attribute_names():
            self.dataset.compute_variables(name)
        self.computed.append((year_replaced_attribute, year))
            
    ###### Reduce methods #####
    def reduce(self, release_dataset = False):
        '''extracts primary keys and computed attributes from dataset and puts 
           them into a tuple-based representation more natural for a 
           table-like structure'''
        
        id_cols = []
        for col in self.primary_keys:
            datasetName = VariableName(col)
            id_cols.append(self.dataset.get_attribute(datasetName))
        
        attribute_cols = {}
        for (attr, year) in self.computed:
            datasetName = VariableName(attr)
            attribute_cols[attr + '_%i'%year] = self.dataset.get_attribute(datasetName)        
        
        self._build_row_representation(id_cols, attribute_cols)
        
        if release_dataset:
            self.dataset = None     
        
        self.reduced = True
        
    def _build_row_representation(self, id_cols, attribute_cols):
        self.row_representation = {}
        num_rows = len(id_cols[0])
        for row in range(num_rows):
            key = tuple([id_col[row] for id_col in id_cols])#key is the tuple of id cols for the row
            self.row_representation[key] = {}
            
            for name, attribute_col in list(attribute_cols.items()):
                self.row_representation[key][name] = attribute_col[row]
                
    ###### Join methods ######
    def join(self, dataset, join_columns = None, fill_value = -1):
        '''Joins computed columns on the given join_columns; will fill in values
             if one dataset does not have a given primary key'''
        
        if not self.reduced or not dataset.reduced:
            raise Exception('cannot join a non-reduced DatasetJunior object')
            
        if self.primary_keys != dataset.primary_keys:
            raise Exception('cannot join the datasets, the primary key columns do not match')
        
        if join_columns is None: 
            join_columns = self.primary_keys

        #fill in missing data between dataset and this dataset            
        self._merge_row_representations(primary_representation = self.row_representation, 
                                          representation_to_merge = dataset.row_representation, 
                                          fill_value = fill_value)                

    
    def _merge_row_representations(self, primary_representation, representation_to_merge, fill_value):
        '''merges representation_to_merge with primary_representation'''
        old_value_cols = list(primary_representation[list(primary_representation.keys())[0]].keys())
        new_value_cols = list(representation_to_merge[list(representation_to_merge.keys())[0]].keys())
        
        for id_tuple in set(list(primary_representation.keys()) + list(representation_to_merge.keys())):
            if id_tuple not in primary_representation:
                primary_representation[id_tuple] = self._get_new_value_dict(
                                                        cols = old_value_cols + new_value_cols, 
                                                        fill_value = fill_value)
            if id_tuple in representation_to_merge:
                for new_value_col in new_value_cols:
                    primary_representation[id_tuple][new_value_col] = representation_to_merge[id_tuple][new_value_col]
            else:
                for new_value_col in new_value_cols:
                    primary_representation[id_tuple][new_value_col] = fill_value
            
    def _get_new_value_dict(self, cols, fill_value):
        return dict((col, fill_value) for col in cols)
        
    def get_columns(self):
        if self.reduced:
            return self.primary_keys + list(self.row_representation[list(self.row_representation.keys())[0]].keys())
        else:
            return None
        
    #############################################
    def get_column_representation(self):
        if not self.reduced:
            self.reduce(release_dataset = False)
            
        if self.column_representation == {}:
            cols = self.get_columns()
            self.column_representation = dict([(col, []) for col in cols])
            keys = list(self.row_representation.keys())
            keys.sort()
            for key in keys:
                for i in range(len(key)):
                    self.column_representation[self.primary_keys[i]].append(key[i])
                values = self.row_representation[key]
                for value_col,value in list(values.items()):
                    self.column_representation[value_col].append(value)
            
            for k,v in list(self.column_representation.items()):
                self.column_representation[k] = array(v)
            
        return self.column_representation
            
    def replace(self, indicator, replacement_vals):
        year_replaced_attribute = indicator.attribute.replace('DDDD',repr(year))
        name = VariableName(year_replaced_attribute)    
        #TODO: replace col name with replacement_vals
        
    def binary_operation(self, dataset, column, operation):
        pass        
        
from opus_core.tests import opus_unittest
from opus_gui.results_manager.run.indicator_framework.test_classes.test_with_attribute_data import TestWithAttributeData
from opus_gui.results_manager.run.indicator_framework.representations.indicator import Indicator

class DatasetJuniorTests(TestWithAttributeData):      
        
    def test_compute(self):
        dataset, dataset_junior = self._get_dataset_for_year_with_computed_attributes(year = 1980)
        
        datasetName = VariableName('opus_core.test.attribute')
        output = list(dataset_junior.dataset.get_attribute(datasetName))
        expected = [5,6,7,8]
        self.assertEqual(output,expected)
        
            
    def test_join(self):
        dataset1, dataset_junior1 = self._get_dataset_for_year_with_computed_attributes(year = 1980)
        dataset_junior1.reduce()
        
        dataset2, dataset_junior2 = self._get_dataset_for_year_with_computed_attributes(year = 1983)
        dataset_junior2.reduce()
                    
        dataset_junior1.join(dataset_junior2)
        output = dataset_junior1.row_representation

        expected = {
            (1,):{'opus_core.test.attribute_1980':5,
                  'opus_core.test.attribute2_1980':50,
                  'opus_core.test.attribute_1983':10,
                  'opus_core.test.attribute2_1983':100},
            (2,):{'opus_core.test.attribute_1980':6,
                  'opus_core.test.attribute2_1980':60,
                  'opus_core.test.attribute_1983':12,
                  'opus_core.test.attribute2_1983':120},
            (3,):{'opus_core.test.attribute_1980':7,
                  'opus_core.test.attribute2_1980':70,
                  'opus_core.test.attribute_1983':14,
                  'opus_core.test.attribute2_1983':140},  
            (4,):{'opus_core.test.attribute_1980':8,
                  'opus_core.test.attribute2_1980':80,
                  'opus_core.test.attribute_1983':16,
                  'opus_core.test.attribute2_1983':160},          
        }
        
        self.assertEqual(expected,output)
        
        
                
    def test_reduce(self):
        dataset, dataset_junior = self._get_dataset_for_year_with_computed_attributes(year = 1980)
                
        dataset_junior.reduce()   
        output = dataset_junior.row_representation
        
        expected = {
            (1,):{'opus_core.test.attribute_1980':5,
                  'opus_core.test.attribute2_1980':50},
            (2,):{'opus_core.test.attribute_1980':6,
                  'opus_core.test.attribute2_1980':60},
            (3,):{'opus_core.test.attribute_1980':7,
                  'opus_core.test.attribute2_1980':70},  
            (4,):{'opus_core.test.attribute_1980':8,
                  'opus_core.test.attribute2_1980':80},          
        }
        self.assertEqual(output,expected)

    def test_get_column_representation(self):
        dataset, dataset_junior = self._get_dataset_for_year_with_computed_attributes(year = 1980)
                
        dataset_junior.reduce()   
        output = dataset_junior.get_column_representation()
        
        expected = {
            'id':[1,2,3,4],
            'opus_core.test.attribute_1980':array([5,6,7,8]),
            'opus_core.test.attribute2_1980':array([50,60,70,80])          
        }
        self.assertEqual(list(output.keys()), list(expected.keys()))
        for k in list(output.keys()):
            self.assertEqual(list(output[k]),list(expected[k]))
        
    def _get_dataset_for_year_with_computed_attributes(self, year):
        dataset = self._get_dataset(dataset_name = 'test', 
                                    cache_directory = self.temp_cache_path, 
                                    year = year)
        dataset_junior = DatasetJunior(dataset = dataset,
                                       name = 'test')
        indicator = Indicator(
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute'
        )           
        
        dataset_junior.compute(indicator = indicator, year = year)
        indicator = Indicator(
                  dataset_name = 'test', 
                  attribute = 'opus_core.test.attribute2'
        )           
        dataset_junior.compute(indicator = indicator, year = year)
        
        return dataset, dataset_junior  
    
    def test__build_row_representation(self):
        id_cols = [
            array([2,4,6]),
            array([1,2,3])]
        attribute_cols = {
            'col1':array([3,2,1]),
            'col2':array([2,1,0]),
            'col3':array([4,5,6])                  
        }
        
        expected = {
            (2,1):{'col1':3,
                   'col2':2,
                   'col3':4},
            (4,2):{'col1':2,
                   'col2':1,
                   'col3':5},
            (6,3):{'col1':1,
                   'col2':0,
                   'col3':6},            
        }
        
        dataset = self._get_dataset(dataset_name = 'test', 
                                    cache_directory = self.temp_cache_path, 
                                    year = 1980)
        dataset_junior = DatasetJunior(dataset=dataset,
                                       name = 'test')

        
        dataset_junior._build_row_representation(id_cols = id_cols, 
                                                   attribute_cols = attribute_cols) 
        output = dataset_junior.row_representation
          
        self.assertEqual(expected,output)
        
    def test__merge_row_representations(self):
        
        dataset = self._get_dataset(dataset_name = 'test', 
                                    cache_directory = self.temp_cache_path, 
                                    year = 1980)
        
        dataset_junior1 = DatasetJunior(dataset=dataset,
                                        name = 'test')
        dataset_junior2 = DatasetJunior(dataset=dataset,
                                        name = 'test2')

        id_cols1 = [
            array([2,4,6]),
            array([1,2,3]),
        ]
        
        attribute_cols1 = {
            'col1':array([3,2,1]),
            'col2':array([2,1,0]),
        }

        id_cols2 = [
            array([2,4,6]),
            array([1,20,3]),
        ]
        
        attribute_cols2 = {
            'col3':array([4,5,6]),
            'col4':array([40,50,60])              
        }
                
        dataset_junior1._build_row_representation(id_cols = id_cols1, 
                                                   attribute_cols = attribute_cols1) 
        dataset_junior2._build_row_representation(id_cols = id_cols2, 
                                                   attribute_cols = attribute_cols2) 
        
        dataset_junior1._merge_row_representations(
             primary_representation = dataset_junior1.row_representation, 
             representation_to_merge = dataset_junior2.row_representation, 
             fill_value = -1)
        
        output = dataset_junior1.row_representation
        
        expected = {
            (2,1):{'col1':3,
                   'col2':2,
                   'col3':4,
                   'col4':40},
            (4,2):{'col1':2,
                   'col2':1,
                   'col3':-1,
                   'col4':-1},
            (4,20):{'col1':-1,
                   'col2':-1,
                   'col3':5,
                   'col4':50},
            (6,3):{'col1':1,
                   'col2':0,
                   'col3':6,
                   'col4':60}}            
        
        self.assertEqual(expected,output)
            
if __name__ == '__main__':
    opus_unittest.main()
    