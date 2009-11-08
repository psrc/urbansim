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

from sets import Set

from numpy import float32

from opus_core.store.old.storage import Storage
from opus_core.resources import Resources
from opus_core.opus_error import OpusError
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
        """cache_directory is the directory containing the year directories."""
        self.simulation_state = SimulationState()
        self._flt_storage_per_year = {}
        self.cache_directory = cache_directory
        
    def write_dataset(self, write_resources):
        values = write_resources['values']
        attrtype = write_resources['attrtype']
        out_table_name = write_resources['in_table_name']

        return self._write_dataset(out_table_name=out_table_name, values=values,
            attrtype=attrtype) 
        
    def _write_dataset(self, out_table_name, values, attrtype):
        """Will write to the SimulationState's current year.
        """
        time = SimulationState().get_current_time()
        self._write_dataset_to_cache(values, attrtype, time, out_table_name)
    
    def determine_field_names(self, load_resources, attributes='*'):
        in_table_name = load_resources['in_table_name']
        
        return self._determine_field_names(in_table_name=in_table_name,
            attributes=attributes)
                
    def _determine_field_names(self, in_table_name, attributes='*'):
        """Return the list of attributes found in any of the years of cached
        data for the load_resources['in_table_name'] table.
        """
        
        time = SimulationState().get_current_time()
        
        names = self._get_field_names_in_year(time, in_table_name, attributes)
        if names is None:
            names = []

        for past_time in self._cached_years_before_year(time):
            additional_names = self._get_field_names_in_year(past_time, in_table_name, attributes)
            if additional_names is not None:
                names += additional_names
                break
        
        if not names and (attributes == AttributeType.PRIMARY or attributes == '*'):
            raise OpusError('Attribute cache "%s" does not contain dataset table "%s" at or before time %s' %
                            (self.cache_directory, in_table_name, time))
        
        return list(Set(names))
    
    def _get_field_names_in_year(self, time, in_table_name, attributes):
        """
        Return in_table_name's attributes in the current year.
        """
        flt_storage = self.get_flt_storage_for_year(time)
        cache_path = flt_storage._get_base_directory()
        
        if flt_storage is not None:
            if os.path.exists(os.path.join(cache_path, in_table_name)):
                return flt_storage.determine_field_names(Resources({'in_table_name':in_table_name}), attributes)
            
        return None
    
    def _this_and_prior_time(self):
        times = [self.simulation_state.get_current_time()]
        if self._prior_year_exists():
            times.append(self.simulation_state.get_prior_time())
        return times
    
    def _prior_year_exists(self):
        return self.simulation_state.get_prior_time() in self._years_in_cache()
    
    def _get_cache_directory(self):
        if self.cache_directory is None:
            return self.simulation_state.get_cache_directory()
        else:
            return self.cache_directory
    
    def _get_base_directory(self, time):
        """Returns the year directory for this time within this attribute cache.
        """
        return os.path.join(self._get_cache_directory(), str(time))
    
    def get_flt_storage_for_year(self, year):
        """Returns a flt_storage object for this year of this cache.
        """
        if year is None:
            return None
        if year not in self._flt_storage_per_year.keys():
            self._flt_storage_per_year[year] = flt_storage(storage_location=self._get_base_directory(year))
        return self._flt_storage_per_year[year]
    
    def _get_flt_storage_for_attribute(self, attribute_name, table_name):
        """Returns flt_storage for most recent cached data for this attribute
        of this table.
        """
        time = self._get_year_for_attribute(attribute_name, table_name)
        return self.get_flt_storage_for_year(time)
    
    def _get_year_for_attribute(self, attribute_name, table_name):
        """Return most recent year containing cache data for this attribute
        of this table.  If not found in any year, raise an Exception.
        """
        current_year = SimulationState().get_current_time()
        
        table_found = False
        for time in self._cached_years_as_of_year(current_year):
            if os.path.exists(os.path.join(    
                    self._get_cache_directory(), 
                    str(time), 
                    table_name)):
                        
                table_found = True
                if self._is_attribute_in_given_times_cache(attribute_name, time, 
                        table_name):
                    return time
        
        if not table_found:
            raise OpusError("Table '%s' not found in attribute cache at or before year %s." % (table_name, current_year))
        else:
            raise AttributeError("Attribute '%s' not found in attribute cache in table '%s' at or before year %s. (%s)" 
                                 % (attribute_name, table_name, current_year, self._get_cache_directory()))
    
    def _cached_years_as_of_year(self, current_year):
        """Returns a list of current and prior years (current year first)"""
        current_and_prior_years = [current_year]
        current_and_prior_years += self._cached_years_before_year(current_year)
        
        return current_and_prior_years
    
    def _cached_years_before_year(self, current_year):
        """Returns a list of prior years (most recent year first)"""
        years = self._years_in_cache()
        years = [year for year in years if year < current_year]
        years.sort()
        years.reverse()
        return years
    
    def _years_in_cache(self):
        """Returns a sorted list (ascending order) of the current and prior years 
        having directories in the cache directory.
        """
        from os import listdir
        dirs = listdir(self._get_cache_directory())
        years = []
        for dir_name in dirs:
            try:
                year = int(dir_name)
                years.append(year)
            except:
                pass
        years.sort()
        return years
    
    def _write_dataset_to_cache(self, values, attribute_types, time, table_name):
        """ writes the values given in values to the cache"""
        write_resources = Resources({"values":values, 
                                     "attrtype":attribute_types, 
                                     "out_table_name":table_name})
        self.get_flt_storage_for_year(time).write_dataset(write_resources)
        
    def _is_attribute_in_given_times_cache(self, attribute_name, time, table_name):
        """Returns true if the given attribute exists in the given time's cache directory
           false otherwise"""
        return attribute_name.lower() in [attribute_name.lower()
                                          for attribute_name in
                                          self._attribute_names_in_given_times_cache(time, table_name)]
    
    def _attribute_names_in_given_times_cache(self, time, table_name):
        """Returns the set of attribute names found in this table's cache for this time.
        """
        flt_storage = self.get_flt_storage_for_year(time)
        
        return flt_storage._determine_field_names(in_table_name=table_name)
    
    
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree
from numpy import array
from numpy import ma

