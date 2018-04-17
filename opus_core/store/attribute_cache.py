# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from numpy import array
from opus_core.misc import unique
from opus_core.store.storage import Storage
from opus_core.store.flt_storage import flt_storage
from opus_core.simulation_state import SimulationState


class AttributeCache(Storage):
    """This Storage class caches data via the file system, which is faster
    than running directly from a database, and allows the simulation to 
    unload computed values from memory when they are no longer needed.
    
    The cached data are stored in a 'cache directory', whose name contains the 
    datetime in which it was created.  In this directory there is a separate
    sub-directory for each year with cached data.  Inside each year directory 
    is a dataset directory for any dataset with cached directory.  
    Inside the dataset directory
    are a set of files, one per attribute of this dataset.  Each attribute 
    file has a suffix indicating the type of data stored in it.
    
    For instance, the file:
    
        'D:\cache\2005_12_14__21_14\2000\gridcells\grid_id.li4 
    
    contains an array of int32 values that are the grid_id attribute for 
    the gridcells dataset as it was last computed in year 2000 of the 
    simulation begun on December 14, 2005 at 21:14 hours.
    
    Delegates as much work as possible to flt_storage objects created
    for a year directory.
    
    It currently uses flt_storage.
    """
    def __init__(self, cache_directory=None):
        """cache_location is the directory containing the year directories."""
        self.simulation_state = SimulationState()
        self._cache_location = cache_directory
        self._flt_storage_per_year = {}
        
    def get_storage_location(self):
        if self._cache_location is None:
            return SimulationState().get_cache_directory()
        else:
            return self._cache_location
    
    def get_flt_storage_for_year(self, year):
        """Returns a flt_storage object for this year of this cache.
        """
        if year is None:
            return None
        if year not in self._flt_storage_per_year.keys():
            base_directory = os.path.join(self.get_storage_location(), str(year))
            self._flt_storage_per_year[year] = flt_storage(storage_location=base_directory)
        return self._flt_storage_per_year[year]
    
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True):
        result = {}
        columns_names_and_years = self._get_column_names_and_years(table_name, lowercase=lowercase)        
        
        for column_name, year in columns_names_and_years:
            if isinstance(column_names, list) and column_name not in column_names:
                continue
            storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
            result.update(storage.load_table(table_name, column_names=[column_name], lowercase=lowercase))

        return result

    def get_current_storage(self):
        year = SimulationState().get_current_time()
        return flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
    
    def delete_table(self, table_name):
        storage = self.get_current_storage()
        storage.delete_table(table_name)
        
    def write_table(self, table_name, table_data, mode = Storage.OVERWRITE):
        storage = self.get_current_storage()
        return storage.write_table(table_name, table_data, mode)

    def delete_computed_tables(self):
        # Use this method only in conjunction with deleting computed attributes of the datasets:
        # dataset.delete_computed_attributes()
        year = SimulationState().get_current_time()
        storage_directory = os.path.join(self.get_storage_location(), '%s' % year)
        if not os.path.exists(storage_directory):
            return array([])
        storage = flt_storage(storage_directory)
        tables = storage.get_table_names()
        tables = [table for table in tables if (table.endswith('.computed'))]
        deleted = array(map(lambda table: storage.delete_table(table), tables))
        if deleted.size > 0:
            return array(tables)[deleted]
        return array(tables)

    def get_column_names(self, table_name, lowercase=True):
        columns = self._get_column_names_and_years(table_name, lowercase)
        return [column[0] for column in columns]
    
    def get_years(self, table_name):
        columns = self._get_column_names_and_years(table_name)
        return unique(array([column[1] for column in columns]))
        
    def get_table_names(self):
        result = []
        for year in self._get_sorted_list_of_years():
            try:
                storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
                tables = storage.get_table_names()
                tables = [table for table in tables if (not table in result)]
                result.extend(tables)
            except:
                pass
        return result
    
    def _get_column_names_and_years(self, table_name, lowercase=True):
        column_names = []
        result = []
        found=False
        for year in self._get_sorted_list_of_years():
            try:
                storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
                columns = storage.get_column_names(table_name, lowercase)
                columns = [column for column in columns if (not column in column_names)]
                column_names.extend(columns)
                result.extend([(column_name, year) for column_name in columns])
                found=True
            except:
                pass
        if not found:
            raise StandardError,"Table %s not found" % table_name
        return result
        
    
    def _get_sorted_list_of_years(self, start_with_current_year=True):
        """Returns a sorted list (descending order) of the years 
        that have directories in the cache directory, starting with
        the current year of the simulation (if "start_with_current_year" is True) 
        and its prior years. If "start_with_current_year" is False, all years are returned.
        """
        from os import listdir
        if start_with_current_year:
            current_year = SimulationState().get_current_time()
        dirs = flt_storage(self.get_storage_location()).listdir_in_base_directory()
        years = []
        for dir_name in dirs:
            try:
                year = int(dir_name)
                if not start_with_current_year:
                    current_year = year + 1
                if (year <= current_year):
                    years.append(year)
            except:
                pass
        years.sort()
        years.reverse()
        return years


