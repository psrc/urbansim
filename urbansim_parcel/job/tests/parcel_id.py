# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

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
                "job":{
                    "job_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "building_id":array([1, 2, 2, 2, 3, 3, 4, 5]),
                    },
                "building":{
                    "building_id":array([1,2,3,4,5]),
                    "parcel_id":  array([1,1,2,3,4])
                    },
                "parcel":{
                     "parcel_id":array([1,2,3,4]),
                     "zone_id":  array([1,3,2,2]),
                     "parcel_sqft":array([0.1, 0.2, 0.4, 0.3]) * 43560.0,                     
                 },
                "zone":{
                     "zone_id":array([1,2,3]),
                 }             
                 
           }
        )
        
        should_be = array([1, 1, 1, 1, 2, 2, 3, 4])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
