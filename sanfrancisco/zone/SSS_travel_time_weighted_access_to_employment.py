# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_weighted_access import abstract_weighted_access

class SSS_travel_time_weighted_access_to_employment(abstract_weighted_access):
    """sum of number of jobs in zone j divided by SSS (mode) travel time from zone i to j,
    """

    def __init__(self, mode):
        self.aggregate_by_origin = False
        self.travel_data_attribute  = "travel_data."+mode
        self.zone_attribute_to_access = "zone.employment"
        
        abstract_weighted_access.__init__(self)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        mode = 'hwy'
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                 "zone":{
                    "zone_id":array([1,3]),
                    "employment":array([10, 1])},
                 "travel_data":{
                     "from_zone_id":array([3,3,1,1]),
                     "to_zone_id":array([1,3,1,3]),
                     mode:array([1, 2, 3, 4])}                 
                 }
        )
        should_be = array([1.17361, 10.25])
        instance_name = "sanfrancisco.zone.%s_travel_time_weighted_access_to_employment" % mode
        tester.test_is_close_for_family_variable(self, should_be, instance_name, rtol=1e-5)

if __name__=='__main__':
    opus_unittest.main()