# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from numpy import newaxis

class parcel_SSS_multiply_SSS_household_SSS(Variable):
    """SSS (the first SSS) variable in psrc.parcel multiplies household variable SSS (the third SSS) defined in package SSS (the second SSS)"""    

    default_value = 180.0
    def __init__(self, parcel_var, package_name, household_var):
        self.parcel_var = parcel_var
        self.package = package_name
        self.household_var = household_var
        Variable.__init__(self)

    def dependencies(self):
        return ["urbansim.parcel." + self.parcel_var,
                "%s.household.%s" % (self.package, self.household_var)]

    def compute(self, dataset_pool):
        household_x_parcels = self.get_dataset()
        return household_x_parcels.get_attribute_of_dataset(self.household_var)[:, newaxis] * \
               household_x_parcels.get_2d_dataset_attribute(self.parcel_var)
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_parcel.parcel_built_sf_multiply_urbansim_household_is_high_income"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='parcels',
            table_data={
                'parcel_id':array([1,2,3,4]),
                'built_sf':array([50, 50, 75, 10])
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'is_high_income':array([1, 0, 1, 0, 1])
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        household_x_parcel = dataset_pool.get_dataset('household_x_parcel')
        household_x_parcel.compute_variables(self.variable_name,
                                             dataset_pool=dataset_pool)
        values = household_x_parcel.get_attribute(self.variable_name)
            
        should_be = array([[50, 50, 75, 10], 
                           [0, 0, 0, 0], 
                           [50, 50, 75, 10], 
                           [0, 0, 0, 0],
                           [50, 50, 75, 10]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()