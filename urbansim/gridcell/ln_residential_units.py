# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_residential_units(Variable):
    """Natural log of the residential_units for this gridcell"""
    
    _return_type="float32"      
    residential_units = "residential_units"
    
    def dependencies(self):
        return [my_attribute_label(self.residential_units)]
        
    def compute(self, dataset_pool):    
        return ln_bounded(self.get_dataset().get_attribute(self.residential_units))

#the ln_bounded function is tested in ln_commercial_sqft        