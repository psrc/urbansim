# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8

class capacity(Variable):
    """return how many persons a job requires (always 1)"""

    def dependencies(self):
        return [my_attribute_label("job_id")]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        return ones(jobs.size(), dtype=int8)
    
