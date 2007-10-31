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

import os
from opus_core.store.storage import Storage
from opus_core.store.flt_storage import flt_storage
from opus_core.simulation_state import SimulationState
from opus_core.misc import unique_values


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
    
    def load_table(self, table_name, column_names=Storage.ALL_COLUMNS, lowercase=True,
            id_name=None # Not used for this storage, but required for SQL-based storages
            ):
        result = {}
        column_names_for_year = {}

        years = self.get_years(table_name)
        if isinstance(column_names, list):
            columns = column_names
        else:
            columns = self.get_column_names(table_name, lowercase)
        
        for year in years:
            column_names_for_year[year] = []
            for column_name in columns:
                column_names_for_year[year].append(column_name)
        for year in column_names_for_year:
            storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
            result.update(storage.load_table(table_name, column_names=column_names_for_year[year], lowercase=lowercase))
        return result


    def write_table(self, table_name, table_data):
        year = SimulationState().get_current_time()
        storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
        return storage.write_table(table_name, table_data)


    def get_column_names(self, table_name, lowercase=True):
        columns = self._get_column_names_and_years(table_name, lowercase)
        return [column[0] for column in columns]
    
    def get_years(self, table_name):
        columns = self._get_column_names_and_years(table_name)
        return unique_values(array([column[1] for column in columns]))
        
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
        for year in self._get_sorted_list_of_years():
            try:
                storage = flt_storage(os.path.join(self.get_storage_location(), '%s' % year))
                columns = storage.get_column_names(table_name, lowercase)
                columns = [column for column in columns if (not column in column_names)]
                column_names.extend(columns)
                result.extend([(column_name, year) for column_name in columns])
            except:
                pass
        return result
        
    
    def _get_sorted_list_of_years(self):
        """Returns a sorted list (descending order) of the current and prior years 
        having directories in the cache directory.
        """
        from os import listdir
        current_year = SimulationState().get_current_time()
        dirs = listdir(self.get_storage_location())
        years = []
        for dir_name in dirs:
            try:
                year = int(dir_name)
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
        

if __name__ == '__main__':
    opus_unittest.main()