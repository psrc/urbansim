# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_home_based_jobs(Variable):
    """Number of home_based jobs for a given zone """

    _return_type="int32"
    is_home_based = "home_based"

    def dependencies(self):
        return [attribute_label("job", self.is_home_based), 
                attribute_label("job", "zone_id")]

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, self.is_home_based)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_home_based_jobs"

    def test_my_inputs(self):
        zone_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's zone_id = 2 (it's in zone 2), etc.
        job_zone_id = array([2, 1, 3, 1] )
        #corresponds to above job array, specifies which jobs in which locations "qualify"
        is_home_based = array([0, 1, 1, 1] )

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            { "zone":{
                  "zone_id":zone_id }, 
              "job":{ 
                  "zone_id":job_zone_id, 
                  "home_based":is_home_based} }, 
              dataset = "zone" )
        should_be = array([2, 0, 1])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()