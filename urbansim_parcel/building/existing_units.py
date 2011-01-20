# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import zeros, logical_not
from opus_core.misc import unique

class existing_units(Variable):
    """total number of units (residential_units or sqft, depending whether the building is_residential or not) """
    _return_type = "int32"
    
    def dependencies(self):
        return [
                "urbansim_parcel.building.building_sqft",
                "urbansim_parcel.building.residential_units",
                "urbansim_parcel.building.is_residential"
                ]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        result = zeros(buildings.size(),dtype=self._return_type)
        is_res = buildings.get_attribute("is_residential")>0
        is_sqft = logical_not(is_res)
        residential_units = buildings.get_attribute("residential_units")
        result[is_res] = residential_units[is_res].astype(self._return_type)
        result[is_sqft] = buildings.get_attribute("building_sqft")[is_sqft].astype(self._return_type)
        return result
    
    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
            
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'building':
            {
                'building_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'residential_units':    array([0,   2,   3,   0,   2,   3,  4, 1, 0, 5]),
                'sqft_per_unit':        array([0,   2,   2,   0,   10,  5,  2,20, 0, 20]),
                'non_residential_sqft': array([19,  0, 310, 400,   0, 223, 58, 0, 0, 0]),
                'is_residential':       array([0,   1,   0,   0,   1,  0,   0, 1, 1, 1], dtype="bool8")
                },           
        }
        )
        
        should_be = array([19, 2, 316, 400, 2, 223+15, 8+58, 1, 0, 5])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    
