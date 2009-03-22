# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.gridcell.SSS_sector_employment_within_walking_distance import \
    SSS_sector_employment_within_walking_distance


class SSS_sector_non_home_based_employment_within_walking_distance(
                            SSS_sector_employment_within_walking_distance):

    def __init__( self, group ):
        self.dependent_variable = "number_of_non_home_based_jobs_of_group_"+ group
        Variable.__init__(self)


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
                    'number_of_non_home_based_jobs_of_group_service': array([100, 1000, 500, 1500]),
                    },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )
        
        should_be = array( [1800.0, 4600.0, 3100.0, 6000.0] )
        instance_name = "urbansim.gridcell.service_sector_non_home_based_employment_within_walking_distance"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()        