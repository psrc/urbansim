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

from opus_core.storage_factory import StorageFactory

from opus_core.indicator_framework.abstract_indicator import AbstractIndicator

class DbfExport(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attribute, 
                 years = None, expression = None, name = None,
                 decimal_places = 4):
        AbstractIndicator.__init__(self, 
                                   source_data, 
                                   dataset_name, 
                                   attribute, 
                                   years, 
                                   expression, 
                                   name,
                                   suppress_file_extension_addition = True)
        self.decimal_places = decimal_places
        
    def is_single_year_indicator_image_type(self):
        return True
    
    def get_file_extension(self):
        return 'dbf'
                
    def get_shorthand(self):
        return 'dbf_export'
    
    def _get_additional_metadata(self):
        return  [('decimal_places',self.decimal_places)]
    
    def _create_indicator(self, year):
        values = self._get_indicator(self.attribute, year)
        
        computed_attribute_name = self.get_last_computed_attribute()
         
        attribute_vals = {
           computed_attribute_name:values       
           }
        
        storage_factory = StorageFactory()
        dbf_storage = storage_factory.get_storage(
            type = 'dbf_storage',
            storage_location = self.source_data.get_indicator_directory(),
            digits_to_right_of_decimal = self.decimal_places)
        dbf_storage.write_table(
            table_name=self.get_file_name(year, suppress_extension_addition=True),
            table_data=attribute_vals,
            )
        
        file_path = self.get_file_path(year = year)
        return file_path

import os
from opus_core.tests import opus_unittest

from opus_core.indicator_framework.abstract_indicator import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    def test_create_indicator(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        dbf_export = DbfExport(
              source_data = self.source_data,
              dataset_name = 'test', 
              attribute = 'package.test.attribute', 
              years = None,
              decimal_places = 2,
        )
        dbf_export.create(False)
        
        self.assert_(os.path.exists(indicator_path))
        
        # Don't fail if dbfpy Python package is not installed.
        try:
            import dbfpy
        except:
            pass
        
        else:
            self.assert_(os.path.exists(os.path.join(indicator_path, 'test__dbf_export__attribute__1980.dbf')))
                    
if __name__ == '__main__':
    opus_unittest.main()