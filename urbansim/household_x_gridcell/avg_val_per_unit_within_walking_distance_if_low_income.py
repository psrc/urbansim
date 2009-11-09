# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class avg_val_per_unit_within_walking_distance_if_low_income(Variable):
    """avg_val_per_unit within the walking radius, given that the decision-making household is low-income.
    """    
    
    gc_variable = "residential_avg_val_per_unit_within_walking_distance"
    hh_is_income = "is_low_income"
        
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_variable), 
                attribute_label("household", self.hh_is_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_variable,
                                            self.hh_is_income)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.avg_val_per_unit_within_walking_distance_if_low_income"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'residential_avg_val_per_unit_within_walking_distance': array([50, 10, 20]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'is_low_income': array([1, 0, 1, 0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[50, 10, 20], 
                           [0, 0, 0 ], 
                           [50, 10, 20], 
                           [0,0,0]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()