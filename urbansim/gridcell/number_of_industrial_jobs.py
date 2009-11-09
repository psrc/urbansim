# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_industrial_jobs(Variable):
    """Number of industrial jobs for a given gridcell """

    _return_type="int32"
    is_industrial = "is_industrial"

    def dependencies(self):
        return [attribute_label("job", self.is_industrial), 
                attribute_label("job", "grid_id"), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, self.is_industrial)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's grid_id = 2 (it's in gridcell 2), etc.
        job_grid_id = array([2, 1, 3, 1] )
        #corresponds to above job array, specifies which jobs in which locations "qualify"
        is_industrial = array([0, 1, 1, 1] )

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":gridcell_grid_id 
                    },
                "job":{ 
                    "job_id":array([1,2,3,4]),
                    "grid_id":job_grid_id, 
                    "is_industrial":is_industrial
                }
            }
        )
        
        should_be = array([2, 0, 1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()