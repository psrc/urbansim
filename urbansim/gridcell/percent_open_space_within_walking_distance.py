# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma

class percent_open_space_within_walking_distance(Variable):
    """"""
    acres_open_space_wwd = "acres_open_space_within_walking_distance"
    _return_type="float32"
    def dependencies(self):
        return [my_attribute_label(self.acres_open_space_wwd)]

    def compute(self, dataset_pool):
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        return 100.0 * (self.get_dataset().get_attribute(self.acres_open_space_wwd) / 
                        float(urbansim_constant["walking_distance_footprint"].sum() * 
                              urbansim_constant["acres"]))


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
                    'acres_open_space_within_walking_distance': array([20, 10, 5, 0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        acres_within_walking_distance = 5 * 5.5597500000000002
        should_be = 100* array([20/acres_within_walking_distance,
                                10/acres_within_walking_distance,
                                5/acres_within_walking_distance,
                                0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

    
if __name__=='__main__':    
    opus_unittest.main()