# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.export_storage import ExportStorage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.dbf_storage import dbf_storage
from opus_core.simulation_state import SimulationState
from opus_core.tools.command.command import Command

class ExportCacheToDbfTableCommand(Command):
    """
    This class serves the request complied by the associated GUI.
    """
    def __init__(self, 
                 dbf_directory,
                 table_name, 
                 cache_directory, 
                 year,
                 decimalcount,
                 ):
        self.cache_directory = cache_directory
        self.year = year
        self.table_name = table_name
        self.dbf_directory = dbf_directory
        self.decimalcount = decimalcount
        
        self._exporter = None # hook for unit tests

    def execute(self):
        in_storage = AttributeCache(cache_directory=self.cache_directory)
        out_storage = dbf_storage(storage_location=self.dbf_directory,
                                  digits_to_right_of_decimal=self.decimalcount)
        
        old_time = SimulationState().get_current_time()
        SimulationState().set_current_time(self.year)
        
        self._get_exporter().export_dataset(
            dataset_name = self.table_name,
            in_storage = in_storage,
            out_storage = out_storage,
            )
        
        SimulationState().set_current_time(old_time)
        return out_storage._short_names
    
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
    import os, sys
    from sets import Set
    from shutil import rmtree
    from tempfile import mkdtemp
    from numpy import array, int32
    from dbfpy.dbf import Dbf as _dbf_class
    from opus_core.tests.utils.cache_extension_replacements import replacements
    
    class FunctionalTests(opus_unittest.OpusTestCase):
        def setUp(self):
            self._temp_dir = mkdtemp(prefix='opus_tmp_export_cache_to_dbf_table_command')
            
        def tearDown(self):
            SimulationState().remove_base_cache_directory()
            if os.path.exists(self._temp_dir):
                rmtree(self._temp_dir)
        
        def test(self):
            # Set up a test cache
            storage = AttributeCache(cache_directory=self._temp_dir)
            SimulationState().set_current_time(2000)
            
            table_name = 'foo'
            
            values = {
                'attribute1': array([1,2,3], dtype=int32),
                'attribute2': array([4,5,6], dtype=int32),
                }
            
            storage.write_table(table_name, values)
                
            table_dir = os.path.join(self._temp_dir, '2000', table_name)
            self.assert_(os.path.exists(table_dir))
            
            actual = Set(os.listdir(table_dir))
            expected = Set(['attribute1.%(endian)si4' % replacements, 'attribute2.%(endian)si4' % replacements])
            self.assertEqual(expected, actual)
            
            exporter = ExportCacheToDbfTableCommand(
            cache_directory = self._temp_dir,
            year = '2000',
            table_name = table_name,
            dbf_directory = self._temp_dir,
            decimalcount = 4,
            )
            exporter.execute()
            
            out_storage = dbf_storage(self._temp_dir)
            
            db = _dbf_class(out_storage._get_file_path_for_table(table_name))
            length = max([len(values[key]) for key in values.keys()])
            i = 0
            field_type = {}
            for name, type in [field.fieldInfo()[:2] for field in db.header.fields]:
                field_type[name] = type
            for rec in db:
                for key in values.keys():
                    if field_type[key.upper()] is 'F':
                        self.assertAlmostEqual(values[key][i], rec[key], 4)
                    else:
                        self.assertEqual(values[key][i], rec[key])
                i = i + 1
            self.assertEquals(length, i, msg="More values expected than the dbf file contains")
            db.close()

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
                    
            command = ExportCacheToDbfTableCommand(
                     cache_directory = 'a-cache-directory', 
                     year = 1000,
                     table_name = 'a-table-name',
                     dbf_directory = 'a-dbf-directory',
                     decimalcount = 9,
                     )
            command._set_exporter(mock_exporter())
            
            SimulationState().set_current_time(-99)
            command.execute()
            
            self.assertEqual('a-table-name', command._get_exporter().dataset_name)
            self.assert_(isinstance(command._get_exporter().out_storage, dbf_storage))
            self.assert_(isinstance(command._get_exporter().in_storage, AttributeCache))
            self.assertEqual('a-dbf-directory', 
                             command._get_exporter().out_storage._get_base_directory())
            self.assertEqual(9, 
                             command._get_exporter().out_storage._digits_to_right_of_decimal)
            self.assertEqual('a-cache-directory', 
                             command._get_exporter().in_storage.get_storage_location())
            self.assertEqual(1000,
                             command._get_exporter().time_of_export_dataset)
            self.assertEqual(-99, 
                             SimulationState().get_current_time())
        
    
if __name__ == '__main__':
    opus_unittest.main()