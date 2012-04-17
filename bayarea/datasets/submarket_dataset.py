# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
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
    subgroup_definition = ['bayarea.building.schooldistrict','bayarea.building.building_type', 'bayarea.building.tenure_id','bayarea.building.neighborhood_type']
    
from opus_core.tests import opus_unittest
class TestSubmarketDataset(opus_unittest.OpusTestCase):
    def test_input1(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='buildings',
                            table_data={
                                        'building_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
                                        'zone_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
                                        'building_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
                                        'tenure' :array([ 1,1, 2,2, 1,2, 1,1, 2, 2,2, 1]),
                                        }
                            ) 

        ds = SubmarketDataset(subgroup_definition=['building.zone_id'], in_storage=storage)
        
        self.assertEqual(ds.get_id_name(), ['submarket_id'])
        self.assertTrue( "zone_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["zone_id"], array([11,21,31]))
        self.assertEqual(ds.size(), 3)
        self.assertArraysEqual(ds.get_id_attribute(), array([11,21,31]))

    def test_input2(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='buildings',
                            table_data={
                                        'building_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
                                        'zone_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
                                        'building_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
                                        'tenure' :array([ 1,1, 2,2, 1,2, 1,1, 2, 2,2, 1]),
                                        }
                            ) 

        ds = DatasetFactory().get_dataset('submarket',
                                          package='bayarea',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(ds.get_id_name(), ['submarket_id'])
        self.assertTrue( "zone_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["zone_id"], array([11,11,11,21,21,21,31,31]))
        self.assertTrue( "building_type_id" in ds.get_known_attribute_names())
        self.assertArraysEqual( ds["building_type_id"], array([0,7,99,0,7,99,7,99]))
        self.assertEqual(ds.size(), 8)
        self.assertArraysEqual(ds.get_id_attribute(), array([11001, 
                                                             11071, 
                                                             11991, 
                                                             21002, 
                                                             21072, 
                                                             21992, 
                                                             31071, 
                                                             31992])
                                    )
        
        
if __name__ == '__main__':
    opus_unittest.main()
