# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_home_based_jobs(Variable):
    """Computes the number of home based jobs for a gridcell"""

    _return_type="int32"
    home_based = "is_home_based_job"

    def dependencies(self):
        return [attribute_label("job", "grid_id"), 
                attribute_label("job", self.home_based), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, attribute_name=self.home_based)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('job').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's grid_id = 2 (it's in gridcell 2), etc.
        job_grid_id = array([2, 1, 3, 1])
        #corresponds to above job array, specifies which jobs in which locations are in the group of interest
        home_based = array([0, 1, 1, 1]) 

        #thorough explanation in number_of_high_income_households

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "gridcell_grid_id":gridcell_grid_id }, 
                "job":{ 
                    "job_id":array([1,2,3,4]),
                    "grid_id":job_grid_id, 
                    "is_home_based_job":home_based
                }
            }
        )
        
        should_be = array([2, 0, 1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()