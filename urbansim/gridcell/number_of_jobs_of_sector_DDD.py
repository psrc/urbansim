# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs_of_sector_DDD(Variable):
    """Sum the number of jobs for a given gridcell that are in the employment sector specified by DDD """
    _return_type="int32"
    
    def __init__(self, number):
        self.tnumber = number
        self.job_is_in_employment_sector = "is_in_employment_sector_"+str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector),
            'job.grid_id']

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, self.job_is_in_employment_sector)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's grid_id = 2 (it's in gridcell 2), etc.
        job_grid_id = array([2, 1, 3, 1])
        #corresponds to above job array, specifies which jobs in which locations "qualify"
        is_in_employment_sector = array([0, 1, 1, 0])

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
                    "is_in_employment_sector_2":is_in_employment_sector
                }
            } 
        )
        
        should_be = array([1, 0, 1])
        instance_name = "urbansim.gridcell.number_of_jobs_of_sector_2"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()