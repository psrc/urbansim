# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from percent_developed_within_walking_distance import percent_developed_within_walking_distance

class percent_developed_with_buildings_within_walking_distance(percent_developed_within_walking_distance):
    """See percent_developed_within_walking_distance. This variable is computed using the buildings table."""
    
    number_of_developed_wwd = "number_of_developed_with_buildings_within_walking_distance"

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
                    'number_of_developed_with_buildings_within_walking_distance': array([3, 5, 1, 0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = 100 * array( [3/5.0, 
                                  5/5.0, 
                                  1/5.0, 
                                  0/5.0] )
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
