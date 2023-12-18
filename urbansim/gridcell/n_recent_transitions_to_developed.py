# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class n_recent_transitions_to_developed(Variable):
    """Returns number of times each gridcell transitions from un-developed to developed.
    """

    _return_type="int32"

    def dependencies(self):
        return []

    def compute(self, dataset_pool):
        results = zeros(self.get_dataset().size())
        recent_years = dataset_pool.get_dataset('urbansim_constant')["recent_years"]
        for i in range(recent_years):
            var_name_for_this_year = 'urbansim.gridcell.is_in_development_type_group_developed_lag%d' % (i+1)
            var_name_for_prior_year = 'urbansim.gridcell.is_in_development_type_group_developed_lag%d' % (i+2)

            self.get_dataset().compute_variables([var_name_for_prior_year, var_name_for_this_year])
            results += logical_and(1 - self.get_dataset().get_attribute(var_name_for_prior_year),
                                   # inverse is_in_development_type_group_developed to get undeveloped
                                   self.get_dataset().get_attribute(var_name_for_this_year))

        return results

from opus_core.tests import opus_unittest
import tempfile
import os, shutil
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.store.attribute_cache import AttributeCache
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.n_recent_transitions_to_developed"

    def _write_dataset_to_cache(self, dataset, cache_dir, year):
        # save to flt file with this year.
        SimulationState().set_current_time(year)
        year_dir = os.path.join(self.cache_dir, str(year))
        flt_storage = StorageFactory().get_storage('flt_storage', subdir='store',
                                                   storage_location=year_dir)
        dataset.write_dataset(out_storage=flt_storage,
                              out_table_name='gridcells')

    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def prepare_dataset_pool(self, recent_years):
        self.cache_dir = os.path.join(self.urbansim_tmp, 'urbansim_cache')
        SimulationState().set_cache_directory(self.cache_dir)

        data = {
            1997:{
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([0,0,0,0]),
                },
            1998:{
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([0,1,0,0]),
            },
            1999:{
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([0,0,1,0])
            },
            2000:{
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([1,1,1,0])
            },
            2001:{
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([1,1,1,0])+1
            }
        }
        self.write_gridcell_data_to_cache(data)

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                'recent_years': array([recent_years]),
            }
        )

        SimulationState().set_current_time(2001)
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             package_order=['urbansim'],
                             in_storage=attribute_cache)
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=attribute_cache)

        # Can't write urbansim_constant, so directly add it to the pool.
        temp_dataset_pool = DatasetPool(package_order=['urbansim'],
                                        storage=storage)
        dataset_pool._add_dataset('urbansim_constant',
                                  temp_dataset_pool.get_dataset('urbansim_constant'))
        return dataset_pool

    def write_gridcell_data_to_cache(self, data_by_year):
        """Write all of this data to the gridcells for each year in data_by_year."""
        for year, data in data_by_year.items():
            self.write_gridcell_data_for_year(data, year)

    def write_gridcell_data_for_year(self, data, year):
        storage = StorageFactory().get_storage('dict_storage')
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        storage.write_table(table_name='gridcells', table_data=data)
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, self.cache_dir, year)

    def test_for_recent_years_of_1_with_2001_changes(self):
        dataset_pool = self.prepare_dataset_pool(1)
        self.write_gridcell_data_for_year(
            {
                'grid_id':array([1,2,3,4]),
                'is_in_development_type_group_developed':array([1,1,1,1]),
            },
            2001)

        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assertTrue(ma.allequal(values, array([1,1,0,0])))

    def test_for_recent_years_of_1(self):
        dataset_pool = self.prepare_dataset_pool(1)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assertTrue(ma.allequal(values, array([1,1,0,0])))

    def test_for_recent_years_of_2(self):
        dataset_pool = self.prepare_dataset_pool(2)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assertTrue(ma.allequal(values, array([1,1,1,0])))

    def test_for_recent_years_of_3(self):
        dataset_pool = self.prepare_dataset_pool(3)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assertTrue(ma.allequal(values, array([1,2,1,0])))

if __name__=='__main__':
    opus_unittest.main()