# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_inc(Variable):
    """Natural log of the inc for this gridcell"""
        
    _return_type="float32"
    inc = "medinc"

    def dependencies(self):
        return [my_attribute_label(self.inc)]

    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.inc))
