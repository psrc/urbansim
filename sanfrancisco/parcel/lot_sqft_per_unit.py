# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class lot_sqft_per_unit(Variable):
    """ (lot_sqft) / residential_units."""
    
    _return_type="float32"
    
    def dependencies(self):
        return ["_lot_sqft_per_unit = parcel.lot_sf / parcel.residential_units"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_lot_sqft_per_unit")

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
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'parcel':{
                     "parcel_id":array([1,2,3,4,5]),
                     "residential_units":array([2,0,1,4,7]),
                     "lot_sf":array([1000,3000,2000,1005,7000]),             
                     }
            }
        )
        
        should_be = array([500, 0, 2000, 251, 1000])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
