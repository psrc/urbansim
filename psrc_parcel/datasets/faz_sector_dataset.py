# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose

class FazSectorDataset(UrbansimDataset):
    
    id_name_default = 'dummy_id'
    in_table_name_default = "faz_sectors"
    out_table_name_default = "faz_sectors"
    dataset_name = "faz_sector"
    
    def __init__(self, **kwargs):
        fazes, sectors = self._try_load_datasets(**kwargs)
        if fazes is not None:
            faz_id = fazes.get_id_attribute()
            sector_id = sectors.get_id_attribute()
            combine_array = array( [[x, y]  for x in faz_id for y in sector_id] )
            storage = StorageFactory().get_storage('dict_storage')        
            storage.write_table(table_name=self.in_table_name_default,
                                table_data={
                                            'dummy_id'   :combine_array[:, 0] * 100 + combine_array[:,1],
                                            'faz_id'     :combine_array[:, 0],
                                            'sector_id'  :combine_array[:, 1],
                                            }
                                ) 
        
            UrbansimDataset.__init__(self, in_storage=storage, 
                                     #in_table_name=self.in_table_name_default, 
                                     #id_name=self.id_name_default, 
                                     #dataset_name=self.dataset_name
                                 )
        else:
            UrbansimDataset.__init__(self, **kwargs)
        
    def _try_load_datasets(self, **kwargs):
        try:
            fazes = DatasetFactory().get_dataset("faz", 
                                                     package='urbansim',
                                                     arguments=kwargs)
            sectors = DatasetFactory().get_dataset("employment_sector", 
                                                     package='urbansim',
                                                     arguments=kwargs)

            fazes.load_dataset()
            sectors.load_dataset(attributes='*')
        except:
            fazes = None
            sectors = None
        return (fazes, sectors)


from opus_core.tests import opus_unittest
class DistrictCommuteDatasetTests(opus_unittest.OpusTestCase):
    def test_input(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='fazes',
                            table_data={
                                        'faz_id'     :array([1,3,4]),
                                        }
                            ) 
        storage.write_table(table_name='employment_sectors',
                            table_data={
                                        'sector_id'  :array([1,3,4]),
                                        }
                            )         
        storage.write_table(table_name='employment_adhoc_sector_group_definitions',
                            table_data={
                                        'sector_id'  :array([]),
                                        'group_id'   :array([]) 
                                        }
                            )         

        dc = DatasetFactory().get_dataset('faz_sector',
                                          package='psrc_parcel',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(dc.get_id_name(), ['dummy_id'])
        self.assertTrue( "faz_id" in dc.get_known_attribute_names())
        self.assertTrue( "sector_id" in dc.get_known_attribute_names())        
        self.assertEqual(dc.size(), 9)
        self.assertTrue(allclose(dc.get_id_attribute(), array([
                                                       101,
                                                       103,
                                                       104,
                                                       301,
                                                       303,
                                                       304,
                                                       401,
                                                       403,
                                                       404])
                                    ))
        
        
if __name__ == '__main__':
    opus_unittest.main()