from opus_core.misc import write_to_file
from opus_core.variables.attribute_type import AttributeType
from opus_core.session_configuration import SessionConfiguration

class AttributeCacheTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.start_year = 2001
        self.dataset_name = "my_dataset"
        self.table_name = "my_dataset"
        self.flt_test_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "attr1.lf4")
        self.flt_index_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "my_id.lf4")
        self.flt_industrial_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "attr2.lf8")
        self.attr1_data = array([3.5,6.7,8.9,-1.2,6])
        self.index_data = array([1,2,3,4,5])
        self.attr2_data = array([5.2,7.4,1.2,4,98])
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=self.temp_dir)
        self.simulation_state.set_current_time(self.start_year)
        SessionConfiguration(new_instance=True,
                             in_storage=AttributeCache())
        os.makedirs(os.path.join(self.temp_dir, str(self.start_year), self.table_name))
        self.create_flt_file(self.flt_test_file_path, self.attr1_data)
        self.create_flt_file(self.flt_index_file_path, self.index_data)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)

    def test_get_field_names_in_year(self):
        cache_dir = os.path.join(self.temp_dir, 'test_get_field_names_in_year')
        SimulationState().set_cache_directory(cache_dir)
        
        os.makedirs(os.path.join(cache_dir, '1997', 'my_dataset'))
        attr_file_path = os.path.join(cache_dir, '1997', 'my_dataset', 'attr1.lf4')
        self.create_flt_file(attr_file_path, array([1,10,100]))
        attr_file_path = os.path.join(cache_dir, '1997', 'my_dataset', 'attr2.lf4')
        self.create_flt_file(attr_file_path, array([1,10,100]))

        os.makedirs(os.path.join(cache_dir, '1997', 'my_dataset2'))
        attr_file_path = os.path.join(cache_dir, '1997', 'my_dataset2', 'attr3.lf4')
        self.create_flt_file(attr_file_path, array([1,10,100]))

        os.makedirs(os.path.join(cache_dir, '1998', 'my_dataset'))
        attr_file_path = os.path.join(cache_dir, '1998', 'my_dataset', 'attr4.lf4')
        self.create_flt_file(attr_file_path, array([1,10,100]))
        attr_file_path = os.path.join(cache_dir, '1998', 'my_dataset', 'attr5.lf4')
        self.create_flt_file(attr_file_path, array([1,10,100]))

        SimulationState().set_current_time(1997)
        
        attribute_names = AttributeCache()._get_field_names_in_year(
            time = 1997,
            in_table_name = 'my_dataset',
            attributes='*'
        )
        self._is_same_set(['attr1','attr2'], attribute_names)
        
        attribute_names = AttributeCache()._get_field_names_in_year(
            time = 1997,
            in_table_name = 'my_dataset2',
            attributes='*'
        )
        self._is_same_set(['attr3'], attribute_names)

        attribute_names = AttributeCache()._get_field_names_in_year(
            time = 1998,
            in_table_name = 'my_dataset',
            attributes='*'
        )
        self._is_same_set(['attr4','attr5'], attribute_names)

        attribute_names = AttributeCache()._get_field_names_in_year(
            time = 1998,
            in_table_name = 'my_dataset2',
            attributes='*'
        )
        self.assertEqual(None, attribute_names)
        
    def _is_same_set(self, a, b):
        """Asserts if the sets a and b do not contain the same values with no duplicates."""
        self.assertEqual(len(a), len(b))
        self.assertEqual(Set(a), Set(b))
        self.assertEqual(len(a), len(Set(a)), msg="Duplicates in %s" % a) 
        self.assertEqual(len(b), len(Set(b)), msg="Duplicates in %s" % b) 
        
    def test_current_and_prior_years(self):
        cache_dir = os.path.join(self.temp_dir, 'test_current_and_prior_years')
        SimulationState().set_cache_directory(cache_dir)
        
        #os.makedirs(os.path.join(cache_dir, '1997', 'my_dataset'))
        #attr_file_path = os.path.join(cache_dir, '1997', 'my_dataset', 'attr.lf4')
        #self.create_flt_file(attr_file_path, array([1,10,100]))

        os.makedirs(os.path.join(cache_dir, '10')) # will it skip years?
        os.makedirs(os.path.join(cache_dir, '1997'))
        os.makedirs(os.path.join(cache_dir, '1998'))
        os.makedirs(os.path.join(cache_dir, '1999'))
        os.makedirs(os.path.join(cache_dir, '2000'))
        os.makedirs(os.path.join(cache_dir, '2001'))
        
        SimulationState().set_current_time(10) # Should not use current year.
        
        years = AttributeCache()._cached_years_before_year(2000)
        self.assertEqual([1999, 1998, 1997, 10], years)
        
        years = AttributeCache()._cached_years_as_of_year(2000)
        self.assertEqual([2000, 1999, 1998, 1997, 10], years)
                     
    def create_flt_file(self, file_name, data_array):
        """ Create a flt file for testing purposes"""
        write_to_file(file_name, data_array.astype(float32))

    def test_years_in_cache(self):
        cache_dir = os.path.join(self.temp_dir, 'test_years_in_cache')
        SimulationState().set_cache_directory(cache_dir)
        os.makedirs(os.path.join(cache_dir, '1997'))
        os.makedirs(os.path.join(cache_dir, '1998'))
        os.makedirs(os.path.join(cache_dir, '2000'))
        os.makedirs(os.path.join(cache_dir, 'indicators'))
        years = AttributeCache()._years_in_cache()
        self.assertEqual([1997,1998,2000], years)

    def test_get_year_for_attribute(self):
        SimulationState().set_cache_directory(self.temp_dir)
        
        AttributeCache()._get_year_for_attribute('attr1', self.table_name)
        
        try:
            AttributeCache()._get_year_for_attribute('idonotexist', self.table_name)
        except AttributeError:
            pass
        else:
            self.fail("Attribute 'idonotexist' does not exist in the attribute cache, but no error was raised.")
        
        try:
            AttributeCache()._get_year_for_attribute('attr1', 'idonotexist')
        except OpusError:
            pass
        else:
            self.fail("Table 'idonotexist' does not exist in the attribute cache, but no error was raised.")

if __name__ == '__main__':
    opus_unittest.main()