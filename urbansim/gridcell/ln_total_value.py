# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_total_value(Variable):
    """Natural log of the total_value for this gridcell"""
    
    _return_type="float32"  
    total_value = "total_value"
    
    def dependencies(self):
        return [my_attribute_label(self.total_value)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.total_value))
        
#this is a special case of total_value, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft