# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_developable_for_industrial_sqft(Variable):
    """"""

    developable_max = "developable_maximum_industrial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.developable_max)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.developable_max) > 0
                       