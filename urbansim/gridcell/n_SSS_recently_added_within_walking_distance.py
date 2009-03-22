# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class n_SSS_recently_added_within_walking_distance(abstract_within_walking_distance):

    _return_type="int32"

    def __init__(self, units):
        self.dependent_variable = "n_%s_recently_added" % units
        abstract_within_walking_distance.__init__(self)

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
                    'residential_units': array([1,2,3,4]),
                    'n_residential_units_recently_added': array([1, 0, 1, 1]),
                    },
                'urbansim_constant':{
                    'recent_years': array([3]),
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([4.0, 2.0, 5.0, 4.0])
        instance_name = 'urbansim.gridcell.n_residential_units_recently_added_within_walking_distance'
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()