# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class industrial_sqft_within_walking_distance(abstract_within_walking_distance):
    """Sum of industrial sqft. of locations within walking distance of this gridcell"""

    _return_type = "int32"
    dependent_variable = "industrial_sqft"

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'industrial_sqft': array([100, 500, 1000, 1500]),
                },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )

        should_be = array([1800.0, 3100.0, 4600.0, 6000.0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()