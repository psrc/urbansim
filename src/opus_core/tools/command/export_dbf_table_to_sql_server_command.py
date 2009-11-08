#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.export_storage import ExportStorage
from opus_core.store.dbf_storage import dbf_storage
from opus_core.store.sql_server_storage import sql_server_storage

class ExportDbfTableToSqlServerCommand(object):
    """
    This class serves the request complied by the associated GUI.
    """
    def __init__(self, 
                 dbf_directory,
                 table_name,
                 hostname, 
                 username,
                 password,
                 database_name, 
                 ):
        self.table_name = table_name
        self.dbf_directory = dbf_directory
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        
        self._exporter = None # hook for unit tests

    def execute(self):
        in_storage = dbf_storage(storage_location=self.dbf_directory)
        
        out_storage = sql_server_storage(
            hostname = self.hostname, 
            username = self.username, 
            password = self.password, 
            database_name = self.database_name,
            )

        self._get_exporter().export_dataset(
            dataset_name = self.table_name,
            in_storage = in_storage,
            out_storage = out_storage,
            )
    
    def _set_exporter(self, exporter):
        """hook for unit tests"""
        self._exporter = exporter
        
    def _get_exporter(self):
        """hook for unit tests"""
        if self._exporter is None:
            # Create default exporter object.
            self._exporter = ExportStorage()
        return self._exporter
    
    
from opus_core.tests import opus_unittest

try:
    dbf_storage(storage_location='')
    sql_server_storage(hostname='', username='', password='', database_name='')
except:
    pass
else:
    class UnitTests(opus_unittest.OpusTestCase):
        def test_execute(self):
            class mock_exporter(object):
                def __init__(self):
                    self.dataset_name = None
                    
                def export_dataset(self, dataset_name, in_storage, out_storage):
                    self.dataset_name = dataset_name
                    self.in_storage = in_storage
                    self.out_storage = out_storage
                    
            command = ExportDbfTableToSqlServerCommand(
                     dbf_directory = 'mock_dbf_directory',
                     table_name = 'mock_table_name',
                     hostname = r'HOSTNAME\MOCK',
                     username = 'mock_username',
                     password = 'mock_password',
                     database_name = 'mock_database_name',
                     )
            
            command._set_exporter(mock_exporter())
            
            command.execute()
            
            exporter = command._get_exporter()
            
            self.assertEqual('mock_table_name', exporter.dataset_name)
            
            self.assert_(isinstance(exporter.in_storage, dbf_storage))
            
            self.assertEqual('mock_dbf_directory', exporter.in_storage._get_base_directory())
            
            self.assert_(isinstance(exporter.out_storage, sql_server_storage))
                    
            self.assertEqual(r'HOSTNAME\MOCK', exporter.out_storage._hostname)
            self.assertEqual('mock_username', exporter.out_storage._username)
            self.assertEqual('mock_password', exporter.out_storage._password)
            self.assertEqual('mock_database_name', exporter.out_storage._database_name)
            
            command = ExportDbfTableToSqlServerCommand(
                     dbf_directory = 'some_other_mock_dbf_directory',
                     table_name = 'some_other_mock_table_name',
                     hostname = r'SOME_OTHER_HOSTNAME\MOCK',
                     username = 'some_other_mock_username',
                     password = 'some_other_mock_password',
                     database_name = 'some_other_mock_database_name',
                     )
            
            command._set_exporter(mock_exporter())
            
            command.execute()
            
            exporter = command._get_exporter()
            
            self.assertEqual('some_other_mock_table_name', exporter.dataset_name)
            
            self.assert_(isinstance(exporter.in_storage, dbf_storage))
            
            self.assertEqual('some_other_mock_dbf_directory', exporter.in_storage._get_base_directory())
            
            self.assert_(isinstance(exporter.out_storage, sql_server_storage))
                    
            self.assertEqual(r'SOME_OTHER_HOSTNAME\MOCK', exporter.out_storage._hostname)
            self.assertEqual('some_other_mock_username', exporter.out_storage._username)
            self.assertEqual('some_other_mock_password', exporter.out_storage._password)
            self.assertEqual('some_other_mock_database_name', exporter.out_storage._database_name)
        
    
if __name__ == '__main__':
    opus_unittest.main()