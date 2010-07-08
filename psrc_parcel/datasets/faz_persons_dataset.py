# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose
from opus_core.misc import unique

class FazPersonsDataset(UrbansimDataset):
    
    id_name_default = 'dummy_id'
    in_table_name_default = "faz_persons"
    out_table_name_default = "faz_persons"
    dataset_name = "faz_persons"
    
    def __init__(self, **kwargs):
        fazes, households = self._try_load_datasets(**kwargs)
        if fazes is not None:
            faz_id = fazes.get_id_attribute()
            persons = unique( households.get_attribute("persons") )
            combine_array = array( [[x, y]  for x in faz_id for y in persons] )
            storage = StorageFactory().get_storage('dict_storage')        
            storage.write_table(table_name=self.in_table_name_default,
                                table_data={
                                            'dummy_id'   :combine_array[:, 0] * 100 + combine_array[:,1],
                                            'faz_id'     :combine_array[:, 0],
                                            'persons'    :combine_array[:, 1],
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
            households = DatasetFactory().get_dataset("household", 
                                                     package='urbansim',
                                                     arguments=kwargs)

            fazes.load_dataset()
            households.load_dataset(attributes='*')
        except:
            fazes = None
            households = None
        return (fazes, households)


from opus_core.tests import opus_unittest
class DistrictCommuteDatasetTests(opus_unittest.OpusTestCase):
    def test_input(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='fazes',
                            table_data={
                                        'faz_id'     :array([1,3,4]),
                                        }
                            ) 
        storage.write_table(table_name='households',
                            table_data={
                                        'household_id'  :array([1,2,3]),
                                        'persons'       :array([1,3,4]),
                                        }
                            )         

        dc = DatasetFactory().get_dataset('faz_persons',
                                          package='psrc_parcel',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(dc.get_id_name(), ['dummy_id'])
        self.assertTrue( "faz_id" in dc.get_known_attribute_names())
        self.assertTrue( "persons" in dc.get_known_attribute_names())        
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