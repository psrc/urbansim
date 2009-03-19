# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class cost_to_income_ratio(Variable):
    """ total_annual_rent /income""" 
    _return_type="float32"
    gc_total_annual_rent = "total_annual_rent"
    hh_income = "income"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_total_annual_rent), 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().divide(self.gc_total_annual_rent, self.hh_income)
#TODO: does "divide" automatically do float division?
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.cost_to_income_ratio"
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'total_annual_rent': array([1000, 10000, 100000]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3]),
                'income': array([1, 20, 500]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[1000, 10000, 100000], 
                           [50, 500, 5000 ], 
                           [2, 20, 200]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()