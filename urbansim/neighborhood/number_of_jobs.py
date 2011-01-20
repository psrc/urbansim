# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_jobs(Variable):
    _return_type="int32"

    def dependencies(self):
        return [attribute_label("job", "neighborhood_id")]
 
    def compute(self, dataset_pool):
        jobs = dataset_pool.get_dataset('job')
        return self.get_dataset().sum_dataset_over_ids(jobs, constant=1)
     
    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('job').size()
        self.do_check("x >= 0 and x <= " + str(size), values)   