# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from numpy import array, allclose, column_stack, cumsum, concatenate
from opus_core.misc import unique, digits
from opus_core.variables.variable_name import VariableName

class SubgroupDataset(UrbansimDataset):
    """
    create a subgroup dataset based on finer-grain dataset, the definition of
    subgroup can be defined with the class attribute subgroup_definition or through
    argument subgroup_definition of __init__ method.  For example, submarkets defined
    on parcels by large_area_id and land_use_type_id. See unittests for details.
    """
    
    id_name_default = 'subgroup_id'
    in_table_name_default = "subgroup"
    out_table_name_default = "subgroup"
    dataset_name = "subgroup"
    default_package_order = ['urbansim', 'opus_core']
    subgroup_definition = ['parcel.large_area_id', 'parcel.land_use_type_id']
    
    def __init__(self, subgroup_definition=[], **kwargs):
        if subgroup_definition:
            self.subgroup_definition = subgroup_definition
            
        dataset, short_names, subgroup_ids = self.solve_dependencies(**kwargs)
        table_data = {}
            
        table_data[self.id_name_default], unique_index = unique( subgroup_ids, return_index=True )
        
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
        variable_names = [VariableName(v) for v in self.subgroup_definition]
        ds = [vn.get_dataset_name() for vn in variable_names]
        short_names = [vn.get_alias() for vn in variable_names]
        assert len(set(ds))==1  ## the subgroup_definition should be of the same dataset

        dataset = DatasetFactory().search_for_dataset(ds[0], 
                                                      package_order=self.default_package_order,
                                                      arguments=kwargs)
        dataset.compute_variables(self.subgroup_definition)
        
        subgroup_ids, multipler = generate_unique_ids(dataset, short_names)
        self.multipler = multipler
        return (dataset, short_names, subgroup_ids)
    
def generate_unique_ids(dataset, short_names, multipler=[]):
    if len(short_names) == 0:
        raise ValueError, "There must have at least 1 attribute."
    elif len(short_names) == 1:
        subgroup_ids = dataset[short_names[0]]
    else:
        attribute_values = dataset.get_multiple_attributes(short_names)
        if not multipler:
            max_digits = digits( attribute_values[:,1:].max(axis=0) )
            tot_digits = concatenate( (cumsum(max_digits[::-1])[::-1], [0]) )
            multipler = 10**tot_digits
        subgroup_ids = (attribute_values * multipler).sum(axis=1)
    return subgroup_ids, multipler

from opus_core.tests import opus_unittest
class TestSubgroupDataset(opus_unittest.OpusTestCase):
    def test_input1(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(table_name='parcels',
                            table_data={
                                        'parcel_id'        :array([ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12]),
                                        'large_area_id'    :array([11,11,21,21,31,31,11,11,21,21,31,31]),
                                        'land_use_type_id' :array([ 7,99, 7,99, 7,99, 0,99, 0, 7,99, 7]),
                                        }
                            ) 

        ds = SubgroupDataset(subgroup_definition=['parcel.large_area_id'], in_storage=storage)
        
        self.assertEqual(ds.get_id_name(), ['subgroup_id'])
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

        ds = DatasetFactory().get_dataset('subgroup',
                                          package='urbansim',
                                          arguments={'in_storage':storage}
                                          )
        
        self.assertEqual(ds.get_id_name(), ['subgroup_id'])
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