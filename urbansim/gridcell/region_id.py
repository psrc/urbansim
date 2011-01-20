# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones

class region_id(Variable):
    """Always returns 1"""

    def dependencies(self):
        return [my_attribute_label('grid_id')]

    def compute(self, dataset_pool):
        return ones(self.get_dataset().size())