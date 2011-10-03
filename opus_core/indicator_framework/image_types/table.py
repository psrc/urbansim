# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
import os, re, sys, time, traceback
from copy import copy

from numpy import newaxis, concatenate, rank, transpose

from opus_core.indicator_framework.core.abstract_indicator import AbstractIndicator
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

class Table(AbstractIndicator):

    def __init__(self, source_data, dataset_name, attribute,
                 years = None, operation = None, name = None,
                 output_type = 'csv',
                 storage_location = None):

        if output_type == 'sql' and not isinstance(storage_location, DatabaseConfiguration):
            raise "If Table output_type is 'sql', a Database object must be passed as storage_location."
        elif output_type in ['dbf', 'csv', 'tab', 'esri'] and \
               storage_location is not None and \
               not isinstance(storage_location,str):
            raise "If Table output_type is %s, storage_location must be a path to the output directory"%output_type
        elif output_type not in ['dbf', 'csv', 'tab', 'sql', 'esri']:
            raise "Table output_type must be either dbf, csv, tab, sql, or esri"

        AbstractIndicator.__init__(self, source_data, dataset_name, [attribute],
                                   years=years, operation=operation, name=name,
                                   storage_location=storage_location, can_write_to_db = True)

        self.output_type = output_type
        kwargs = {}
        #if self.output_type == 'sql':
        #    kwargs['protocol'] = storage_location.protocol
        #    kwargs['username'] = storage_location.user_name
        #    kwargs['password'] = storage_location.password
        #    kwargs['hostname'] = storage_location.host_name
        #    kwargs['database_name'] = storage_location.database_name
        #elif self.output_type == 'esri':
        if self.output_type == 'esri':
            kwargs['storage_location'] = storage_location
        else:
            kwargs['storage_location'] = self.get_storage_location()

        self.store = StorageFactory().get_storage(
            type = '%s_storage'%(self.output_type),
            **kwargs
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
        elif self.output_type == 'dbf':
            return 'dbf'
        elif self.output_type == 'sql':
            return 'sql'

    def get_additional_metadata(self):
        return  [('output_type',self.output_type)]

    def _create_indicator(self, years):
        """Create a table for the given indicator, save it to the cache
        directory's 'indicators' sub-directory.
        """
        results, years_found = self._get_indicator_for_years(years,
                                                             wrap = False)

        dataset = self._get_dataset(years[-1])

        attribute_name_short = self.get_attribute_alias(self.attributes[0])

        id_attribute = dataset.get_id_attribute()
        if id_attribute.size == 1 and rank(results) == 1:
            results = concatenate((id_attribute, results))[:, newaxis]
        else:
            if rank(id_attribute) == 1:
                results = concatenate((id_attribute[newaxis,:], results))
            else:
                results = concatenate((transpose(id_attribute), results))

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

        kwargs = {}
        if self.output_type in ['csv','tab']:
            kwargs['fixed_column_order'] = cols
            kwargs['append_type_info'] = False

        table_name = self.get_file_name(suppress_extension_addition=True)
        self.store.write_table(table_name = table_name,
                               table_data = attribute_vals,
                               **kwargs)

        return self.get_file_path()

from opus_core.tests import opus_unittest
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest

class Tests(AbstractIndicatorTest):
    def test_create_indicator(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        table = Table(
                  source_data = self.source_data,
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute',
                  years = None,
                  output_type = 'csv'
        )
        table.create(False)

        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(os.path.join(indicator_path, 'test__table__attribute.csv')))

    def test_create_indicator_multiple_years(self):
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))

        table = Table(
                  source_data = self.source_data,
                  dataset_name = 'test',
                  attribute = 'opus_core.test.attribute',
                  years = range(1980,1984),
                  output_type = 'csv'
        )
        table.create(False)

        file_path = os.path.join(indicator_path, 'test__table__attribute.csv')
        self.assert_(os.path.exists(indicator_path))
        self.assert_(os.path.exists(file_path))

        f = open(file_path)
        cols = [col.strip() for col in f.readline().split(',')]
        data = []
        i = 0
        for line in f:
            line = line.strip()
            if line == '': continue
            row = [int(r.strip()) for r in line.split(',')]
            #rows should all be tuples with all cols defined
            self.assertEqual(len(cols), len(row))
            #rows should be ordered by primary id
            self.assertEqual(row[0],self.id_vals[i])
            for col_index in range(1,len(cols)):
                #each attribute value should be correct
                if cols[col_index] == 'attribute_1983':
                    self.assertEqual(row[col_index],self.attribute_vals_diff[i])
                else:
                    self.assertEqual(row[col_index],self.attribute_vals[i])
            i += 1
            data.append(row)
        self.assertEqual(len(data),4)

if __name__ == '__main__':
    opus_unittest.main()