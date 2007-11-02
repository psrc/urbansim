#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 
from opus_core.variables.variable import Variable
from numpy import zeros, where
from scipy import ndimage

class total_value_per_sqft(Variable):
    def dependencies(self):
        return ["large_area_id = parcel.disaggregate(faz.large_area_id, intermediates=[zone])",
                "parcel.land_use_type_id",
                "urbansim_parcel.parcel.total_value_per_sqft"
                ]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        parcels = dataset_pool.get_dataset('parcel')
        up = parcels.get_attribute("total_value_per_sqft")
        la = parcels.get_attribute("large_area_id")
        lut = parcels.get_attribute("land_use_type_id")
        laids = ds.get_dataset(1).get_id_attribute()
        lutids = ds.get_dataset(2).get_id_attribute()
        result = zeros(ds.size()[0])
        for i in range(result.shape[0]): # iterate over large areas
            labels = where(la == laids[i], lut, 0)
            result[i,:] = ndimage.mean(up, labels=labels, index=lutids)
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
            "large_area":{ 
                 "large_area_id": arange(1,3)
                           }, 
             "land_use_type":{ 
                 "land_use_type_id":arange(1,6)
                              },
             "parcel":{
                 "parcel_id": arange(1,21),
                 "total_value_per_sqft":       array([10,5,3,100,2,1,4,2,68,400,3,12,14,59,24,0,0,24,5,2.5]),
                 "land_use_type_id": array([1, 3,1, 5, 4,5,4,3,1,  1, 4,3, 1, 5, 5, 3,4, 1,1, 1]),
                 "large_area_id":    array([1, 2,2, 1, 2,1,1,1,1,  2, 2,1, 2, 1, 2, 2,1, 1,1, 2])
                       }
             })
        should_be = array([[array([10,68,24,5]).mean(), 0, array([2,12]).mean(), array([4,0]).mean(), array([100,1,59]).mean()],
                           [array([3,400,14,2.5]).mean(), 0, array([5,0]).mean(), array([2,3]).mean(), 24]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()