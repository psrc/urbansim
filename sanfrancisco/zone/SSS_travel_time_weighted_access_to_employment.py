# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import where, power, float32, array
from scipy.ndimage import sum as ndimage_sum

class SSS_travel_time_weighted_access_to_employment(Variable):
    """sum of number of jobs in zone j divided by SSS (mode) travel time from zone i to j,
    """

    def __init__(self, mode):
        self.mode = mode
        Variable.__init__(self)
    
    def dependencies(self):
        return [attribute_label("travel_data", self.mode),
                my_attribute_label("employment")]
    
    def compute(self,  dataset_pool):
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset("travel_data")
        time = power(travel_data.get_attribute(self.mode), 2)
        
        to_zone_id = travel_data.get_attribute("to_zone_id")
        zone_index = self.get_dataset().get_id_index(to_zone_id)
        num_jobs = self.get_dataset().get_attribute('employment')[zone_index]

        from_zone_id = travel_data.get_attribute("from_zone_id")        
        results = array(ndimage_sum(num_jobs / time.astype(float32), labels = from_zone_id, index=zone_ids))
        
        return results

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