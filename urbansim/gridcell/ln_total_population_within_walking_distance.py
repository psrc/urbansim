# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_total_population_within_walking_distance(Variable):
    """Natural log of the total_population_within_walking_distance for this gridcell"""
    
    _return_type="float32"  
    total_population_within_walking_distance = "total_population_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.total_population_within_walking_distance)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.total_population_within_walking_distance))

#this is a special case of total_population_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft