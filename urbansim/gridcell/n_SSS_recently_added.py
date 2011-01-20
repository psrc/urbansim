# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class n_SSS_recently_added(Variable):

    _return_type="int32"

    def __init__(self, units):
        self.units = units
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.units)]

    def compute(self, dataset_pool):
        recent_years = dataset_pool.get_dataset('urbansim_constant')["recent_years"]

        self.get_dataset().compute_variables('urbansim.gridcell.%s_lag%s' % (self.units, recent_years+1)),
        results = self.get_dataset().get_attribute(self.units) - \
                  self.get_dataset().get_attribute("%s_lag%s" % (self.units, recent_years+1))

        return results

from opus_core.tests import opus_unittest
import tempfile
import os, shutil
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.store.attribute_cache import AttributeCache
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.n_industrial_sqft_recently_added"

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
                'grid_id': array([1,2,3,4]),
                'industrial_sqft': array([4,0,1,0]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 1998)
        dataset_pool.remove_all_datasets()

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'industrial_sqft': array([3,0,2,1]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 1999)
        dataset_pool.remove_all_datasets()

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'industrial_sqft': array([3,0,3,1]),
            }
        )
        gridcell = dataset_pool.get_dataset('gridcell')
        self._write_dataset_to_cache(gridcell, cache_dir, 2000)
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
        self.assert_(ma.allequal(values, array([0,0,1,0])))

    def test_recent_years_of_2(self):
        dataset_pool = self.prepare_dataset_pool(2)
        gridcell = dataset_pool.get_dataset('gridcell')

        gridcell.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        self.assert_(ma.allequal(values, array([-1,0,2,1])))

if __name__=='__main__':
    opus_unittest.main()