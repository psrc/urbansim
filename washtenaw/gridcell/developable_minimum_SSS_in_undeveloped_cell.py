# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import where, float32, zeros, logical_and

class developable_minimum_SSS_in_undeveloped_cell(Variable):
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
        result = zeros((self.get_dataset().size(),),dtype=float32)
        result[w] = self.get_dataset().get_development_constrained_capacity(
            constraints, 
            dataset_pool=dataset_pool,
            index=w)[self.type][:,0]
        return result
                       
    def post_check(self, values, dataset_pool):
        upper_limit = 4000000   #TODO replace hard-coded upper limit with config or constant
        self.do_check("x >= 0 and x <= %s" % upper_limit, values)
        