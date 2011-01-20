# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose

class DistrictCommuteDataset(UrbansimDataset):
    
    id_name_default = 'commute_id'   ##["origin_district_id", "destination_district_id"]
    in_table_name_default = "district_commutes"
    out_table_name_default = "district_commutes"
    dataset_name = "district_commute"
    
    def __init__(self, **kwargs):
        districts = self._try_load_district_dataset(**kwargs)
        if districts is not None:
            district_ids = districts.get_id_attribute()
            OD_array = array( [[x, y]  for x in district_ids for y in district_ids] )

            storage = StorageFactory().get_storage('dict_storage')
        
            storage.write_table(table_name=self.in_table_name_default,
                                table_data={
                                            'commute_id'     :OD_array[:,0] * 1000 + OD_array[:,1],
                                            'origin_district_id'     :OD_array[:,0],
                                            'destination_district_id':OD_array[:,1],
                                            }
                                ) 
        
            UrbansimDataset.__init__(self, in_storage=storage, 
                                     #in_table_name=self.in_table_name_default, 
                                     #id_name=self.id_name_default, 
                                     #dataset_name=self.dataset_name
                                 )
        else:
            UrbansimDataset.__init__(self, **kwargs)
        
    def _try_load_district_dataset(self, **kwargs):
        try:
            districts = DatasetFactory().get_dataset("district", 
                                                     package='psrc_parcel',
                                                     arguments=kwargs)
            districts.load_dataset()
        except:
            districts = None
        return districts


from opus_core.tests import opus_unittest
class DistrictCommuteDatasetTests(opus_unittest.OpusTestCase):
    def test_input(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='districts',
                            table_data={
                                        'district_id'     :array([1,3,4]),
                                        }
                            ) 
        
        dc = DatasetFactory().get_dataset('district_commute',
                                          package='psrc_parcel',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(dc.get_id_name(), ['commute_id'])
        self.assertTrue( "origin_district_id" in dc.get_known_attribute_names())
        self.assertTrue( "destination_district_id" in dc.get_known_attribute_names())        
        self.assertEqual(dc.size(), 9)
        self.assertTrue(allclose(dc.get_id_attribute(), array([1001,
                                                       1003,
                                                       1004,
                                                       3001,
                                                       3003,
                                                       3004,
                                                       4001,
                                                       4003,
                                                       4004])
                                    ))
        
        
if __name__ == '__main__':
    opus_unittest.main()