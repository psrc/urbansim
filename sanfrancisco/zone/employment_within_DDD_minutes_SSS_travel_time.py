# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import where, zeros, float32, array
from scipy.ndimage import sum as ndimage_sum

class employment_within_DDD_minutes_SSS_travel_time(Variable):
    """total number of jobs for zones within DDD minutes SSS (mode) travel time,
    """
    def __init__(self, number, mode):
        self.minutes = number
        self.mode = mode
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.mode),
                my_attribute_label("employment")]
    
    def compute(self,  dataset_pool):
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset("travel_data")
        within_indicator = (travel_data.get_attribute(self.mode) <= self.minutes)
        
        to_zone_id = travel_data.get_attribute("to_zone_id")
        zone_index = self.get_dataset().get_id_index(to_zone_id)
        num_jobs = self.get_dataset().get_attribute('employment')[zone_index]

        from_zone_id = travel_data.get_attribute("from_zone_id")        
        results = array(ndimage_sum(within_indicator * num_jobs.astype(float32), labels = from_zone_id, index=zone_ids))
        
        return results



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