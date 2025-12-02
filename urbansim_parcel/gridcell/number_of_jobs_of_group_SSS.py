from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label

class number_of_jobs_of_group_SSS(Variable):
    """Computes number of jobs of a specified group (which is a collection of sectors) in a gridcell"""
    _return_type="int32"

    def __init__(self, group):
        self.group = group
        self.job_is_in_employment_sector_group = "is_in_employment_sector_group_" + self.group
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector_group), 
                attribute_label("job", "job_id"), 
                "urbansim_parcel.job.grid_id", 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, self.job_is_in_employment_sector_group)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
        