# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class sector_DDD_non_home_based_employment_within_walking_distance(abstract_within_walking_distance):
    """Sum over c in cell.walking_radius, count of j in c.placed_jobs
    where employment_sector_groups includes sector DDD."""

    def __init__(self, number):
        self.dependent_variable = "number_of_non_home_based_jobs_of_sector_"+str(int(number))
        abstract_within_walking_distance.__init__(self)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'number_of_non_home_based_jobs_of_sector_1': array([100, 500, 1000, 1500]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = array([1800, 3100, 4600, 6000])
        instance_name = "urbansim.gridcell.sector_1_non_home_based_employment_within_walking_distance"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()