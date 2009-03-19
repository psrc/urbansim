# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_jobs_within_walking_distance(Variable):
    """
    """
    _return_type="float32"
    
    def dependencies(self):
        return ["_number_of_jobs_within_walking_distance=building.disaggregate(psrc.parcel.number_of_jobs_within_walking_distance)"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_number_of_jobs_within_walking_distance")
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
