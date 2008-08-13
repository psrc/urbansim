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
from numpy import where, zeros

class developable_minimum_residential_units(Variable):
    """The minimum number of residential units that must be developed for each gridcell after applying
    development constraints.  Only development projects with at least this number of residential units
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
            index=where_developable)["residential"][:,0]).astype(self._return_type)
        return result
