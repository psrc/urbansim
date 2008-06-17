#
# UrbanSim software. Copyright (C) 1998-2008 University of Washington
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

import os
import re
import csv
from glob import glob

from numpy import array, dtype

from opus_core.opus_error import OpusError
from opus_core.store.storage import Storage


class fixed_field_storage(Storage):
    """
    A storage object that saves table and value data into a directory, 
    giving each table its own file in the directory. Fields are written
    with fixed width and no delimiters. Format info optionally is
    written in a commented header.
    """

    #
    # Static members
    #
    
    class Location:
        NONE = 0
        HEADER = 1
        FILE = 2


    #
    # Constructors
    #

    def __init__(self, 
                 storage_location, 
                 file_extension,
                 format_location = Location.HEADER,
                 format_file_extension = 'fmt',
                 format_prefix = '# ',
                 data_prefix = '',
                 line_terminator = '\n'
                ):

        if not file_extension:
            raise ValueError('File extension must be a non-empty string.')

        if not ( format_location == self.Location.NONE   or
                 format_location == self.Location.HEADER or
                 format_location == self.Location.FILE ) :
            raise ValueError('format_location must be a fixed_field_storage.Location value.')

        self._output_directory = storage_location
        self._file_extension = file_extension
        self._format_location = format_location
        self._format_file_extension = format_file_extension
        self._format_prefix = format_prefix
        self._data_prefix = data_prefix
        self._line_terminator = line_terminator

    
    #
    # Storage interface implementation
    #

    def get_storage_location(self):
        return self._output_directory


    def write_table(self, 
                    table_name, 
                    table_data, 
                    mode = Storage.OVERWRITE,
                    format = None,
                   ):

        if not format:
            raise ValueError('No format supplied, and no default implemented yet.')
        
        if mode == Storage.APPEND:
            # Should this re-load the file and append at the data level,
            # or can we just append at the text level by writing to the
            # end of the file?
            raise NotImplementedError()

        column_size, column_names = self._get_column_size_and_names(table_data)

        output = open(self._get_file_path_for_table(table_name), 'wb')

        if self._format_location == self.Location.HEADER:
            output.write(self._format_prefix
                         + format
                         + self._line_terminator)
        elif self._format_location == self.Location.FILE:
            format_output = open(self._get_format_file_path_for_table(table_name), 'wb')
            format_output.write(format + self._line_terminator)
            format_output.close()

        for row_index in range(column_size):
            row = {}
            for column_name, column_values in table_data.iteritems():
                row[column_name] = column_values[row_index]
            python_format, target_size = self._convert_format_to_python_format_and_get_target_size(format)
            formatted_row = python_format % row
            if len(formatted_row) != target_size:
                raise ValueError('Input data went over fixed field size.')
            output.write(self._data_prefix
                         + formatted_row
                         + self._line_terminator)

        output.close()


    def load_table(self,
                   table_name,
                   column_names = Storage.ALL_COLUMNS,
                   lowercase = True
                  ):

        raise NotImplementedError()


    def get_column_names(self,
                         table_name,
                         lowercase = True
                        ):

        raise NotImplementedError()


    #
    # Private utility methods
    #

    def _get_file_path_for_table(self, table_name):
        filename_with_extention = '%s.%s' % (table_name, self._file_extension)
        return os.path.join(self._output_directory, filename_with_extention)

    def _get_format_file_path_for_table(self, table_name):
        filename_with_extention = '%s.%s' % (table_name, self._format_file_extension)
        return os.path.join(self._output_directory, filename_with_extention)

    def _convert_format_to_python_format_and_get_target_size(self, format):
        field_spec_re = re.compile("^(?P<name>.*):(?P<format>[-#0 +]*(?P<length>[1-9]+[0-9]*)(?:\.[1-9]+[0-9]*)?[diouxXeEfFgGcrs])$")
        python_format = ""
        target_size = 0
        field_specs = format.split(',')
        for field_spec in field_specs:
            match = field_spec_re.match(field_spec).groupdict()
            if not match:
                raise ValueError('Did not understand field spec "' + field_spec + '".')
            python_format += "%%(%(name)s)%(format)s" % match
            target_size += int(match['length'])
        return python_format, target_size


#
# Unit Tests
#

from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

import os

from shutil import rmtree
from tempfile import mkdtemp


class TestFixedFieldStorage(TestStorageInterface):

    format = "strings:5s,floats:6.2f,integers: 04i"
    table_data = {
                  'integers': array([1,2,-3]),
                  'strings': array(['one', 'two', 'three']),
                  'floats': array([1.11,22.2,3.3333])
                 }


    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_fixed_field_storage')
        self.storage = fixed_field_storage(
                            storage_location=self.temp_dir,
                            file_extension='dat',
                            format_location=fixed_field_storage.Location.FILE)
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    def test_fixed_field(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = self.table_data,
            format = self.format
                 )

        output = open(self.storage._get_file_path_for_table('foo'), 'r')
        self.assertEqual(output.readline(), '  one  1.11 001\n')
        self.assertEqual(output.readline(), '  two 22.20 002\n')
        self.assertEqual(output.readline(), 'three  3.33-003\n')
        output.close()

        output = open(self.storage._get_format_file_path_for_table('foo'), 'r')
        self.assertEqual(output.readline(), self.format + self.storage._line_terminator)
        output.close()


if __name__ == '__main__':
    opus_unittest.main()
