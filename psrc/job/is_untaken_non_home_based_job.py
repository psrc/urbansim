# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8, logical_and

class is_untaken_non_home_based_job(Variable):
    """return if a job is untaken and non home-based"""

    def dependencies(self):
        return [my_attribute_label("is_untaken"),
                "job.home_based"]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        results = logical_and(jobs.get_attribute("is_untaken"),
                              1 - jobs.get_attribute("home_based"))
        return results
    
