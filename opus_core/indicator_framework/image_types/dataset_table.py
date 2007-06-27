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

from numpy import array, logical_and, logical_not

from opus_core.indicator_framework.core import AbstractIndicator
from opus_core.variables.variable_name import VariableName
from opus_core.storage_factory import StorageFactory

class DatasetTable(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attributes, 
                 name, years = None, operation = None, 
                 exclude_condition = None, output_type = 'tab'):
        
        if output_type not in ['dbf', 'csv', 'tab']:
            raise "table output type needs to be either dbf, csv, or tab"
        
        self.attributes = attributes
        self.output_type = output_type
        self.exclude_condition = exclude_condition
        self.name = name
        
        AbstractIndicator.__init__(self, source_data, dataset_name, '', years, operation, name)
        
        self.output_type = output_type
        storage_factory = StorageFactory()
        
        self.store = storage_factory.get_storage(
            type = self.output_type + '_storage',
            storage_location = self.source_data.get_indicator_directory())
        
    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return self.output_type
                
    def get_visualization_shorthand(self):
        return 'dataset_table'

    def get_additional_metadata(self):
        return  [('attributes',self.attributes),
                 ('output_type',self.output_type),
                 ('exclude_condition',self.exclude_condition)]
    
    def get_file_name(self, 
                      year, 
                      extension = None,
                      suppress_extension_addition = False):
        '''returns the file name for the outputted indicator'''
        
        if extension is None:
            extension = self.get_file_extension()
            
        file_name = '%s__dataset_table__%s__%i'%(
            self.dataset_name,
            self.name,
            year)
        
        if not suppress_extension_addition:
            file_name += '.%s'%extension
                
        return file_name
    
    def get_attribute_alias(self, year = None):
        alias = self.name
        if year is not None:
            alias = self.name.replace('DDDD',repr(year))
        return alias
      
    def _create_indicator(self, year):
        '''Creates a table with a column for each attribute specified in the arguments
        
           The id attributes are also included as columns. The outputted file
           contains data for only one year and one dataset.
        '''

        dataset = self._get_dataset(year)
        
        id_attributes = dataset.get_id_name()
        non_id_attributes = []

        for attribute_name in self.attributes:
            if attribute_name not in id_attributes:
                non_id_attributes.append(attribute_name)
   
        attributes = id_attributes + non_id_attributes   
        id_columns = [i for i in range(len(id_attributes))]
    
        cols = []
        col_titles = []
        
        for attribute_name in attributes:
            attribute_vals = self._get_indicator(attribute_name, year)
            cols.append(attribute_vals)
            variable_name = VariableName(attribute_name).get_alias()
            col_titles.append(variable_name)
        
        if self.exclude_condition is not None:
            cols = self._conditionally_eliminate_rows(
                cols,
                id_columns,
                self.exclude_condition)
        
        attribute_vals = {}
        for i in range(len(col_titles)):
            attribute_vals[col_titles[i]] = cols[i]
        
        
        write_resources = {
           'out_table_name':self.get_file_name(year, suppress_extension_addition=True),
           'values':attribute_vals,
           'fixed_column_ordering':col_titles,
           'append_type_info':False
           }
                 
        self.store.write_dataset(write_resources)               
        
#        self.store.write_table(
#            table_name=self.get_file_name(year = year, suppress_extension_addition = True),
#            table_data=attribute_vals,
#            )

        return self.get_file_path(year = year)
    
    def _conditionally_eliminate_rows(self, data, id_columns, exclude_condition):
        '''eliminates all the rows where all the data values match the exclude_condition
           
           data -- an array of arrays 
           id_columns -- the columns which should be ignored when deciding to eliminate a row
           exclude_condition -- the condition which determines whether a value can be eliminated
        '''
        
        if exclude_condition is None:
            return data
        
        data_columns = [c for c in range(len(data)) if c not in id_columns]
        mask = None
        
        for col in data_columns:
            col_data = data[col]
            mask_cmd = 'col_data %s' % exclude_condition
            masked_col = eval(mask_cmd)
            if mask is None:
                mask = masked_col
            else:
                mask = logical_and(mask, masked_col)
                
        mask = logical_not(mask)
        new_data = []
        for col in data:
            new_col = col[mask]
            new_data.append(new_col)
        
        return new_data    

import os
from opus_core.tests import opus_unittest

from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

from numpy import ma

class Tests(AbstractIndicatorTest):
        
    def test_create_indicator(self):
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        table = DatasetTable(
                  source_data = self.source_data,
                  name = '',
                  dataset_name = 'test', 
                  attributes = ['opus_core.test.attribute', 
                                'opus_core.test.attribute2'],
                  output_type = 'tab'
        )
        

        table.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__dataset_table____1980.tab')))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__dataset_table____1980.meta')))

    def test__conditionally_eliminate_rows(self):
        
        dataset_table = DatasetTable(
             source_data = self.source_data, 
             attributes = [], 
             dataset_name = 'test',
             name = 'test')
        
        data = [
          array([1,1,2,2]),#id 1
          array([1,2,0,0]),
          array([1,2,0,0]),
          array([1,2,1,2]),#id 2
          array([0,2,0,4])
          ]

        actual_output = dataset_table._conditionally_eliminate_rows(
            data, 
            id_columns=[0,3],
            exclude_condition=None)        
        self.assert_(ma.allequal(actual_output,data))
        
        actual_output = dataset_table._conditionally_eliminate_rows(
            data, 
            id_columns=[0,3],
            exclude_condition='==0')
        
        desired_output = [
          array([1,1,2]),
          array([1,2,0]),
          array([1,2,0]),
          array([1,2,2]),
          array([0,2,4])
          ]
        
        self.assertEqual(len(actual_output), len(desired_output))
        for col in range(len(actual_output)):
            self.assert_(ma.allclose(actual_output[col], desired_output[col]))
                                
if __name__ == '__main__':
    opus_unittest.main()
