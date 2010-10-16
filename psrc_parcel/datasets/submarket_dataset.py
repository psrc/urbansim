# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.subgroup_dataset import SubgroupDataset, generate_unique_ids
from numpy import array, allclose 

class SubmarketDataset(SubgroupDataset):
    
    id_name_default = 'submarket_id'
    in_table_name_default = "submarket"
    out_table_name_default = "submarket"
    dataset_name = "submarket"
    subgroup_definition = ['parcel.large_area_id', 'parcel.land_use_type_id']
    
from opus_core.tests import opus_unittest
class TestSubmarketDataset(opus_unittest.OpusTestCase):
    def test_input1(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='parcels',
                            table_data={
                                        'parcel_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
                                        'large_area_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
                                        'land_use_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
                                        }
                            ) 

        ds = SubmarketDataset(subgroup_definition=['parcel.large_area_id'], in_storage=storage)
        
        self.assertEqual(ds.get_id_name(), ['submarket_id'])
        self.assertTrue( "large_area_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["large_area_id"], array([11,21,31]))
        self.assertEqual(ds.size(), 3)
        self.assertArraysEqual(ds.get_id_attribute(), array([11,21,31]))

    def test_input2(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='parcels',
                            table_data={
                                        'parcel_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
                                        'large_area_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
                                        'land_use_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
                                        }
                            ) 

        ds = DatasetFactory().get_dataset('submarket',
                                          package='psrc_parcel',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(ds.get_id_name(), ['submarket_id'])
        self.assertTrue( "large_area_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["large_area_id"], array([11,11,11,21,21,21,31,31]))
        self.assertTrue( "land_use_type_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["land_use_type_id"], array([0,7,99,0,7,99,7,99]))
        self.assertEqual(ds.size(), 8)
        self.assertArraysEqual(ds.get_id_attribute(), array([
                                                       1100,
                                                       1107,
                                                       1199,
                                                       2100,
                                                       2107,
                                                       2199,
                                                       3107,
                                                       3199])
                                    )
        
        
if __name__ == '__main__':
    opus_unittest.main()