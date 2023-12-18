# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from .variable_functions import my_attribute_label

class ln_industrial_sqft(Variable):
    """Natural log of the industrial_sqft for this gridcell"""
    
    _return_type="float32"    
    industrial_sqft = "industrial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.industrial_sqft))

#the ln_bounded function is tested in ln_commercial_sqft