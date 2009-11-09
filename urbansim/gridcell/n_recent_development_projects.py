# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros

class n_recent_development_projects(Variable):
    """Number of development projects per each gridcell has experienced in the last
    N years, where N is the values of the recent_years field of the
    uransim_constants table.
    """

    _return_type="int32"

    def dependencies(self):
        return []

    def compute(self, dataset_pool):
        results = zeros(self.get_dataset().size())
        recent_years = dataset_pool.get_dataset('urbansim_constant')["recent_years"]
        units = ["residential_units", "commercial_sqft", "industrial_sqft", "governmental_sqft"]
        # TODO: if both commercial_sqft and industrial_sqft increase in one year, should that
        # count for 1 or 2 development events?
        for i in range(recent_years):
            for unit in units:
                var_name_for_this_year = 'urbansim.gridcell.%s_lag%d' % (unit, i+1)
                var_name_for_prior_year = 'urbansim.gridcell.%s_lag%d' % (unit, i+2)
                self.get_dataset().compute_variables([var_name_for_prior_year, var_name_for_this_year])
                results += (self.get_dataset().get_attribute(var_name_for_this_year) >
                                                 self.get_dataset().get_attribute(var_name_for_prior_year))

        return results

from opus_core.tests import opus_unittest
import tempfile
import os
import shutil

from numpy import array
from numpy import ma

from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.n_recent_development_projects"

    def _write_dataset_to_cache(self, dataset, cache_dir, year):
        # save to flt file with this year.
        SimulationState().set_current_time(year)
        year_dir = os.path.join(cache_dir, str(year))
        flt_storage = StorageFactory().get_storage('flt_storage', subdir='store',
            storage_location=year_dir)
        dataset.write_dataset(out_storage=flt_storage,
                              out_table_name='gridcells')

    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def prepare_dataset_pool(self, recent_years):
        cache_dir = os.path.join(self.urbansim_tmp, 'urbansim_cache')
        SimulationState().set_cache_directory(cache_dir)

        storage = StorageFactory().get_storage('dict_storage')
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id':array([1,2,3,4]),
                'residential_units':array([1,0,5,0]),
                'commercial_sqft':array([0,20,7,0]),
                'industrial_sqft':array([0,0,0,10]),
                'governmental_sqft':array([0,0,0,10]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 1998)
        dataset_pool.remove_all_datasets()

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id':array([1,2,3,4]),
                'residential_units':array([1,0,6,0]),
                'commercial_sqft':array([10,20,10,0]),
                'industrial_sqft':array([0,0,0,10]),
                'governmental_sqft':array([0,0,0,10]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 1999)
        dataset_pool.remove_all_datasets()

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id':array([1,2,3,4]),
                'residential_units':array([1,0,6,0]),
                'commercial_sqft':array([10,20,10,0]),
                'industrial_sqft':array([0,0,5,11]),
                'governmental_sqft':array([0,0,0,11]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 2000)
        dataset_pool.remove_all_datasets()

        # For 2001, make sure every gridcell has changed in every way,
        # since this data should *not* be used by this variable.
        storage.write_table(
            table_name='gridcells',
            table_data={
            'grid_id':array([1,2,3,4]),
            'residential_units':gridcell.get_attribute('residential_units') + 1,
            'commercial_sqft':gridcell.get_attribute('commercial_sqft') + 1,
            'industrial_sqft':gridcell.get_attribute('industrial_sqft') + 1,
            'governmental_sqft':gridcell.get_attribute('governmental_sqft') + 1,
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 2001)
        dataset_pool.remove_all_datasets()

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

    def test_recent_years_of_1(self):
        dataset_pool = self.prepare_dataset_pool(1)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assert_(ma.allequal(values, array([0,0,1,2])))

    def test_recent_years_of_2(self):
        dataset_pool = self.prepare_dataset_pool(2)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assert_(ma.allequal(values, array([1,0,3,2])))

if __name__=='__main__':
    opus_unittest.main()