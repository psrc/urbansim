# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_year_built(Variable):
    """ income * year_built"""
    _return_type="float32"
    parcel_year_built = "year_built"
    hh_income = "income"
    
    def dependencies(self):
        return ["parcel.year_built",
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        "year_built")


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_parcel.income_and_year_built"
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='parcels',
            table_data={
                'parcel_id':array([1,2,3,4]),
                'year_built':array([1990, 1950, 1921, 2000])
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'income':array([1000, 300000, 50000, 0, 10550])
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        household_x_parcel = dataset_pool.get_dataset('household_x_parcel')
        household_x_parcel.compute_variables(self.variable_name,
                                             dataset_pool=dataset_pool)
        values = household_x_parcel.get_attribute(self.variable_name)
            
        should_be = array([[1000*1990, 1000*1950, 1000*1921, 1000*2000], 
                           [300000*1990, 300000*1950, 300000*1921,300000*2000 ], 
                           [50000*1990, 50000*1950, 50000*1921,50000*2000], 
                           [0, 0, 0, 0], 
                           [10550*1990, 10550*1950, 10550*1921, 10550*2000]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()