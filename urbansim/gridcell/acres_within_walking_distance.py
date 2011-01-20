# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class acres_within_walking_distance( abstract_within_walking_distance ):
    """Caclulate the total acres of land within the walking distance range."""

    dependent_variable = "acres_of_land"

    def post_check(self, values, dataset_pool):
        self.do_check( "x >= 0", values )


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
                    'acres_of_land': array([100.0, 500.0, 1000.0, 1500.0])
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([1800.0, 3100.0, 4600.0, 6000.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
