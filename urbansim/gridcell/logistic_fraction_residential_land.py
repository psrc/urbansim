# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class logistic_fraction_residential_land(Variable):
    """Natural log of the total_value for this gridcell"""
    
    _return_type="float32"  
    
    def dependencies(self):
        return [my_attribute_label('fraction_residential_land')]
        
    def compute(self, dataset_pool):
        res_fraction = self.get_dataset().get_attribute("fraction_residential_land")
        return ln_bounded(res_fraction/(1-res_fraction))
        