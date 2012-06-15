# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley
# See opus_core/LICENSE

from numpy import array, dtype

from opus_core.opus_error import OpusError
from opus_core.logger import logger
from opus_core.store.storage import Storage

try:
    import xlwt

except:
    # If xlwt is not installed, provide an xls storage class that fails.  This
    # technique is borrowed from the dbf class.
    class xls_storage(Storage):
        def __init__(self, *args, **kwargs):
            raise ImportError('Must install Python module xlwt to use '
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
        """

        def __init__(self, storage_location, *args, **kwargs):
            self.storage_location = storage_location

        def get_storage_location(self):
            return storage_location

        def get_table_names(self):
            return []

        def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
            raise NotImplementedError()

        def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
            """
            raises a NameError if the table_name is more than 31 chars.  This
            is a limitation of the xls format.
            """
            raise NotImplementedError()

        def get_column_names(self, table_name, lowercase=True):
            raise NotImplementedError()

    from opus_core.tests import opus_unittest
    from opus_core.store.storage import TestStorageInterface
    from tempfile import mkdtemp
    from shutil import rmtree    
    import os

    class TestXlsStorage(TestStorageInterface):

        def setUp(self):
            self.temp_dir = mkdtemp(prefix='opus_core_test_xls_storage')
            storage_location = os.path.join(self.temp_dir, "foo.xls")
            self.storage = xls_storage(storage_location)

        def tearDown(self):
            if os.path.exists(self.temp_dir):
                rmtree(self.temp_dir)

if __name__ == '__main__':
    opus_unittest.main()
