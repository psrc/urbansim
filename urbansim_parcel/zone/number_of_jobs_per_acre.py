# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs_per_acre(Variable):
    """Number of jobs in zone / number of acres in zone"""
    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.zone.number_of_jobs",
                "acres = zone.aggregate(parcel.parcel_sqft) / 43560.0 ",
                ]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute('number_of_jobs') / self.get_dataset().get_attribute('acres')
        
    def post_check(self, values, dataset_pool):
        size = self.get_dataset().get_attribute("number_of_jobs").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
        

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
        
        should_be = array([4/0.1, int(2/(0.3+0.4)), 2/0.2])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
