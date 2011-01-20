# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_distance_to_highway(Variable):
    """Natural log of this gridcell's distance to the nearest highway"""
    
    _return_type="float32"    
    distance_to_highway = "distance_to_highway"

    def dependencies(self):
        return [my_attribute_label(self.distance_to_highway)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.distance_to_highway))

#the ln_bounded function is tested in ln_commercial_sqft