# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_parcel.faz_x_land_use_type.total_value_per_sqft import total_value_per_sqft as faz_total_value_per_sqft

class total_value_per_sqft(faz_total_value_per_sqft):
    id_variable = "large_area_id = parcel.disaggregate(faz.large_area_id, intermediates=[zone])"

    
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
            "large_area":{ 
                 "large_area_id": arange(1,3)
                           }, 
             "land_use_type":{ 
                 "land_use_type_id":arange(1,6)
                              },
             "parcel":{
                 "parcel_id": arange(1,21),
                 "unit_price":       array([10,5,3,100,2,1,4,2,68,400,3,12,14,59,24,0,0,24,5,2.5]),
                "total_value_per_sqft": array([10,5,3,100,2,1,4,2,68,400,3,12,14,59,24,0,5,24,5,2.5]),
                 "land_use_type_id": array([1, 3,1, 5, 4,5,4,3,1,  1, 4,3, 1, 5, 5, 3,4, 1,1, 1]),
                 "large_area_id":    array([1, 2,2, 1, 2,1,1,1,1,  2, 2,1, 2, 1, 2, 2,1, 1,1, 2])
                       }
             })
        should_be = array([[array([10,68,24,5]).mean(), 0, array([2,12]).mean(), array([4,5]).mean(), array([100,1,59]).mean()],
                           [array([3,400,14,2.5]).mean(), 0, array([5]).mean(), array([2,3]).mean(), 24]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()