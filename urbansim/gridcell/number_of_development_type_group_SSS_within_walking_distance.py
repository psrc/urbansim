# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class number_of_development_type_group_SSS_within_walking_distance(abstract_within_walking_distance):
    """Total number of locations within walking distance that are of DDD development type"""

    _return_type = "int32"
    def __init__(self, group):
        self.dependent_variable = "is_in_development_type_group_" + group
        abstract_within_walking_distance.__init__(self)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


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
                    'is_in_development_type_group_residential': array([1, 1, 1, 0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )

        should_be = array([5, 4, 4, 2])
        #"1" in this case is the group number. was originally DDD, but have to specify it since this is a test, and the
        #"parent code" isn't actually invoked
        instance_name = "urbansim.gridcell.number_of_development_type_group_residential_within_walking_distance"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()