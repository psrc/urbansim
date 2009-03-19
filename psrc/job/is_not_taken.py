# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8

class is_not_taken(Variable):
    """return if a job has a match to person in persons table"""

    def dependencies(self):
        return [my_attribute_label("job_id"),
                "person.job_id", "person.person_id"]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        persons = arguments.translate("person")
        hh_ids = jobs.get_join_data(persons, "person_id", join_attribute="job_id",
                           return_value_if_not_found=-1)
        return (hh_ids == -1)
    
