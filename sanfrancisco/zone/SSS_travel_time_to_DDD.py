# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import where, zeros, float32

class SSS_travel_time_to_DDD(Variable):
    """Travel time by mode SSS to the zone whose ID is the DDD.
    """
    def __init__(self, mode, number):
        self.mode = mode
        self.dzone_id = number
        self.my_name = "%s_travel_time_to_%s" % (self.mode, self.dzone_id)
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.mode),
                attribute_label("travel_data", "from_zone_id"),
                attribute_label("travel_data", "to_zone_id")
                ]
    
    def compute(self,  dataset_pool):
        zone_id = self.get_dataset().get_id_attribute()
        keys = map(lambda x: (x, self.dzone_id), zone_id)
        travel_data = dataset_pool.get_dataset("travel_data")
        try:
            time = travel_data.get_attribute_by_id(self.mode, keys)
        except:
            logger.log_warning("Variable %s returns zeros, since zone number %d is not in zoneset." % (self.my_name, self.dzone_id))
            time = zeros(self.get_dataset().size(), dtype=float32)
        return time


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
        instance_name = "sanfrancisco.zone.%s_travel_time_to_%s" % (sss, ddd)
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

    def test_to_1(self):
        should_be = array([3.3, 1.1])
        self.do('hwy', 1, should_be)

    def test_to_3(self):
        should_be = array([4.4, 2.2])
        self.do('bart', 3, should_be)

if __name__=='__main__':
    opus_unittest.main()
    