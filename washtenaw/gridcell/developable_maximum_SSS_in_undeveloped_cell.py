#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.variable import Variable
from variable_functions import my_attribute_label
from numarray import where, Float32, zeros, logical_and

class developable_maximum_SSS_in_undeveloped_cell(Variable):
    """How many commercial sqft are at most developable for undeveloped gridcell after applying 
    development constraints."""

    def __init__(self, unit):
        self.unit = unit
        self.type, dummy = self.unit.split('_')   #get 'residential', 'commercial' or 'industrial'
        Variable.__init__(self)

    def dependencies(self):
        return ["urbansim.gridcell.is_in_development_type_group_developable", 
                "urbansim.gridcell.is_developed",
                "urbansim.gridcell." + self.unit,
                ]

    def compute(self, dataset_pool):
        constraints = dataset_pool.get_dataset('development_constraint')
        is_developable = self.get_dataset().get_attribute("is_in_development_type_group_developable")
        is_undeveloped = 1 - self.get_dataset().get_attribute("is_developed")
        w = where(logical_and(is_developable, is_undeveloped))[0]
        result = zeros((self.get_dataset().size(),),type=Float32)
        result[w] = self.get_dataset().get_development_constrained_capacity(
            constraints, 
            dataset_pool=dataset_pool,
            index=w)[self.type][:,1]
        return result
                       
    def post_check(self, values, dataset_pool):
        upper_limit = 4000000   #TODO replace hard-coded upper limit with config or constant
        self.do_check("x >= 0 and x <= %s" % upper_limit, values)
        