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
    # Constructor
    #

    def __init__(self, 
                 storage_location, 
                 file_extension,
                 write_format_to_header = true,
                 header_prefix = '#',
                 data_prefix = ''
                 line_terminator = '\r\n',
                 ):

        if not file_extension:
            raise ValueError('File extension must be a non-empty string.')

        self._output_directory = storage_location
        self._file_extension = file_extension
        self._write_format_to_header = write_format_to_header
        self._header_prefix = header_prefix
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
#                    filename = None,
                   ):

        if not format:
            raise ValueError('No format supplied, and no default implemented yet.')
        
#        if not filename:
#            filename = table_name
#        file_path = _get_file_path_for_file(filename)
        
        if mode == Storage.APPEND:
            # Should this re-load the file and append at the data level,
            # or can we just append at the text level by writing to the
            # end of the file?
            raise NotImplementedError()

        column_size, column_names = self._get_column_size_and_names(table_data)

        output = open(file_path, 'wb')

        if self._write_format_to_header:
            output.write(self._header_prefix + ' format: ' + format + self._line_terminator)

        for row_index in range(column_size):
            row = {}
            for column_name, column_values in table_data.iteritems():
                row[column_name] = column_values[row_index]
            output.write(self._data_prefix + (format % row) + self._line_terminator)

        output.close()


    def load_table(self,
                   table_name,
                   column_names = ALL_COLUMNS,
                   lowercase = True
                  ):

        raise NotImplementedError()


    def get_column_names(self,
                         table_name,
                         lowercase = True
                        ):

        raise NotImplementedError()


    #
    # Private methods
    #

    def _get_file_path_for_file(self, filename):
        filename_with_extention = '%s.%s' % (filename, self._file_extension)
        return os.path.join(self._output_directory, filename_with_extention)
