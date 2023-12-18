# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .abstract_within_walking_distance import abstract_within_walking_distance

class residential_units_within_walking_distance(abstract_within_walking_distance):
    """Sum over c in cell.walking_radius, c.residential_units."""

    _return_type = "int32"
    dependent_variable = "residential_units"

    def post_check(self, values, dataset_pool):
        residential_units_sum = self.get_dataset().get_attribute(self.residential_units).sum()
        self.do_check("0 <= x and x <= " + str(residential_units_sum), ma.filled(values,0))


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
                    'residential_units': array([100, 500, 1000, 1500]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )

        should_be = array([1800, 3100, 4600, 6000])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()