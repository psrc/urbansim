# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import zeros, where

class total_maximum_development_SSS(Variable):
    """How many commercial/industrial sqft or residential units are at most developable for each
    gridcell after applying development constraints without subtracting developed units."""

    _return_type = "int32"
    is_developable = "is_in_development_type_group_developable"

    def __init__(self, sss):
        Variable.__init__(self)
        self.type = sss

    def dependencies(self):
        return [my_attribute_label(self.is_developable)]

    def compute(self, dataset_pool):
        constraints = dataset_pool.get_dataset('development_constraint')
        is_developable = self.get_dataset().get_attribute(self.is_developable).astype("?")
        result = zeros((self.get_dataset().size(),),dtype=self._return_type)
        result[is_developable] = (self.get_dataset().get_development_constrained_capacity(
            constraints,
            dataset_pool=dataset_pool,
            index=where(is_developable)[0])[self.type][:,1]).astype(self._return_type)
        return result
