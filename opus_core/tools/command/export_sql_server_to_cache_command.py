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
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.sql_server_storage import sql_server_storage
from opus_core.simulation_state import SimulationState
from opus_core.tools.command.command import Command

class ExportSqlServerToCacheCommand(Command):
    """
    This class serves the request complied by the associated GUI.
    """
    def __init__(self, 
                 hostname,
                 username,
                 password,
                 database_name,
                 table_name, 
                 cache_directory, 
                 year):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        self.year = year
        self.table_name = table_name
        self.cache_directory = cache_directory
        
        self._exporter = None # hook for unit tests

    def execute(self):
        in_storage = sql_server_storage(
            hostname=self.hostname, 
            username=self.username, 
            password=self.password, 
            database_name=self.database_name,
            )
        
        out_storage = AttributeCache(cache_directory=self.cache_directory)
        
        old_time = SimulationState().get_current_time()
        SimulationState().set_current_time(self.year)
        
        self._get_exporter().export_dataset(
            dataset_name = self.table_name,
            in_storage = in_storage,
            out_storage = out_storage,
            )
        
        SimulationState().set_current_time(old_time)
    
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
                    self.time_of_export_dataset = SimulationState().get_current_time()
                    
            command = ExportSqlServerToCacheCommand(
                     hostname = r'HOSTNAME\MOCK',
                     username = 'mock_username',
                     password = 'mock_password',
                     database_name = 'mock_database_name',
                     table_name = 'a-table-name',
                     cache_directory = 'a-cache-directory', 
                     year = 1000,
                     )
            command._set_exporter(mock_exporter())
            
            SimulationState().set_current_time(-99)
            command.execute()
            
            self.assertEqual('a-table-name', command._get_exporter().dataset_name)
            self.assert_(isinstance(command._get_exporter().in_storage, sql_server_storage))
            self.assert_(isinstance(command._get_exporter().out_storage, AttributeCache))
            self.assertEqual(r'HOSTNAME\MOCK', 
                             command._get_exporter().in_storage._hostname)
            self.assertEqual('mock_username', 
                             command._get_exporter().in_storage._username)
            self.assertEqual('mock_password', 
                             command._get_exporter().in_storage._password)
            self.assertEqual('mock_database_name', 
                             command._get_exporter().in_storage._database_name)
            self.assertEqual('a-cache-directory', 
                             command._get_exporter().out_storage._get_cache_directory())
            self.assertEqual(1000,
                             command._get_exporter().time_of_export_dataset)
            self.assertEqual(-99, 
                             SimulationState().get_current_time())
        
    
if __name__ == '__main__':
    opus_unittest.main()