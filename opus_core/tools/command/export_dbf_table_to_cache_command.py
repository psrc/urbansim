# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.export_storage import ExportStorage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.dbf_storage import dbf_storage
from opus_core.simulation_state import SimulationState

class ExportDbfTableToCacheCommand(object):
    """
    This class serves the request complied by the associated GUI.
    """
    def __init__(self, 
                 dbf_directory,
                 table_name, 
                 cache_directory, 
                 year):
        self.cache_directory = cache_directory
        self.year = year
        self.table_name = table_name
        self.dbf_directory = dbf_directory
        
        self._exporter = None # hook for unit tests

    def execute(self):
        in_storage = dbf_storage(storage_location=self.dbf_directory)
        
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
    dbf_storage(storage_location='')
except:
    pass
else:
    import os
    
    from sets import Set
    from shutil import rmtree
    from tempfile import mkdtemp
    
    from numpy import array
    from numpy import ma
    
    from opus_core.opus_package import OpusPackage
    
    class FunctionalTests(opus_unittest.OpusTestCase):
        def setUp(self):
            self._temp_dir = mkdtemp(prefix='opus_tmp_export_dbf_table_to_cache_command')
            
        def tearDown(self):
            SimulationState().remove_base_cache_directory()
            if os.path.exists(self._temp_dir):
                rmtree(self._temp_dir)
        
        def test(self):
            opus_core_path = OpusPackage().get_opus_core_path()
            dbf_directory = os.path.join(
                opus_core_path, 'tests', 'data', 'dbf')
            table_name = 'test_logical'
            cache_directory = self._temp_dir
            year = 1000
    
            exporter = ExportDbfTableToCacheCommand(
                dbf_directory = dbf_directory,
                table_name = table_name,
                cache_directory = cache_directory,
                year = year,
                )
            exporter.execute()
            
            attribute_cache = AttributeCache(cache_directory=cache_directory)
            
            old_time = SimulationState().get_current_time()
            SimulationState().set_current_time(year)
            
            values = attribute_cache.load_table(table_name)
            
            self.assertEqual(Set(['keyid', 'works']), Set(values.keys()))
            self.assert_(ma.allequal(array([1,2,3,4,5]), values['keyid']))
            self.assert_(ma.allequal(array([1,1,-1,0,0]), values['works']))
            
            SimulationState().set_current_time(old_time)
            

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
                    
            command = ExportDbfTableToCacheCommand(
                     dbf_directory = 'a-dbf-directory',
                     table_name = 'a-table-name',
                     cache_directory = 'a-cache-directory', 
                     year = 1000)
            command._set_exporter(mock_exporter())
            
            SimulationState().set_current_time(-99)
            command.execute()
            
            self.assertEqual('a-table-name', command._get_exporter().dataset_name)
            self.assert_(isinstance(command._get_exporter().in_storage, dbf_storage))
            self.assert_(isinstance(command._get_exporter().out_storage, AttributeCache))
            self.assertEqual('a-dbf-directory', 
                             command._get_exporter().in_storage._get_base_directory())
            self.assertEqual('a-cache-directory', 
                             command._get_exporter().out_storage.get_storage_location())
            self.assertEqual(1000,
                             command._get_exporter().time_of_export_dataset)
            self.assertEqual(-99, 
                             SimulationState().get_current_time())
        
    
if __name__ == '__main__':
    opus_unittest.main()