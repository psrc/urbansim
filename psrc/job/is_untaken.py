# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8

class is_untaken(Variable):
    """return if a job has a match to person in persons table"""

    def dependencies(self):
        return [my_attribute_label("job_id"),
                "person.job_id", "person.person_id"]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        persons = dataset_pool.get_dataset("person")
        workers = jobs.sum_dataset_over_ids(persons, constant=1)
        return (workers == 0)
    
