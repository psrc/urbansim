# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class young_household_in_mixed_use(Variable):
    """Indicator variable calculated by...
    [if development_type_groups includes (cell.development_type, 'mixed use') and hh.is_young then 1 else 0]"""
    
    gc_is_in_development_type_group_mixed_use = "is_in_development_type_group_mixed_use"
    hh_is_young = "is_young"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_is_in_development_type_group_mixed_use), 
                attribute_label("household", self.hh_is_young)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_is_in_development_type_group_mixed_use,
                                            self.hh_is_young)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.young_household_in_mixed_use"
    
    # TODO: this tests most of the tree, but not quite the full tree.  To
    # test the full tree, the grid cells should be given their 
    # DEVELOPMENT_TYPE_ID plain, rather than using 
    # is_in_development_type_group_mixed_use
    # Fix this (maybe low priority though, since if 
    # is_in_development_type_group_mixed_use is working
    # this is OK)
    def test_most_of_tree(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'is_in_development_type_group_mixed_use': array([0,1,1]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1,2,3,4,5,6]),
                'age_of_head': array([30,31,22,65,100,25]), # so [1,0,1,0,0,1] for is_young
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "young_age": array([30]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[0,1,1], 
                           [0,0,0], 
                           [0,1,1], 
                           [0,0,0], 
                           [0,0,0], 
                           [0,1,1]])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'is_in_development_type_group_mixed_use': array([0,1,1]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1,2,3,4,5,6]),
                'is_young': array([1,0,1,0,0,1])
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "young_age": array([30]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[0,1,1],
                           [0,0,0],
                           [0,1,1],
                           [0,0,0],
                           [0,0,0],
                           [0,1,1]])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()