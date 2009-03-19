# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 
from opus_core.variables.variable import Variable
from numpy import zeros, where
from scipy import ndimage

class total_value_per_sqft(Variable):
    
    id_variable = "faz_id = parcel.disaggregate(zone.faz_id)"
    
    def dependencies(self):
        return [self.id_variable,
                "parcel.land_use_type_id",
                "urbansim_parcel.parcel.total_value_per_sqft",
                "urbansim_parcel.parcel.unit_price"
                ]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        parcels = dataset_pool.get_dataset('parcel')
        #up = parcels.get_attribute("total_value_per_sqft")
        up = parcels.get_attribute("unit_price")
        where_zero = where(up == 0)[0]
        up[where_zero] = parcels.get_attribute("total_value_per_sqft")[where_zero]
        where_positive = where(up > 0)[0]
        faz = parcels.get_attribute(self.id_variable)
        lut = parcels.get_attribute("land_use_type_id")
        fazids = ds.get_dataset(1).get_id_attribute()
        lutids = ds.get_dataset(2).get_id_attribute()
        result = zeros(ds.size()[0])
        for i in range(result.shape[0]): # iterate over large areas
            labels = where(faz == fazids[i], lut, 0)
            result[i,:] = ndimage.mean(up[where_positive], labels=labels[where_positive], index=lutids)
        return result
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import arange, array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "faz":{ 
                 "faz_id": arange(1,3)
                           }, 
             "land_use_type":{ 
                 "land_use_type_id":arange(1,6)
                              },
             "parcel":{
                 "parcel_id": arange(1,21),
                 "unit_price":       array([10,5,3,100,2,1,4,2,68,400,3,12,14,59,24,0,0,24,5,2.5]),
             "total_value_per_sqft": array([10,5,3,100,2,1,4,2,68,400,3,12,14,59,24,20,0,24,5,2.5]),
                 "land_use_type_id": array([1, 3,1, 5, 4,5,4,3,1,  1, 4,3, 1, 5, 5, 3,4, 1,1, 1]),
                 "faz_id":           array([1, 2,2, 1, 2,1,1,1,1,  2, 2,1, 2, 1, 2, 2,1, 1,1, 2])
                       }
             })
        should_be = array([[array([10,68,24,5]).mean(), 0, array([2,12]).mean(), 4, array([100,1,59]).mean()],
                           [array([3,400,14,2.5]).mean(), 0, array([5, 20]).mean(), array([2,3]).mean(), 24]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()