# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_developable_commercial_sqft_capacity_within_walking_distance(Variable):
    """Natural log of the developable_commercial_sqft_capacity_within_walking_distance for this gridcell"""
    
    _return_type="float32"    
    commercial_sqft_wwd = "developable_commercial_sqft_capacity_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.commercial_sqft_wwd)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.commercial_sqft_wwd))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft