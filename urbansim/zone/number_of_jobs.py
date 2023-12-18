# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs(Variable):
    """Number of jobs in zones """
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("job", "zone_id"), 
                my_attribute_label("zone_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(households, constant=1)
        
    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('job').size()
        self.do_check("x >= 0 and x <= " + str(size), values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_jobs"

    def test_my_inputs(self):
        zone_ids = array([1,2,1,3]) 
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2, 3])}, 
            "job":{ 
                "zone_id":zone_ids}}, 
            dataset = "zone")
        should_be = array([2, 1, 1])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()