# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_is_in_city_SSS(Variable):
    """ income * is_in_city_SSS"""
    _return_type="float32"
    
    def __init__(self, city):
        self.is_in_city = "is_in_city_%s" % city
        self.hh_income = "income"
        
        Variable.__init__(self)
    
    def dependencies(self):
        return ["psrc.parcel.%s" % self.is_in_city,
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        self.is_in_city)


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_parcel.income_and_is_in_city_seattle"
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='parcels',
            table_data={
                'parcel_id':array([1,2,3,4]),
                'is_in_city_seattle':array([1, 1, 0, 0])
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
            
        should_be = array([[1000*1, 1000*1, 1000*0, 1000*0], 
                           [300000*1, 300000*1, 300000*0,300000*0 ], 
                           [50000*1, 50000*1, 50000*0,50000*0], 
                           [0, 0, 0, 0], 
                           [10550*1, 10550*1, 10550*0, 10550*0]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()