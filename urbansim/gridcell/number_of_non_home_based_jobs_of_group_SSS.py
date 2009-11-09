# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import where
from opus_core.datasets.dataset import DatasetSubset
from opus_core.logger import logger

class number_of_non_home_based_jobs_of_group_SSS(Variable):
    """Computes number of jobs of a specified group (which is a collection of sectors) in a gridcell"""
    _return_type="int32"

    def __init__(self, group):
        self.group = group
        self.job_is_in_employment_sector_group = "is_in_employment_sector_group_"+ self.group
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector_group), 
                attribute_label("job", "is_home_based_job"), 
                attribute_label("job", "grid_id"), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        nhb_jobs = DatasetSubset(jobs, where(jobs.get_attribute('is_home_based_job')==0)[0])
        return self.get_dataset().sum_dataset_over_ids(nhb_jobs, self.job_is_in_employment_sector_group)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        """Sum the number of jobs for a given gridcell that are in the employment sector specified by DDD """
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's grid_id = 2 (it's in gridcell 2), etc.
        job_grid_id = array([2, 1, 3, 1] )
        home_based = array([1,1,0,0])
        #corresponds to above job array, specifies which jobs in which locations "qualify"
        is_in_employment_sector_group = array([0, 1, 1, 0] )

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
                    "is_home_based_job":home_based,
                    "is_in_employment_sector_group_basic":is_in_employment_sector_group
                }
            }
        )
        
        should_be = array([0, 0, 1])
        instance_name = "urbansim.gridcell.number_of_non_home_based_jobs_of_group_basic"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()