# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import where, float32, zeros, clip

class developable_maximum_industrial_sqft(Variable):
    """How many industrial sqft are at most developable for each zone."""

    _return_type = "int32"
    units = "buildings_industrial_sqft"
    total_maximum = "total_maximum_development_industrial"

    def dependencies(self):
        return [my_attribute_label(self.units),
                my_attribute_label(self.total_maximum)
                 ]

    def compute(self, dataset_pool):
        where_developable = where(self.get_dataset().get_attribute(self.total_maximum) > 0)[0]
        result = zeros((self.get_dataset().size(),),dtype=self._return_type)
        tot_max = self.get_dataset().get_attribute_by_index(self.total_maximum, where_developable)
        result[where_developable] = \
            clip(tot_max - \
            self.get_dataset().get_attribute_by_index(self.units, where_developable),
                              0, tot_max.max()).astype(self._return_type)
        return result
