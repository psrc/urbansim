# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_residential_units_within_walking_distance(Variable):
    """Natural log of the residential_units_within_walking_distance for this gridcell"""
    
    _return_type="float32"  
    residential_units_within_walking_distance = "residential_units_within_walking_distance"
    
    def dependencies(self):
        return [my_attribute_label(self.residential_units_within_walking_distance)]
        
    def compute(self, dataset_pool):    
        return ln_bounded(self.get_dataset().get_attribute(self.residential_units_within_walking_distance))


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_full_tree(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'residential_units': array([5.0, 3.0, 0.0, 2.0]),
                    },
                'urbansim_constant':{
                    'walking_distance_circle_radius': array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = ma.log(array([18, 16, 7, 9])) 
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()      