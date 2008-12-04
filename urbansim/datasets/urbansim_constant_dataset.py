#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from numpy import array
from opus_core.datasets.dataset import Dataset
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from urbansim.constants import Constants
from urbansim.data.test_cache_configuration import TestCacheConfiguration

class UrbansimConstantDataset(Dataset):

    def __init__(self, **kwargs):
        self.constants_dict = Constants(**kwargs)
        data = {}
        for attr, value in self.constants_dict.iteritems():
            new_value = array([value])
            if new_value.size == 1:
                data[attr] = new_value
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'urbansim_constants', # whatever name
                        table_data = data)
        Dataset.__init__(self, in_storage = storage, 
                           in_table_name='urbansim_constants',
                           id_name = [], dataset_name='urbansim_constant')
        
    def summary(self, output=logger):
        output.write("UrbanSim constant dataset")

    def __getitem__(self, name):
        if name in self.get_known_attribute_names():
            return self.get_attribute(name)[0]
        return self.constants_dict[name]
    
    def get_income_range_for_type(self, income_type):
        return self.constants_dict.get_income_range_for_type(income_type)
        
import os
from opus_core.tests import opus_unittest
from opus_core.opus_package_info import package
from opus_core.datasets.dataset_pool import DatasetPool

from numpy import array, isscalar

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.config = TestCacheConfiguration()

        opus_core_path = package().get_opus_core_path()
        cache_dir = os.path.join(opus_core_path, 'data', 'test_cache')

        SimulationState(new_instance=True).set_current_time(
            self.config['base_year'])
        SimulationState().set_cache_directory(cache_dir)
        SessionConfiguration(self.config, new_instance=True,
                             package_order=['urbansim', 'opus_core'],
                             in_storage=AttributeCache())

    def test(self):
        urbansim_constant = UrbansimConstantDataset(in_storage=AttributeCache())
        self.assertEqual(urbansim_constant['absolute_max_year'], 3000)
        self.assertAlmostEqual(urbansim_constant['acres'], 150*150*0.0002471, 6)
        self.assert_(urbansim_constant["walking_distance_footprint"].ndim == 2)
        
    def testLoadTable(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name = 'urbansim_constants',
            table_data = {
                'young_age':array([30,])
            }
        )
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        self.assert_('young_age' in urbansim_constant.get_primary_attribute_names(), msg = "Some constants are missing.")
        self.assert_(urbansim_constant['young_age']==30, msg = "Wrong constant value.")
        self.assert_(isscalar(urbansim_constant['young_age']), msg = "Constant  is an array.")
        
    def test_expression(self):
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=AttributeCache())
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name='dataset',
            table_data={
                "id":array([1,2,3,4]), 
                "year":array([1968,1989,1750,0]) # absolute_min_year = 1800
                }
            )
        
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name="id")
        # This does not work but should
        #result = ds.compute_variables(['is_correct_year = dataset.year >= urbansim_constant.absolute_min_year'], dataset_pool=dataset_pool)
        #self.assertEqual(ma.allequal(result, array([1,1,0,0])), True)
        
if __name__ == '__main__':
    opus_unittest.main()
