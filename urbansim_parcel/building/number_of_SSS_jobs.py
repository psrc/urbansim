# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import where

class number_of_SSS_jobs(Variable):
    """Number of SSS (home_based, non_home_based) jobs in a given building"""

    _return_type="int32"
    
    def __init__(self, status):
        self.status = status
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim.job.is_building_type_%s" % self.status,
                "job.building_id"
                ]

    def compute(self,  dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, attribute_name="is_building_type_%s" % self.status)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").size()
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
            'job':
            {"job_id":array([1,2,3,4,5]),
             "building_type":array([1,2,1,1,2]),
             "building_id":array([1,1,3,2,2]),
             },
            'building':
            {
             "building_id":array([1,2,3]),
             },
            'job_building_type':
            {
             "id":array([1,2]),
             "name":array(["home_based", "non_home_based"])
             },
             
           }
        )
        
        should_be = array([1, 1, 0])
        instance_name = 'urbansim_parcel.building.number_of_non_home_based_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()