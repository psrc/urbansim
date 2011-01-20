# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class percent_residential(Variable):
    """Percent residential for this gridcell"""
    
    _return_type="float32"      
    fraction_residential_land = "fraction_residential_land"
    
    def dependencies(self):
        return [my_attribute_label(self.fraction_residential_land)]
        
    def compute(self, dataset_pool):    
        return 100*(self.get_dataset().get_attribute(self.fraction_residential_land))

#(TODO: Need to add test)        