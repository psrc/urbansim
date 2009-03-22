# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import where, zeros

class developable_minimum_industrial_sqft(Variable):
    """The minimum number of industrial sqft that must be developed for each gridcell after applying
    development constraints.  Only development projects with at least this number of industrial sqft
    will be placed in these gridcells."""

    _return_type = "int32"
    is_developable = "is_in_development_type_group_developable"

    def dependencies(self):
        return [my_attribute_label(self.is_developable)]

    def compute(self, dataset_pool):
        constraints = dataset_pool.get_dataset('development_constraint')
        where_developable = where(self.get_dataset().get_attribute(self.is_developable))[0]
        result = zeros((self.get_dataset().size(),),dtype=self._return_type)
        result[where_developable] = (self.get_dataset().get_development_constrained_capacity(
            constraints,
            dataset_pool=dataset_pool,
            index=where_developable)["industrial"][:,0]).astype(self._return_type)
        return result
