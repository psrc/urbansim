# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class percent_low_income_households_within_walking_distance_if_low_income(Variable):
    """Percent of households within the walking radius that are designated as low-income, given that 
    the decision-making household is low-income.
    [percent_low_income_households_within_walking_distance if hh.is_low_income is true else 0]"""    
    
    gc_percent_low_income_households_within_walking_distance = \
      "percent_low_income_households_within_walking_distance"
    hh_is_low_income = "is_low_income"
        
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_percent_low_income_households_within_walking_distance), 
                attribute_label("household", self.hh_is_low_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_percent_low_income_households_within_walking_distance,
                                            self.hh_is_low_income)        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.percent_low_income_households_within_walking_distance_if_low_income"
    
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4, 5, 6]),
                'grid_id': array([1, 2, 3, 4, 2, 2]),
                'income': array([1500, 5000, 3000, 10000, 1000, 8000]) # low income: <= 1500
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
                'low_income_fraction': array([.25]),
                'mid_income_fraction': array([.3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[57.14286, 36.36364, 20, 14.28571], 
                           [0,0,0,0], 
                           [0,0,0,0], 
                           [0,0,0,0], 
                           [57.14286, 36.36364, 20, 14.28571], 
                           [0,0,0,0]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-5), 
                     msg="Error in " + self.variable_name)
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'percent_low_income_households_within_walking_distance': array([50, 0, 15]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'is_low_income': array([1, 0, 1, 1]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
                'low_income_fraction': array([.25]),
                'mid_income_fraction': array([.3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[50, 0, 15], 
                           [0, 0, 0], 
                           [50, 0, 15], 
                           [50, 0, 15]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()