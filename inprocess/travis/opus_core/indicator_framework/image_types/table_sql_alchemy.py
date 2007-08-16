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

from numpy import newaxis, concatenate, rank

from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator
from opus_core.storage_factory import StorageFactory
from inprocess.travis.opus_core.store.sql_storage import sql_storage

class TableSQLAlchemy(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attribute, 
                 years = None, operation = None, name = None,
                 protocol = 'mysql',
                 database_name = None,
                 user_name = None,
                 host_name = None,
                 password = None):
        
        self.protocol = protocol
        self.user_name = username
        self.host_name = host_name
        self.database_name = database_name
        
        AbstractIndicator.__init__(self, source_data, dataset_name, attribute, years, operation, name)
        
        self.store = sql_storage(
            protocol = self.protocol, 
            user_name = self.user_name, 
            password = self.password, 
            host_name = self.host_name, 
            database_name = self.database_name
        )
        
    def is_single_year_indicator_image_type(self):
        return False
    
    def get_file_extension(self):
        return None
    
    def get_visualization_shorthand(self):
        return 'table'

    def get_additional_metadata(self):
        return  [('protocol',self.protocol),
                 ('user_name',self.user_name),
                 ('host_name',self.host_name),
                 ('database_name',self.database_name)]
        
    def _create_indicator(self, years):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory.
        """
        results, years_found = self._get_indicator_for_years(self.attribute, 
                                                             years)
        
        dataset = self._get_dataset(years[-1])
        
        attribute_name_short = self.get_attribute_alias()
        
        id_attribute = dataset.get_id_attribute()
        if id_attribute.size == 1 and rank(results) == 1:
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
        
        table_name = self.get_file_name(year, suppress_extension_addition=True)
        self.store.write_table(table_name = table_name,
                               table_data = attribute_vals) 

        return self.get_file_path()


from opus_core.tests import opus_unittest
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    def test_create_indicator(self):
        pass
#        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
#        self.assert_(not os.path.exists(indicator_path))
#        
#        table = Table(
#                  source_data = self.source_data,
#                  dataset_name = 'test', 
#                  attribute = 'opus_core.test.attribute', 
#                  years = None, 
#                  output_type = 'csv'
#        )
#        table.create(False)
#        
#        self.assert_(os.path.exists(indicator_path))
#        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__table__attribute.csv')))
                    
if __name__ == '__main__':
    opus_unittest.main()