from opus_core.tests import opus_unittest
from opus_core.opus_package import OpusPackage
from numpy import int32

class AttributeCacheTests(opus_unittest.OpusTestCase):
    def setUp(self):
        opus_core_path = OpusPackage().get_opus_core_path()
        self.local_test_data_path = os.path.join(
            opus_core_path, 'data', 'test_cache')
        self.storage = AttributeCache(self.local_test_data_path)
        self._SimulationState_time = SimulationState().get_current_time()
    
    def tearDown(self):
        SimulationState().set_current_time(self._SimulationState_time)
        
    def test_get_column_names_one_column(self):
        SimulationState().set_current_time(1981)
        expected = ['year']
        actual = self.storage.get_column_names('base_year')
        self.assertEqual(expected, actual)
        
    def test_get_column_names_one_column_nonexisting_year(self):
        SimulationState().set_current_time(1982)
        expected = ['year']
        actual = self.storage.get_column_names('base_year')
        self.assertEqual(expected, actual)
        
    def test_get_column_names_two_columns(self):
        SimulationState().set_current_time(1981)
        expected = ['city_id', 'city_name']
        expected.sort()
        actual = self.storage.get_column_names('cities')
        actual.sort()
        self.assertEqual(expected, actual)
        
    def test_get_column_names_for_table_not_stored_in_1981(self):
        SimulationState().set_current_time(1981)
        expected = ['building_type_id', 'is_residential', 'name', 'units']
        expected.sort()
        actual = self.storage.get_column_names('building_types')
        actual.sort()
        self.assertEqual(expected, actual)
        
    def test_load_table_1980(self):
        SimulationState().set_current_time(1980)
        expected = {
            'year': array([1980]),
            }
        actual = self.storage.load_table('base_year')
        self.assertEqual(expected, actual)
        
    def test_load_table_1981(self):
        SimulationState().set_current_time(1981)
        expected = {
            'year': array([1981]),
            }
        actual = self.storage.load_table('base_year')
        self.assertEqual(expected, actual)
        
    def test_load_table_1980_if_not_in_1981(self):
        SimulationState().set_current_time(1981)
        expected = {
            'county_id': array([39]),
            'county_name': array(['Lane']),
            }
        actual = self.storage.load_table('counties')
        self.assertEqual(expected, actual)
        
    def test_load_table_1982(self):
        SimulationState().set_current_time(1982)
        expected = {
            'year': array([1981]),
            }
        actual = self.storage.load_table('base_year')
        self.assertEqual(expected, actual)
        
    def test_load_table_with_two_columns_1980(self):
        SimulationState().set_current_time(1980)
        expected = {
            'city_id': array([3, 1, 2], dtype='<i4'),
            'city_name': array(['Unknown', 'Eugene', 'Springfield']),
            }
        actual = self.storage.load_table('cities')
        self.assertDictsEqual(expected, actual)
        
    def test_load_table_with_two_columns_1981_one_column_unchanged_from_1980(self):
        SimulationState().set_current_time(1981)
        expected = {
            'city_id': array([3, 1, 2], dtype='<i4'),
            'city_name': array(['NotUnknownAnymore', 'Eugene', 'Springfield']),
            }
        actual = self.storage.load_table('cities')
        self.assertDictsEqual(expected, actual)

    def test_load_table_with_different_length_and_num_of_columns_between_1980_and_1981(self):
        SimulationState().set_current_time(1981)
        expected = {
            'dumb_dataset_id': array([1, 2, 3, 4], dtype='int32'),                                   ##attribute values read from 1981
            'dumb_number':     array([97, 101, 8, 79], dtype='int32'),                               ##attribute values read from 1981
            'dumb_name':       array(['ninety-seven', 'one hundred one', 'eight'], dtype='|S15')   ##attribute values read from 1980
            }
        actual = self.storage.load_table('dumb_datasets')
        self.assertDictsEqual(expected, actual)
        
    def test_load_one_attribute(self):
        SimulationState().set_current_time(1980)
        expected = {'city_id': array([3, 1, 2], dtype='<i4')}
        actual = self.storage.load_table('cities', column_names=['city_id'])
        self.assertDictsEqual(expected, actual)
        
import tempfile
from shutil import rmtree
from tempfile import mkdtemp
from numpy import array
import numpy
from opus_core.tests.utils.cache_extension_replacements import replacements
        
class AttributeCacheWriteTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache')
        self.storage = AttributeCache(self.temp_dir)
        self.table_name = 'test_table'
        self._SimulationState_time = SimulationState().get_current_time()
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        SimulationState().set_current_time(self._SimulationState_time)
    
    def test_write(self):
        year = 1980
        SimulationState().set_current_time(year)
        expected = array([100, 70], dtype=int32)
        table_data = {'int_column': expected}
        # file name will be e.g. 'int_column.li4' for a little-endian machine
        full_name = os.path.join(self.temp_dir, str(year),  self.table_name, 'int_column.%(endian)si4'%replacements)
        self.storage.write_table(self.table_name, table_data)
        self.assert_(os.path.exists(full_name))
        # dtype will be e.g. '<i4' for a little-endian machine
        actual = numpy.fromfile(full_name, dtype='%(numpy_endian)si4' % replacements)
        self.assert_((expected==actual).all())
        
class TestAttributeCacheGetTableNames(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='opus_core_test_delimited_storage_get_table_names')
        self.storage = AttributeCache(cache_directory = self.temp_dir)
        os.makedirs(os.path.join(self.temp_dir, '1980', 'cities'))
        os.makedirs(os.path.join(self.temp_dir, '1980', 'base_year'))
        os.makedirs(os.path.join(self.temp_dir, '1981', 'base_year'))
        open(os.path.join(self.temp_dir, '1980', 'cities', 'city_name.iS17'), 'w').close()
        open(os.path.join(self.temp_dir, '1980', 'base_year', 'year.li4'), 'w').close()
        open(os.path.join(self.temp_dir, '1981', 'base_year', 'year.li4'), 'w').close()
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
            
    def test_get_table_names_from_1980(self):
        SimulationState().set_current_time(1980)
        expected = ['cities', 'base_year']
        expected.sort()
        actual = self.storage.get_table_names()
        actual.sort()
        self.assertEquals(expected, actual)
        
    def test_get_table_names_from_1981(self):
        SimulationState().set_current_time(1981)
        expected = ['cities', 'base_year']
        expected.sort()
        actual = self.storage.get_table_names()
        actual.sort()
        self.assertEquals(expected, actual)
  
class AttributeCacheDeleteTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp_attribute_cache_delete')
        self.storage = AttributeCache(self.temp_dir)
        self._SimulationState_time = SimulationState().get_current_time()
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        SimulationState().set_current_time(self._SimulationState_time)
    
    def get_table_path(self, year, table):
        return os.path.join(self.temp_dir,  "%s" % year, table)
        
    def test_delete_computed_tables(self):
        year = 1980
        tables_keep = ['test_table1', 'test_table2']
        tables_delete = ['test_table1.computed', 'test_table2.computed']
        for table in tables_keep+tables_delete:
            os.makedirs(os.path.join(self.temp_dir, str(year), table))
            open(os.path.join(self.temp_dir, str(year), table, 'attr1.i16'), 'w').close()
            open(os.path.join(self.temp_dir, str(year), table, 'attr2.i32'), 'w').close()
        SimulationState().set_current_time(year)
        #check if all tables exist before the test
        for table in tables_keep+tables_delete: 
            self.assert_(os.path.exists(self.get_table_path(year, table)))
        self.storage.delete_computed_tables()
        
        #check if the right tables exist
        for table in tables_keep: 
            self.assert_(os.path.exists(self.get_table_path(year, table)))
        # and not the others
        for table in tables_delete: 
            self.assert_(not os.path.exists(self.get_table_path(year, table)))
 
    def test_delete_computed_tables_if_nothing_to_delete(self):
        year = 1980
        tables_keep = ['test_table1', 'test_table2']
        tables_delete = []
        for table in tables_keep+tables_delete:
            os.makedirs(os.path.join(self.temp_dir, str(year), table))
            open(os.path.join(self.temp_dir, str(year), table, 'attr1.i16'), 'w').close()
            open(os.path.join(self.temp_dir, str(year), table, 'attr2.i32'), 'w').close()
        SimulationState().set_current_time(year)
        #check if all tables exist before the test
        for table in tables_keep+tables_delete: 
            self.assert_(os.path.exists(self.get_table_path(year, table)))
        self.storage.delete_computed_tables()
        
        #check if the right tables exist
        for table in tables_keep: 
            self.assert_(os.path.exists(self.get_table_path(year, table)))

    def test_delete_computed_tables_if_cache_doesnt_exist(self):
        SimulationState().set_current_time(1990)
        res = self.storage.delete_computed_tables()
        self.assert_(res.size == 0)
        
if __name__ == '__main__':
    opus_unittest.main()