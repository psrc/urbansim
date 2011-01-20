# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from numpy import ma
from abstract_within_walking_distance import abstract_within_walking_distance
from variable_functions import my_attribute_label

class average_building_age_within_walking_distance( abstract_within_walking_distance ):
    """average building age within walking distance calculated only over 'valid' ages.
    The results are rounded to the nearest integer. gridcells that have no valid age wwd are masked."""

    _return_type = "int32"
    dependent_variable = "building_age_masked"
    sum_gridcells = "sum_has_valid_year_built_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.dependent_variable), my_attribute_label(self.sum_gridcells)]

    def compute(self, dataset_pool):
        sum_ages = abstract_within_walking_distance.compute(self, dataset_pool)
        sum_grids = self.get_dataset().get_attribute(self.sum_gridcells)
        return ma.masked_where(sum_grids == 0, (sum_ages/sum_grids.astype("float32")).round())

    def post_check(self, values, dataset_pool):
        self.do_check( "x >= 0", values )


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from opus_core.simulation_state import SimulationState

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
                    'year_built': array([1995, 1799, 2006, 200], dtype="int32")
                },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                     'cell_size': array([150]),
                }
            }
        )
        SimulationState().set_current_time(2005)
        should_be = array( [8, 10, 2, 0] )
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
