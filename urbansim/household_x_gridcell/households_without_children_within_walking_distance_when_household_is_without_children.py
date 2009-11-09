# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class households_without_children_within_walking_distance_when_household_is_without_children(Variable):
    """Number of households without children within walking distance that are without children,
    given that the household is without children.
    (If the household has children the corresponding value is 0.)"""
    
    gc_households_without_children_within_walking_distance = \
      "households_without_children_within_walking_distance"
    hh_is_without_children = "is_without_children"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_households_without_children_within_walking_distance), 
                attribute_label("household", self.hh_is_without_children)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                                self.gc_households_without_children_within_walking_distance,
                                                self.hh_is_without_children, 0)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.households_without_children_within_walking_distance_when_household_is_without_children"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'households_without_children_within_walking_distance': array([5, 0, 42]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'is_without_children': array([0, 1, 1, 0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[0,0,0], 
                           [5,0,42], 
                           [5,0,42], 
                           [0,0,0]])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()