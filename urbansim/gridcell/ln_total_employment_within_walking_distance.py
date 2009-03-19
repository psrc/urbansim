# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_total_employment_within_walking_distance(Variable):
    """Natural log of the total_employment_within_walking_distance for this gridcell"""
    
    _return_type="float32"  
    total_employment_within_walking_distance = "total_employment_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.total_employment_within_walking_distance)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.total_employment_within_walking_distance))

#the ln_bounded function is tested in ln_commercial_sqft
#this is a special case of total_employment_within_walking_distance, so the unnittest is there