# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from .variable_functions import my_attribute_label

class ln_developable_commercial_sqft_capacity(Variable):
    """Natural log of the developable_commercial_sqft_capacity for this gridcell"""
    
    _return_type="float32"    
    commercial_sqft = "developable_commercial_sqft_capacity"

    def dependencies(self):
        return [my_attribute_label(self.commercial_sqft)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.commercial_sqft))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft