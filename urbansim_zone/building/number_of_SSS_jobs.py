# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class number_of_SSS_jobs(Variable):
    """Number of SSS (e.g. commercial, industrial) jobs in each building"""

    _return_type="int32"
    
    def __init__(self, type):
        self.status = type
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim_zone.job.is_building_type_%s" % self.status,
                "job.building_id"
                ]

    def compute(self,  dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, attribute_name="is_building_type_%s" % self.status)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone','urbansim'],
            test_data={
            'job':
            {"job_id":array([1,2,3,4,5]),
             "building_id":array([1,1,3,2,2]),
             },
            'building':
            {
             'building_id':array([1,2,3]),
             'building_type_id': array([1,1,2]),
             },
            'building_type':
            {
             "building_type_id":array([1,2]),
             "building_type_name":array(["commercial", "industrial"])
             },
             
           }
        )
        
        should_be = array([0, 0, 1])
        instance_name = 'urbansim_zone.building.number_of_industrial_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        should_be = array([2, 2, 0])
        instance_name = 'urbansim_zone.building.number_of_commercial_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()