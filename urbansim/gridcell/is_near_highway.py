# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.length_constants import UrbanSimLength, UrbanSimLengthConstants

class is_near_highway(Variable):
    """Boolean indicating if this gridcell is near an highway, as specified by the arterial
    threshold (a constant). Distance is assumed to be measured from the "border" of the gridcell."""

    def dependencies(self):
        return ['gridcell.distance_to_highway']

    def compute(self, dataset_pool):
        distance = self.get_dataset().get_attribute('distance_to_highway')
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        length = UrbanSimLength(distance, urbansim_constant["gridcell_width"].units)
        return length.less_than(urbansim_constant["near_highway_threshold_unit"])

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        """If cell.distance_to_highway < NearHighwayThreshold then 1 else 0."""
        #we assume that the distance is measured from the gridcell border to the arterial
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4,5,6]),
                    'distance_to_highway': array([0.0, 50.0, 99.0, 100.0, 101.0, 200.0]),
                    },
                'urbansim_constant':{
                    'cell_size': array([150]),
                    'near_highway_threshold': array([100]),
                    'units': array(['meters']),
                }
            }
        )
        
        should_be = array( [True, True, True, False, False, False] )
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()