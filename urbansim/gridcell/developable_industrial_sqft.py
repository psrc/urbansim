# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class developable_industrial_sqft(Variable):
    """"""

    developable_max = "developable_maximum_industrial_sqft"
    def dependencies(self):
        return [my_attribute_label(self.developable_max)]

    def compute(self, dataset_pool):
        max = self.get_dataset().get_attribute(self.developable_max)
        return max

    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.developable_max).max()
        self.do_check("x >= 0 and x <=%s" % global_max, values)                       