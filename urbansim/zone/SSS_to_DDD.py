# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class SSS_to_DDD(abstract_travel_time_variable_for_non_interaction_dataset):
    """Travel time by mode SSS to the zone whose ID is the DDD.
    """
    default_value = 999
    origin_zone_id = 'zone.zone_id'

    def __init__(self, mode, number):
        self.travel_data_attribute = "travel_data.%s" % mode
        self.destination_zone_id = "destination_zone_id=%s+0*zone.zone_id" % number 
        abstract_travel_time_variable_for_non_interaction_dataset.__init__(self)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def do(self,sss, ddd, should_be):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                 "zone":{
                    "zone_id":array([1,3])},
                 "travel_data":{
                     "from_zone_id":array([3,3,1,1]),
                     "to_zone_id":array([1,3,1,3]),
                     sss:array([1.1, 2.2, 3.3, 4.4])}            
                 }
        )
        instance_name = "urbansim.zone.%s_to_%s" % (sss, ddd)
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

    def test_to_1(self):
        should_be = array([3.3, 1.1])
        self.do('hwy', 1, should_be)

    def test_to_3(self):
        should_be = array([4.4, 2.2])
        self.do('bart', 3, should_be)

if __name__=='__main__':
    opus_unittest.main()
    
