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
import xml.etree.cElementTree as ET

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
    
    _root_element = 'fixed_field'
    _field_element = 'field'

    class Location:
        NONE = 0
        HEADER = 1
        FILE = 2

    _format_re = re.compile("^[-#0 +]*(?P<size>[1-9]+[0-9]*)(?:\.[0-9]*)?(?P<type>[diouxXeEfFgGcrs])$")


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
        format_et = self._parse_format_to_et(format)
        python_format, target_size = self._convert_et_format_to_python_format_and_get_target_size(format_et)

        # Normalize format XML string
        format = ET.tostring(format_et).replace('\n','').replace('\r','')

        output = open(self._get_file_path_for_table(table_name), 'wb')

        if self._format_location == self.Location.HEADER:
            output.write(self._format_prefix
                         + format.replace(self._line_terminator,'')
                         + self._line_terminator)
        elif self._format_location == self.Location.FILE:
            format_output = open(self._get_format_file_path_for_table(table_name), 'wb')
            format_output.write(format)
            format_output.close()

        for row_index in range(column_size):
            row = {}
            for column_name, column_values in table_data.iteritems():
                row[column_name] = column_values[row_index]
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
                   lowercase = True,
                   format = None,
                   strip = True
                  ):

        data_file = open(self._get_file_path_for_table(table_name))
        
        # Look for a format spec
        if not format:
            try:
                format_file = open(self._get_format_file_path_for_table(table_name))
                format = format_file.read()
                format_file.close()
            except IOError:
                data_file.read(len(self._format_prefix))
                format = data_file.readline().strip()
        
        # Parse out the field formats
        format_et = self._parse_format_to_et(format)

        # Initialize intermediate storage for table data
        table_data_lists = {}
        for field_et in format_et:
            if column_names == Storage.ALL_COLUMNS or field_et.get('name') in column_names:
                table_data_lists[field_et.get('name')] = []
        
        # Parse the data file
        for line in data_file:
            location = len(self._data_prefix)
            for field_et in format_et:
                next_location = location + self._get_field_size(field_et)
                field_text = line[location:next_location]
                location = next_location
                if column_names == Storage.ALL_COLUMNS or field_et.get('name') in column_names:
                    type_char = self._format_re.match(field_et.get('format')).group('type')
                    if   type_char in ['d','i','u']:
                        table_data_lists[field_et.get('name')].append(int(field_text))
                    elif type_char == 'o':
                        table_data_lists[field_et.get('name')].append(int(field_text), 8)
                    elif type_char in ['x','X']:
                        table_data_lists[field_et.get('name')].append(int(field_text), 16)
                    elif type_char in ['e','E','f','F','g','G']:
                        table_data_lists[field_et.get('name')].append(float(field_text))
                    else:
                        if strip:
                            field_text = field_text.strip()
                        table_data_lists[field_et.get('name')].append(field_text)
        
        # Load data into arrays
        table_data = {}
        for name, data in table_data_lists.iteritems():
            table_data[name] = array(data)
        
        return table_data


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

    def _parse_format_to_et(self, format_xml):
        result = ET.Element(self._root_element)
        format_et = ET.fromstring(format_xml)
        if format_et.tag != self._root_element:
            raise ValueError('Format root element is not "'+self._root_element+'".')
        for field_et in format_et:
            if field_et.tag == self._field_element:
                ET.SubElement(result, self._field_element, name=field_et.get('name'), format=field_et.get('format'))
        return result

    def _get_field_size(self, field_et):
        return int(self._format_re.match(field_et.get('format')).group('size'))

    def _convert_et_format_to_python_format_and_get_target_size(self, format_et):
        python_format = ""
        target_size = 0
        for field_et in format_et:
            python_format += "%%(%(name)s)%(format)s" % field_et.attrib
            target_size += self._get_field_size(field_et)
        return python_format, target_size



################################################################################
# Unit Tests
#

from opus_core.tests import opus_unittest
from opus_core.store.storage import TestStorageInterface

import os
import xml.etree.cElementTree as ET

from shutil import rmtree
from tempfile import mkdtemp


class TestFixedFieldStorageBase(object):

    format = '''
        <fixed_field>
            <field name="strs" format="5s" />
            <field name="flts" format="6.2f" />
            <field name="ints" format=" 04i"/>
        </fixed_field>
        '''
    data_in = {
        'ints': array([1,2,-3]),
        'strs': array(['one', 'two', 'three']),
        'flts': array([1.11,22.2,3.3333]),
        'misc': array([10,20,30])
        }
    data_out = {
        'ints': array([1,2,-3]),
        'strs': array(['one', 'two', 'three']),
        'flts': array([1.11,22.2,3.33])
        }
    data_text = '  one  1.11 001\n  two 22.20 002\nthree  3.33-003\n'

    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_fixed_field_storage')

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    def fixed_field_read(self):
        actual = self.storage.load_table(table_name = 'foo')
        self.assertDictsEqual(actual, self.data_out)


class TestFixedFieldStorageWithFormatFile(TestStorageInterface,TestFixedFieldStorageBase):

    def setUp(self):
        TestFixedFieldStorageBase.setUp(self)
        self.storage = fixed_field_storage(
                            storage_location=self.temp_dir,
                            file_extension='dat',
                            format_location=fixed_field_storage.Location.FILE)

    def tearDown(self):
        TestFixedFieldStorageBase.tearDown(self)

    def test_fixed_field_write(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = self.data_in,
            format = self.format)
        file = open(self.temp_dir+'/foo.dat', 'r')
        self.assertEqual(file.read(), self.data_text)
        file.close()
        # Do I need to test XML equality...? Or is that covered by testing if the file can be read back in?
        file = open(self.temp_dir+'/foo.fmt', 'r')
        file.close()
        
    def test_fixed_field_read(self):
        format_file = open(self.temp_dir+'/foo.fmt', 'wb')
        format_file.write(self.format)
        format_file.close()
        data_file = open(self.temp_dir+'/foo.dat', 'wb')
        data_file.write(self.data_text)
        data_file.close()
        self.fixed_field_read()


class TestFixedFieldStorageWithFormatHeader(TestStorageInterface,TestFixedFieldStorageBase):

    def setUp(self):
        TestFixedFieldStorageBase.setUp(self)
        self.storage = fixed_field_storage(
                            storage_location=self.temp_dir,
                            file_extension='dat',
                            format_location=fixed_field_storage.Location.HEADER)

    def tearDown(self):
        TestFixedFieldStorageBase.tearDown(self)

    def test_fixed_field_write(self):
        self.storage.write_table(
            table_name = 'foo',
            table_data = self.data_out,
            format = self.format)
        file = open(self.temp_dir+'/foo.dat', 'r')
        self.assertEqual(file.read(2), '# ')
        file.readline()
        self.assertEqual(file.read(), self.data_text)
        file.close()

    def test_fixed_field_read(self):
        data_file = open(self.temp_dir+'/foo.dat', 'wb')
        data_file.write('# ' + self.format.replace('\n','') + '\n')
        data_file.write(self.data_text)
        data_file.close()
        self.fixed_field_read()


if __name__ == '__main__':
    opus_unittest.main()
