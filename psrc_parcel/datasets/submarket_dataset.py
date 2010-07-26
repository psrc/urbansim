# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose, column_stack
from opus_core.misc import unique, digits
from opus_core.variables.variable_name import VariableName

class SubmarketDataset(UrbansimDataset):
    
    id_name_default = 'submarket_id'
    in_table_name_default = "submarket"
    out_table_name_default = "submarket"
    dataset_name = "submarket"
    submarket_definition = ['parcel.large_area_id', 'parcel.land_use_type_id']
    
    def __init__(self, submarket_definition=[], **kwargs):
        if submarket_definition:
            self.submarket_definition = submarket_definition
            
        dataset, short_names, submarket_ids = self.solve_dependencies(**kwargs)
        table_data = {}
            
        table_data['submarket_id'], unique_index = unique( submarket_ids, return_index=True )
        
        table_data.update([(short_name, dataset[short_name][unique_index]) for short_name in short_names])

        storage = StorageFactory().get_storage('dict_storage')        
        storage.write_table(table_name=self.in_table_name_default,
                            table_data=table_data
                            ) 
    
        UrbansimDataset.__init__(self, in_storage=storage, 
                                 #in_table_name=self.in_table_name_default, 
                                 #id_name=self.id_name_default, 
                                 #dataset_name=self.dataset_name
                             )
        
    def solve_dependencies(self, **kwargs):
        variable_names = [VariableName(v) for v in self.submarket_definition]
        ds = [vn.get_dataset_name() for vn in variable_names]
        short_names = [vn.get_alias() for vn in variable_names]
        assert len(set(ds))==1  ## the submarket_definition should be of the same dataset

        dataset = DatasetFactory().get_dataset(ds[0], 
                                               package='urbansim_parcel',
                                               arguments=kwargs)
        dataset.compute_variables(self.submarket_definition)
        
        submarket_ids = generate_unique_ids(dataset, short_names)
        return (dataset, short_names, submarket_ids)
    
def generate_unique_ids(dataset, short_names):
    if len(short_names) == 0:
        raise ValueError, "There must have at least 1 attribute."
    elif len(short_names) == 1:
        submarket_ids = dataset[short_names[0]]
    else:
        attribute_values = column_stack( [dataset.get_attribute_as_column(short_name) for short_name in short_names] )
        max_digits = digits( attribute_values.max(axis=0) )
        multipler = array([10**d for d in max_digits[1:] + [0]])
        submarket_ids = (attribute_values * multipler).sum(axis=1)
        
    return submarket_ids

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

        ds = SubmarketDataset(submarket_definition=['parcel.large_area_id'], in_storage=storage)
        
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