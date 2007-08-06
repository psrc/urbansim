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
from opus_core.tools.command.command import Command
from opus_core.store.sql_server_storage import sql_server_storage
from opus_core.simulation_state import SimulationState


class ExportCacheTableToSqlServerCommand(Command):
    """
    This class serves the request complied by the associated GUI.
    """
    def __init__(self, 
                 cache_directory, 
                 year,
                 table_name, 
                 hostname, 
                 username, 
                 password, 
                 database_name):
        self.cache_directory = cache_directory
        self.year = year
        self.table_name = table_name
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
        
    def execute(self):            
        in_storage = AttributeCache(cache_directory=self.cache_directory)
        
        out_storage = sql_server_storage(
            hostname = self.hostname, 
            username = self.username,
            password = self.password,
            database_name = self.database_name,
            )
        
        old_time = SimulationState().get_current_time()
        SimulationState().set_current_time(self.year)
        
        ExportStorage().export_dataset(
            dataset_name = self.table_name,
            in_storage = in_storage,
            out_storage = out_storage,
            )
            
        SimulationState().set_current_time(old_time)
    
    
from opus_core.tests import opus_unittest

import os, sys

from sets import Set
from shutil import rmtree
from tempfile import mkdtemp

from numpy import array

from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

from opus_core.store.sql_server_storage import TestSqlServerStorage


class TestExportCacheTableToSqlServerCommand(opus_unittest.TestCase):
    
    def setUp(self):
        self.pymssql_module = sql_server_storage._pymssql
            
        self.mock_pymssql = TestSqlServerStorage.mock_pymssql()
        sql_server_storage._pymssql = self.mock_pymssql
        
        self.temp_dir = mkdtemp(prefix='export_cache_table_to_sql_server')
        
    def tearDown(self):
        sql_server_storage._pymssql = self.pymssql_module
        SimulationState().remove_base_cache_directory()
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
    
    def test_export(self):
        # Set up a test cache
        storage = AttributeCache(cache_directory=self.temp_dir)
        SimulationState().set_current_time(2000)
        
        values = {
                'attribute1': array([1,2,3]),
                'attribute2': array([4,5,6]),
                }
        storage.write_table('foo', values)
            
        table_dir = os.path.join(self.temp_dir, '2000', 'foo')
        self.assert_(os.path.exists(table_dir))
        
        actual = Set(os.listdir(table_dir))
        if sys.byteorder=='little':
            expected = Set(['attribute1.li4', 'attribute2.li4'])
        else:
            expected = Set(['attribute1.bi4', 'attribute2.bi4'])
        self.assertEqual(expected, actual)
        
        exporter = ExportCacheTableToSqlServerCommand(
            cache_directory = self.temp_dir,
            year = '2000',
            table_name = 'foo',
            hostname = r'HOSTNAME\MOCK',
            username = 'mock_username',
            password = 'mock_password',
            database_name = 'mock_database_name',
            )
        exporter.execute()
            
        actual_parameters = self.mock_pymssql._parameters
        self.assertEqual(actual_parameters['hostname'], r'HOSTNAME\MOCK')
        self.assertEqual(actual_parameters['username'], 'mock_username')
        self.assertEqual(actual_parameters['password'], 'mock_password')
        self.assertEqual(actual_parameters['database_name'], 'mock_database_name')
            
        mock_conn = self.mock_pymssql._last_connection

        self.assert_(mock_conn._committed_last)
        
        self.assert_(mock_conn._closed)
        
        actual_queries = mock_conn._cursor._executed_queries

        possible_expected_queries = [
            ["CREATE TABLE foo (attribute1 INT, attribute2 INT)", 
                "CREATE TABLE foo (attribute2 INT, attribute1 INT)"],
            ["INSERT INTO foo (attribute1, attribute2) VALUES (1,4)", 
                "INSERT INTO foo (attribute2, attribute1) VALUES (4,1)"],
            ["INSERT INTO foo (attribute1, attribute2) VALUES (2,5)", 
                "INSERT INTO foo (attribute2, attribute1) VALUES (5,2)"],
            ["INSERT INTO foo (attribute1, attribute2) VALUES (3,6)", 
                "INSERT INTO foo (attribute2, attribute1) VALUES (6,3)"],
            ]
        self.assertEqual(len(actual_queries), len(possible_expected_queries))
        for actual_query, possible_queries in zip(actual_queries, possible_expected_queries):
            self.assert_(actual_query in possible_queries)
                
    def test_export_take_two(self):
        # Set up a test cache
        storage = AttributeCache(cache_directory=self.temp_dir)
        SessionConfiguration(new_instance=True, in_storage=storage)
        
        SimulationState().set_current_time(2001)
        values = {
                'spam': array([7,8,9]),
                'eggs': array(['a','ab','abc']),
                }
        storage.write_table('bar', values)
            
        table_dir = os.path.join(self.temp_dir, '2001', 'bar')
        self.assert_(os.path.exists(table_dir))
            
        actual = Set(os.listdir(table_dir))
        if sys.byteorder=='little':
            expected = Set(['spam.li4', 'eggs.iS3'])
        else:
            expected = Set(['spam.bi4', 'eggs.iS3'])
        self.assertEqual(expected, actual)
                    
        exporter = ExportCacheTableToSqlServerCommand(
            cache_directory = self.temp_dir,
            year = '2001',
            table_name = 'bar',
            hostname = r'HOSTNAME\MOCK',
            username = 'mock_username',
            password = 'mock_password',
            database_name = 'mock_database_name',
            )
        exporter.execute()
        
        mock_conn = self.mock_pymssql._last_connection
        
        actual_queries = mock_conn._cursor._executed_queries

        possible_expected_queries = [
            ["CREATE TABLE bar (spam INT, eggs VARCHAR(3))", 
                "CREATE TABLE bar (eggs VARCHAR(3), spam INT)"],
            ["INSERT INTO bar (spam, eggs) VALUES (7,'a')", 
                "INSERT INTO bar (eggs, spam) VALUES ('a',7)"],
            ["INSERT INTO bar (spam, eggs) VALUES (8,'ab')", 
                "INSERT INTO bar (eggs, spam) VALUES ('ab',8)"],
            ["INSERT INTO bar (spam, eggs) VALUES (9,'abc')", 
                "INSERT INTO bar (eggs, spam) VALUES ('abc',9)"],
            ]
        self.assertEqual(len(actual_queries), len(possible_expected_queries))
        for actual_query, possible_queries in zip(actual_queries, possible_expected_queries):
            self.assert_(actual_query in possible_queries)
    
    def test_that_get_data_from_correct_year(self):
        pass

    
if __name__ == '__main__':
    opus_unittest.main()