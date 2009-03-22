# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class total_buildings_SSS_space_within_walking_distance( abstract_within_walking_distance ):
    """Caclulate the buildings space of the given type within the walking distance range."""
    
    _return_type = "float32"
    
    def __init__(self, type):
        self.dependent_variable = "buildings_%s_space" % type
        abstract_within_walking_distance.__init__(self)

    def post_check(self, values, dataset_pool):
        self.do_check( "x >= 0", values )


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

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
                    'buildings_residential_space': array([100.0, 500.0, 1000.0, 1500.0]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array( [1800.0, 3100.0, 4600.0, 6000.0] )
        instance_name = "urbansim.gridcell.total_buildings_residential_space_within_walking_distance"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()
