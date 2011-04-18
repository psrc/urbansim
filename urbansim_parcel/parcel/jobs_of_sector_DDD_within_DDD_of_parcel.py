# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_variable_within_radius_DDD_of_parcel import abstract_variable_within_radius_DDD_of_parcel

class jobs_of_sector_DDD_within_DDD_of_parcel(abstract_variable_within_radius_DDD_of_parcel):
    """total number of jobs with sector_id=DDD within radius DDD of parcel"""
    _return_type = "int32"

    def __init__(self, sector_id, radius):
        self.quantity = "_njobs_of_sector_%s = parcel.aggregate(job.sector_id==%s)" % (sector_id, sector_id)
        abstract_variable_within_radius_DDD_of_parcel.__init__(self, radius)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    
    def test_my_inputs_sector_1(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    3 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'job':
            {
                "job_id":array([1,2,3,4,5,6,7]),
                "building_id":array([1,2,3,4,5,6,7]),
                "sector_id":array([1,2,2,1,2,1,2]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([3, 3, 1])

        instance_name = 'urbansim_parcel.parcel.jobs_of_sector_1_within_1_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
    
    def test_my_inputs_sector_2(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "x_coord_sp": array([1,   2,    3 ]),
                "y_coord_sp": array([1,   1,    1 ]),
            },
            'job':
            {
                "job_id":array([1,2,3,4,5,6,7]),
                "building_id":array([1,2,3,4,5,6,7]),
                "sector_id":array([1,2,2,1,2,1,2]),
             },
            'building':
            {
                "building_id":array([1,2,3,4,5,6,7]),
                "parcel_id":array([1,2,2,2,2,1,3]),
             },
        })
        should_be = array([3, 4, 4])

        instance_name = 'urbansim_parcel.parcel.jobs_of_sector_2_within_1_of_parcel'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
