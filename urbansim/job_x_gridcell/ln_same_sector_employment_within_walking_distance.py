# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_same_sector_employment_within_walking_distance(Variable):
    """Natural log of the same_sector_employment_within_walking_distance for this gridcell"""
    
    _return_type="float32"  
    same_sector_employment_within_walking_distance = "same_sector_employment_within_walking_distance"
    
    def dependencies(self):
        return [my_attribute_label(self.same_sector_employment_within_walking_distance)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.same_sector_employment_within_walking_distance))
        
#this is a special case of total_value, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft
