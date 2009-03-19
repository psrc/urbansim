# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_developable_residential_units_capacity(Variable):
    """Natural log of the developable_residential_units_capacity for this gridcell"""
    
    _return_type="float32"    
    residential_units = "developable_residential_units_capacity"

    def dependencies(self):
        return [my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.residential_units))

#this is a special case of commercial_sqft_within_walking_distance, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft