# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from sets import Set

from numpy import array, int32, concatenate


from opus_core.datasets.abstract_dataset import AbstractDataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.attribute_type import AttributeType
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.storage import Storage

class MultipleYearDatasetView(AbstractDataset):
    """
    A dataset whose data is the union of multiple years of another dataset.
    """

    def __init__(self, name_of_dataset_to_merge, in_table_name, attribute_cache, years_to_merge, *args, **kwargs):
        """Create a dataset that contains this many years of data from this dataset.
        
        Years are from current year backwards, inclusive.
        """
        self.name_of_dataset_to_merge = name_of_dataset_to_merge
        self.years_to_merge = years_to_merge
        
        self._validate_primary_attributes_same_for_all_years(name_of_dataset_to_merge, in_table_name, attribute_cache, years_to_merge)
        
        # Add 'year' to id_names.
        dataset_for_current_year = SessionConfiguration().get_dataset_from_pool(
            self.name_of_dataset_to_merge)
        id_names = dataset_for_current_year.get_id_name() + ['year']
        self.base_id_name = dataset_for_current_year.get_id_name()
        
        # Masquerade as a dataset of the right type (important for computing the right variables).
        dataset_name = dataset_for_current_year.get_dataset_name()
        
        AbstractDataset.__init__(self,
                                 id_name=id_names,
                                 in_table_name=in_table_name,
                                 dataset_name=dataset_name,
                                 *args, **kwargs)

        coord_system = dataset_for_current_year.get_coordinate_system()
        if coord_system is not None:
            self._coordinate_system = coord_system
                    
    def _validate_primary_attributes_same_for_all_years(self, name_of_dataset_to_merge, in_table_name, attribute_cache, years_to_merge):
        # Make sure that the set of primary attributes is the same for all years
        # being merged; otherwise, cannot do merge.
        old_year = SimulationState().get_current_time()
        try:
            primary_attributes_from_other_years = None
            for year in years_to_merge:
                SimulationState().set_current_time(year)
                primary_attributes_for_this_year = attribute_cache.get_column_names(table_name = in_table_name)
                
                if primary_attributes_from_other_years is None:
                    primary_attributes_from_other_years = primary_attributes_for_this_year
                else:
                    if Set(primary_attributes_for_this_year) != Set(primary_attributes_from_other_years):
                        raise AttributeError("The set of primary attributes of dataset '%s' must be "
                                             "the same for each year to merge %s." 
                                                 % (name_of_dataset_to_merge, str(years_to_merge)))
                    
                
        finally:
            SimulationState().set_current_time(old_year)
            
        
    def load_dataset(self, resources=None, nchunks=None, attributes=None, in_storage=None,
                     in_table_name=None, lowercase=None, load_id_with_each_chunk=None,
                     flush_after_each_chunk=None):
        """Loads multiple years of data into each attribute.
        
        See opus_core.dataset for description of arguments.
        """
        
        # Load attributes one at a time.
        if attributes is None:
            if resources is not None and 'attributes' in resources:
                attributes = resources.get('attributes', '*')
            else:
                attributes = '*'
                
        if in_storage is None and resources is not None:
            in_storage = resources['in_storage']
        
        if attributes == Storage.ALL_COLUMNS:
            attributes = []
            if in_storage.table_exists(in_table_name):
                attributes += in_storage.get_column_names(
                    table_name = in_table_name)
                
            if in_storage.table_exists(in_table_name + '.computed'):
                attributes += in_storage.get_column_names(
                    table_name = in_table_name + '.computed')
                
        size_map = {}
        for attribute_name in attributes:
            values = self._get_attribute_for_year(self.name_of_dataset_to_merge, 
                                                  attribute_name,
                                                  self.years_to_merge[0])
            size_map[self.years_to_merge[0]] = values.size
            for year in self.years_to_merge[1:]:
                year_data = self._get_attribute_for_year(self.name_of_dataset_to_merge, 
                                                         attribute_name,
                                                         year)
                size_map[year] = year_data.size
                values = concatenate( (values, year_data) )
                
            self.add_attribute(name=attribute_name, data=values)

        # add the 'year' attribute, too.
        values = array([], dtype='int32')
        for year in self.years_to_merge:
            size = size_map[year]
            values = concatenate( (values, array([year]*size)) )
            
        self.add_attribute(name='year', data=values)
                
    def _get_attribute_for_year(self, dataset_name, attribute_name, year):
        """Return the attribute values for this year."""
        calling_dataset_pool = SessionConfiguration().get_dataset_pool()
        calling_time = SimulationState().get_current_time()
        SimulationState().set_current_time(year)
        try:
            my_dataset_pool = DatasetPool(
                package_order=calling_dataset_pool.get_package_order(),
                storage=AttributeCache())
            dataset = my_dataset_pool.get_dataset(dataset_name)
            attribute_name = attribute_name.replace('DDDD',repr(year))
            dataset.compute_variables(attribute_name, my_dataset_pool)
            values = dataset.get_attribute(attribute_name)
            return values
        finally:
            SimulationState().set_current_time(calling_time)
            
    #===========================================================================
    # Methods overridden from AbstractDataset.
    #===========================================================================
    def get_attribute(self, name):
        if isinstance(name, VariableName):
            name = name.get_alias()
        return self.attribute_boxes[name]._data
    
    def determine_stored_attribute_names(self, resources=None, in_storage=None,
                                              in_table_name=None, attribute_type=AttributeType.PRIMARY):
        dataset_for_current_year = SessionConfiguration().get_dataset_from_pool(
            self.name_of_dataset_to_merge)
        return dataset_for_current_year.determine_stored_attribute_names()
    
    def compute_variables(self, names, dataset_pool=None, resources=None, quiet=False):
        self.load_dataset(resources, attributes=names)
        
    def _do_flush_attribute(self, name):
        raise NotImplementedError('_do_flush_attribute')
    
    def write_dataset(self, resources = None, attributes=None, out_storage=None,
                       out_table_name=None, valuetypes=None):
        """Write dataset into the media given in out_storage (see also load_dataset).
        If 'attributes' is '*' all attributes that are known to the dataset (i.e. primary  + computed) are written.
        'attributes' can be also a list of attributes or AttributeType.PRIMARY or AttributeType.COMPUTED.
        """
        raise NotImplementedError('write_dataset')
    
    def load_dataset_if_not_loaded(self, resources=None, nchunks=None, attributes=None,
                            in_storage=None, in_table_name=None, lowercase=None):
        raise NotImplementedError('load_dataset_if_not_loaded')
    

import os
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree

from numpy import array, ma
from numpy import ma

from opus_core.cache.create_test_attribute_cache import CreateTestAttributeCache

class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
        
    def _create_data_with_same_ids_each_year(self, years_to_merge):
        """Return merged dataset for this set of years."""
        test_data = {
            1000:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([10,20,30]),
                    'attr2':array([100,200,300]),
                    'attr3':array([1000,2000,3000]),
                    },
                },
            1001:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([11,21,31]),
                    'attr2':array([111,211,311]),
                    'attr3':array([1111,2111,3111]),
                    },
                },
            1002:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([12,22,32]),
                    'attr2':array([122,222,322]),
                    'attr3':array([1222,2222,3222]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, test_data)
        
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['opus_core'],
                             in_storage=attribute_cache)
        ds = MultipleYearDatasetView(
            name_of_dataset_to_merge = 'test',
            in_table_name = 'tests',
            attribute_cache = attribute_cache,
            years_to_merge = years_to_merge
        )
        return ds
    
    def _create_data_with_different_ids_each_year(self, years_to_merge):
        """Return merged dataset for this set of years."""
        test_data = {
            1000:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([10,20,30]),
                    'attr2':array([100,200,300]),
                    'attr3':array([1000,2000,3000]),
                    },
                },
            1001:{
                'tests':{
                    'id':array([3,4,5]),
                    'attr1':array([11,21,31]),
                    'attr2':array([111,211,311]),
                    'attr3':array([1111,2111,3111]),
                    },
                },
            1002:{
                'tests':{
                    'id':array([3,6,7]),
                    'attr1':array([12,22,32]),
                    'attr2':array([122,222,322]),
                    'attr3':array([1222,2222,3222]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, test_data)
        
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['opus_core'],
                             in_storage=attribute_cache)
        ds = MultipleYearDatasetView(
            name_of_dataset_to_merge = 'test',
            in_table_name = 'tests',
            years_to_merge = years_to_merge,
            attribute_cache = attribute_cache,
        )
        return ds
        
    def test_compute_a_variable(self):
        """Return merged dataset for this set of years."""
        test_data = {
            1000:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([10,20,30]),
                    },
                },
            1001:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([40,50,60]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, test_data)
        
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['opus_core'],
                             in_storage=attribute_cache)
        ds = MultipleYearDatasetView(
            name_of_dataset_to_merge = 'test',
            in_table_name = 'tests',
            years_to_merge = [1000,1001],
            attribute_cache = attribute_cache,
        )
        
        ds.compute_variables(['opus_core.test.attr1_times_2'])
                
    def _check_dataset_methods_on_dataset_view(self, ds, years_to_merge):
        self.assert_(ds is not None)
        ds.load_dataset(attributes='*',
                        in_table_name='tests',
                        in_storage=AttributeCache()
                        )
        id = ds.get_attribute('id')
        attr1 = ds.get_attribute('attr1')
        
        # Does compute_variables work?
        ds.compute_variables(['opus_core.test.attr1_times_2'])
        attr1_times_2 = ds.get_attribute('attr1_times_2')
        
        # Are values as expected?
        self.assert_(ma.allequal(attr1*2, attr1_times_2))
        
        # Does results have expected number of elements?
        self.assertEqual(len(years_to_merge)*3, len(attr1_times_2))
        
        # Does _compute_if_needed work?
        ds._compute_if_needed(
            'opus_core.test.attr2_times_2',
            dataset_pool=SessionConfiguration().get_dataset_pool()
        )
        attr2_times_2 = ds.get_attribute('attr2_times_2')
        attr2 = ds.get_attribute('attr2')
        self.assert_(ma.allequal(attr2*2, attr2_times_2))
            
    def test_years_1000_1001_with_same_ids_each_year(self):
        years_to_merge = [1000,1001]
        ds = self._create_data_with_same_ids_each_year(years_to_merge)
        self._do_years_1000_1001_tests(ds, years_to_merge)
        
    def test_years_1000_1001_with_different_ids_each_year(self):
        years_to_merge = [1000,1001]
        ds = self._create_data_with_different_ids_each_year(years_to_merge)
        self._do_years_1000_1001_tests(ds, years_to_merge)
        
    def _do_years_1000_1001_tests(self, ds, years_to_merge):
        self._check_dataset_methods_on_dataset_view(ds, years_to_merge)
        
        # Test that are getting exact set of expected values.
        attr1 = ds.get_attribute('attr1')
        self.assertEqual(10+20+30+11+21+31, attr1.sum())
        attr1_times_2 = ds.get_attribute('attr1_times_2')
        self.assertEqual(attr1.sum()*2, attr1_times_2.sum())
        
        # Test some other methods inherited from Dataset.
        self.assert_(ds.has_attribute('attr1'))
        self.assert_(not ds.has_attribute('attribute_not_there'))
        
        # Can get 'year' values?
        years = ds.get_attribute('year')
        self.assert_(ma.allequal(array([1000,1000,1000,1001,1001,1001]), years))
        
    def test_years_1001_1002(self):
        years_to_merge = [1001,1002]
        ds = self._create_data_with_same_ids_each_year(years_to_merge)
        self._check_dataset_methods_on_dataset_view(ds, years_to_merge)
        
        # Test that are getting exact set of expected values.
        attr1 = ds.get_attribute('attr1')
        self.assertEqual(11+21+31+12+22+32, attr1.sum())
        attr1_times_2 = ds.get_attribute('attr1_times_2')
        self.assertEqual(attr1.sum()*2, attr1_times_2.sum())
        
    def test_years_1001_1002_1003(self):
        years_to_merge = [1001,1002,1003]
        ds = self._create_data_with_same_ids_each_year(years_to_merge)
        self._check_dataset_methods_on_dataset_view(ds, years_to_merge)
        
    def test_with_different_ids_and_different_attributes_each_year(self):
        years_to_merge = [1000,1001]
        
        test_data = {
            1000:{
                'tests':{
                    'id':array([1,2,3]),
                    'attr1':array([10,20,30]),
                    'attr2':array([100,200,300]),
                    },
                },
            1001:{
                'tests':{
                    'id':array([4,5,6]),
                    'attr1':array([11,21,31]),
                    'attr4':array([14,24,34]),
                    },
                },
            }
        cache_creator = CreateTestAttributeCache()
        cache_creator.create_attribute_cache_with_data(self.temp_dir, test_data)
        
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['opus_core'],
                             in_storage=attribute_cache)
        
        # This should fail, since the set of primary attributes are different in the different years.
        self.assertRaises(AttributeError,
                          MultipleYearDatasetView,
                          name_of_dataset_to_merge = 'test',
                          in_table_name = 'tests',
                          attribute_cache = attribute_cache,
                          years_to_merge = years_to_merge,
                          )

        
if __name__ == '__main__':
    opus_unittest.main()