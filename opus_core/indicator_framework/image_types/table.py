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
import os, re, sys, time, traceback
from copy import copy

from numpy import newaxis, concatenate

from opus_core.indicator_framework import AbstractIndicator
from opus_core.storage_factory import StorageFactory

class Table(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attribute, 
                 years = None, operation = None, name = None,
                 #decimal_places = 4,
                 output_type = 'csv'):
        
        if output_type not in ['dbf', 'csv', 'tab']:
            raise "table output type needs to be either dbf, csv, or tab"

        AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, operation, name)
        
        self.output_type = output_type
        #self.decimal_places = decimal_places
        
        self.store = StorageFactory().get_storage(
            type = self.output_type + '_storage',
            storage_location = self.source_data.get_indicator_directory(),
            #digits_to_right_of_decimal = self.decimal_places
        )
        
    def is_single_year_indicator_image_type(self):
        return False
    
    def get_file_extension(self):
        return self.output_type
    
    def get_visualization_shorthand(self):
        if self.output_type == 'csv':
            return 'table'
        elif self.output_type == 'tab':
            return 'tab'
        else:
            return 'dbf'

    def get_additional_metadata(self):
        return  [
                 #('decimal_places',self.decimal_places),
                 ('output_type',self.output_type)]
        
    def _create_indicator(self, years):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory.
        """
        results, years_found = self._get_indicator_for_years(self.attribute, 
                                                             years)
        
        dataset = self._get_dataset(years[-1])
        
        attribute_name_short = self.get_attribute_alias()
        
        id_attribute = dataset.get_id_attribute()
        if id_attribute.size == 1 and results.size == 1:
            results = concatenate((id_attribute, results))[:, newaxis]
        else:
            results = concatenate((id_attribute[newaxis,:], results))
        
        attribute_vals = {}
        cols = []
        id_cols = dataset.get_id_name()
        cur_index = 0
        for id_col in id_cols:    
            attribute_vals[id_col] = results[cur_index,:]
            cols.append(id_col)
            cur_index += 1
                        
        for year in years_found:
            header = '%s_%i'%(attribute_name_short, year)
            attribute_vals[header] = results[cur_index,:]
            cols.append(header)
            cur_index += 1
        
        write_resources = {
           'out_table_name':self.get_file_name(suppress_extension_addition=True),
           'values':attribute_vals,
           'fixed_column_ordering':cols,
           'append_type_info':False
           }
                 
        self.store.write_dataset(write_resources)  

        return self.get_file_path()


from opus_core.tests import opus_unittest
from opus_core.indicator_framework import SourceData
from opus_core.indicator_framework.utilities import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    def test_create_indicator(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        table = Table(
                  source_data = self.source_data,
                  dataset_name = 'test', 
                  attribute = 'package.test.attribute', 
                  years = None, 
                  output_type = 'csv'
        )
        table.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__table__attribute.csv')))
                    
if __name__ == '__main__':
    opus_unittest.main()