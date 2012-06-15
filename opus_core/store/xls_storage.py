# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley
# See opus_core/LICENSE

from numpy import array, dtype

from opus_core.opus_error import OpusError
from opus_core.logger import logger
from opus_core.store.storage import Storage
import os

try:
    import xlwt
    import xlrd
    from xlutils.copy import copy
except:
    # If xlwt is not installed, provide an xls storage class that fails.  This
    # technique is borrowed from the dbf class.
    class xls_storage(Storage):
        def __init__(self, *args, **kwargs):
            raise ImportError('Must install python-excel to use '
                              'xls_storage; See http://www.python-excel.org/')

    class TestXlsStorage(opus_unittest.OpusTestCase):
        def test(self):
            self.assertRaises(ImportError, dbf_storage)

else:
    class xls_storage(Storage):
        """
        A storage object that saves tabular data into an xls spreadsheet

        The storage_location is a path to a .xls file.  Each sheet in the .xls
        file is treated as a separate table with a single header row and any
        number of data rows.  If the file does not exist, it will be created.

        The table_to_sheet kwarg is a mapping from arbitrarily long table names
        to 31-char sheet names.  table names not specified in this mapping that
        exceed 31 chars will be truncated when the table is written.
        """

        def __init__(self, storage_location, *args, **kwargs):
            self.storage_location = storage_location
            if os.path.exists(storage_location):
                self.rwb = xlrd.open_workbook(storage_location)
                self.workbook = copy(self.rwb)
            else:
                self.workbook = xlwt.Workbook()
                self.rwb = None
            self.table_to_sheet = kwargs.get('table_to_sheet', {})

        def get_storage_location(self):
            return storage_location

        def get_table_names(self):
            return []

        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
            if self.rwb == None:
                raise NameError("Table '%s' could not be found." % table_name)

            sheet_name = self.table_to_sheet.get(table_name, table_name)
            sheet = self.rwb.sheet_by_name(sheet_name)
            if sheet == None:
                raise NameError("Table '%s' could not be found." % table_name)
            if column_names != Storage.ALL_COLUMNS:
                raise NotImplementedError("individual column loading not supported yet")
            table_data = {}
            for i in range(0, sheet.ncols):
                col = sheet.col_values(i)
                table_data[col[0]] = array(col[1:])
            return table_data

        def _get_sheet_by_name(self, name):
            # Odd that xlwt doesn't have a method like this
            s = 0
            try:
                while True:
                    sheet = self.workbook.get_sheet(s)
                    if sheet.get_name() == name:
                        return sheet
                    s = s + 1
            except IndexError:
                return None

        def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
            """
            raises a NameError if the table_name is more than 31 chars.  This
            is a limitation of the xls format.
            """
            sheet_name = self.table_to_sheet.get(table_name, table_name)
            if len(sheet_name) > 31:
                # Dumbly truncate table name
                logger.log_warning("xls_storage: Truncating " + sheet_name +
                                   " to 31 chars")
                sheet_name = sheet_name[0:30]

            self._get_column_size_and_names(table_data)

            # TODO: respect mode argument
            sheet = self._get_sheet_by_name(sheet_name)
            if sheet == None:
                sheet = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

            c = 0
            for column,data in table_data.iteritems():
                sheet.write(0, c, column)
                if data[0].dtype.kind == 'f':
                    pass
                elif data[0].dtype.kind == 'i':
                    logger.log_warning("xls_storage: Changing output data " +
                                       table_name + ":" + column +
                                       " from integer to float")
                else:
                    raise NotImplementedError("xls only supports float and int at this time")
                r = 1
                for value in data:
                    sheet.write(r, c, float(value))
                    r = r + 1
                c = c + 1
            self.workbook.save(self.storage_location)
            # Reload the readable workbook.  For some reason, the python-excel
            # guys decided that reading and writing should be handled in
            # different classes.
            self.rwb = xlrd.open_workbook(self.storage_location)

        def get_column_names(self, table_name, lowercase=True):
            raise NotImplementedError()

    from opus_core.tests import opus_unittest
    from opus_core.store.storage import TestStorageInterface
    from tempfile import mkdtemp
    from shutil import rmtree    

    class TestXlsStorage(TestStorageInterface):

        def setUp(self):
            self.temp_dir = mkdtemp(prefix='opus_core_test_xls_storage')
            storage_location = os.path.join(self.temp_dir, "foo.xls")
            self.storage = xls_storage(storage_location)
            self.expected = {
                'bar': array([1.0]),
                'baz': array([2.0]),
                }

        def tearDown(self):
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)

        def test_write_table_and_load_table(self):
            self.storage.write_table(
                table_name = 'foo',
                table_data = self.expected
                )
            actual = self.storage.load_table(table_name='foo')
            self.assertDictsEqual(self.expected, actual)

        def test_sheet_name_truncation(self):
            self.storage.write_table(
                table_name = 'thistablenameislongerthanthirtyonechars',
                table_data = self.expected
                )
            actual = self.storage.load_table(table_name='thistablenameislongerthanthirt')
            self.assertDictsEqual(self.expected, actual)

    class TestXlsStorageWithTableMapping(TestStorageInterface):

        def setUp(self):
            self.temp_dir = mkdtemp(prefix='opus_core_test_xls_storage')
            storage_location = os.path.join(self.temp_dir, "fib.xls")
            self.storage = xls_storage(storage_location,
                table_to_sheet = {
                    'thisisasheetwithfibonaccinumbers':'fibnac',
                })
            self.expected = {
                'fib': array([1.0, 1.0, 2.0, 3.0, 5.0]),
                'fib2': array([8.0, 13.0, 21.0, 34.0, 55.0]),
                }

        def tearDown(self):
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)

        def test_sheet_mapping(self):
            self.storage.write_table(
                table_name = 'thisisasheetwithfibonaccinumbers',
                table_data = self.expected
                )
            actual = self.storage.load_table(table_name='thisisasheetwithfibonaccinumbers')
            self.assertDictsEqual(self.expected, actual)

if __name__ == '__main__':
    opus_unittest.main()
