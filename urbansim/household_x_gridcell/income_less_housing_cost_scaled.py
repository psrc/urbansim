# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import reshape

class income_less_housing_cost_scaled(Variable):
    """ (income - housing_cost) / 10000 where income > housing_cost""" 
    housing_cost = "housing_cost"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.housing_cost), 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        attr1 = reshape(self.get_dataset().get_attribute_of_dataset(self.hh_income),
                             (self.get_dataset().get_reduced_n(), 1))
#        return where(attr1 > self.get_dataset().get_2d_dataset_attribute(self.housing_cost),
#        ((attr1 - self.get_dataset().get_2d_dataset_attribute(self.housing_cost))/10000),0)
        return (attr1 - self.get_dataset().get_2d_dataset_attribute(self.housing_cost))/10000
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.income_less_housing_cost_scaled"
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'housing_cost': array([10000, 20000, 100000]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3]),
                'income': array([10000, 20000, 500000]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[0, -1, -9], 
                           [1, 0, -8], 
                           [49, 48, 40]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()