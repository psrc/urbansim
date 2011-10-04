# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, logical_and, logical_not, concatenate, newaxis, rank


from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator
from opus_core.variables.variable_name import VariableName
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.opus_database import OpusDatabase

class DatasetTable(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attributes,
                 name, years = None, operation = None,
                 exclude_condition = None, output_type = 'tab',
                 storage_location = None):

        if output_type == 'sql' and not isinstance(storage_location, OpusDatabase):
            raise "If DatasetTable output_type is 'sql', a OpusDatabase object must be passed as storage_location."
        elif output_type in ['dbf', 'csv', 'tab', 'esri'] and \
               storage_location is not None and \
               not isinstance(storage_location,str):
            raise "If DatasetTable output_type is %s, storage_location must be a path to the output directory"%output_type
        elif output_type not in ['dbf', 'csv', 'tab', 'sql', 'esri']:
            raise "DatasetTable output_type needs to be either dbf, csv, tab, or sql"

        self.output_type = output_type
        self.exclude_condition = exclude_condition
        self.name = name

        AbstractIndicator.__init__(self, source_data, dataset_name,
                                   attributes, years, operation, name,
                                   storage_location=storage_location, 
                                   can_write_to_db = True)
                
        self.output_type = output_type
        kwargs = {}
        if self.output_type == 'esri':
            kwargs['storage_location'] = storage_location
        else:
            kwargs['storage_location'] = self.get_storage_location()

        self.store = StorageFactory().get_storage(
            type = '%s_storage'%(self.output_type),
            **kwargs
        )

    def is_single_year_indicator_image_type(self):
        return True

    def get_file_extension(self):
        return self.output_type

    def get_visualization_shorthand(self):
        return 'dataset_table'

    def get_additional_metadata(self):
        return  [('output_type',self.output_type),
                 ('exclude_condition',self.exclude_condition)]

    def _create_indicator(self, year):
        '''Creates a table with a column for each attribute specified in the arguments

           The id attributes are also included as columns. The outputted file
           contains data for only one year and one dataset.
        '''

        dataset = self._get_dataset(year)

        id_attributes = dataset.get_id_attribute()
        id_cols = dataset.get_id_name()
        id_columns = [i for i in range(len(id_cols))]

        col_titles = id_cols + [VariableName(attribute_name).get_alias()
                        for attribute_name in self.attributes]

        cols = self._get_indicator(year)
        if id_attributes.size == 1 and rank(cols) == 1:
            cols = concatenate((id_attributes, cols))[:, newaxis]
        else:
            cols = concatenate((id_attributes[newaxis,:], cols))

        if self.exclude_condition is not None:
            exclude_mask = self._get_indicator(year,
                                               attributes = [self.exclude_condition],
                                               wrap = False)

            cols = self._conditionally_eliminate_rows(
                cols,
                id_columns,
                exclude_mask)

        attribute_vals = {}
        for i in range(len(col_titles)):
            attribute_vals[col_titles[i]] = cols[i]

        kwargs = {}
        if self.output_type in ['csv','tab']:
            kwargs['fixed_column_order'] = col_titles
            kwargs['append_type_info'] = False

        table_name = self.get_file_name(year = year,
                                        suppress_extension_addition=True)
        self.store.write_table(table_name = table_name,
                               table_data = attribute_vals,
                               **kwargs)

        return self.get_file_path(year = year)

    def _conditionally_eliminate_rows(self, data, id_columns, exclude_mask):
        '''eliminates all the rows where all the data values match the exclude_condition

           data -- an array of arrays
           id_columns -- the columns which should be ignored when deciding to eliminate a row
           exclude_mask -- the mask to be applied to the cols
        '''

        mask = logical_not(exclude_mask)
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

    def test_conditionally_eliminate_rows_through_create_indicator(self):

        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        table = DatasetTable(
                  source_data = self.source_data,
                  name = '',
                  dataset_name = 'test',
                  attributes = ['opus_core.test.attribute',
                                'opus_core.test.attribute2'],
                  output_type = 'tab',
                  exclude_condition = 'opus_core.test.attribute<7'
        )

        table.create(False)

        fpath = os.path.join(indicator_path, 'test__dataset_table____1980.tab')
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(fpath))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__dataset_table____1980.meta')))


        expected_r1 = [3,7,70]
        expected_r2 = [4,8,80]

        f = open(fpath)
        f.readline() #don't care about header
        output_r1 = [int(c) for c in f.readline().split('\t')]
        output_r2 = [int(c) for c in f.readline().split('\t')]
        self.assertEqual(expected_r1,output_r1)
        self.assertEqual(expected_r2,output_r2)

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
        exclude_mask = array([0,0,0,0])
        actual_output = dataset_table._conditionally_eliminate_rows(
            data,
            id_columns=[0,3],
            exclude_mask = exclude_mask)

        self.assert_(ma.allequal(actual_output,data))

        exclude_mask = array([0,0,1,0])
        actual_output = dataset_table._conditionally_eliminate_rows(
            data,
            id_columns=[0,3],
            exclude_mask = exclude_mask)

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
