# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import zeros

class developable_maximum_industrial_sqft(Variable):
    """How many industrial sqft are at most developable for each gridcell after applying
    development constraints."""
    _return_type = "int32"
    industrial_sqft = "industrial_sqft"
    total_maximum = "total_maximum_development_industrial"

    def dependencies(self):
        return [my_attribute_label(self.industrial_sqft),
                my_attribute_label(self.total_maximum)]

    def compute(self, dataset_pool):
        is_developable = self.get_dataset().get_attribute(self.total_maximum) > 0
        result = zeros((self.get_dataset().size(),),dtype=self._return_type)
        values = self.get_dataset().get_attribute_by_index(self.total_maximum, is_developable) - \
            self.get_dataset().get_attribute_by_index(self.industrial_sqft, is_developable)
        result[is_developable] = values.astype(self._return_type)

        return result

    def post_check(self, values, dataset_pool):
        upper_limit = 1200000    #TODO replace hard-coded upper limit with config or constant
        self.do_check("x >= 0 and x <= %s" % upper_limit, values)
