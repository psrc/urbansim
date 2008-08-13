#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

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
