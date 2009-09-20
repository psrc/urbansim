# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class employment_within_DDD_minutes_SSS_travel_time(abstract_access_within_threshold_variable):
    """total number of jobs for zones within DDD minutes SSS (mode) travel time,
    """
    
    _return_type = "int32"
    zone_attribute_to_access = "sanfrancisco.zone.employment"
    function = "sum"

    def __init__(self, number, mode):
        self.threshold = number
        self.travel_data_attribute  = "travel_data.%s" % mode
        abstract_access_within_threshold_variable.__init__(self)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def do(self, ddd, sss, should_be):
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
                     sss:array([1.1, 2.2, 3.3, 4.4])}
            }
        )
        instance_name = "sanfrancisco.zone.employment_within_%s_minutes_%s_travel_time" % (ddd, sss) 
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

    def test_to_2(self):
        should_be = array([0, 10])
        self.do(2, 'hwy', should_be)

    def test_to_4(self):
        should_be = array([10, 11])
        self.do(4, 'bart', should_be)

if __name__=='__main__':
    opus_unittest.main()