# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_nonresidential_improvement_value(Variable):
    """Natural log of the nonresidential_improvement_value for this gridcell"""
    
    _return_type="float32"  
    nonresidential_improvement_value = "nonresidential_improvement_value"
    
    def dependencies(self):
        return [my_attribute_label(self.nonresidential_improvement_value)]
        
    def compute(self, resources):
        return ln_bounded(resources["dataset"].get_attribute(self.nonresidential_improvement_value))
        
#this is a special case of nonresidential_improvement_value, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft