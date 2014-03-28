# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class income_breaks_DDD_DDD_DDD(Variable):
    """Income breaks"""
    
    def __init__(self, break1, break2, break3):
        self.breaks = (break1, break2, break3)
        Variable.__init__(self)
        
    def dependencies(self):
        return ["income_breaks = 1 * (household.income < %s) +" % self.breaks[0] + \
                " 2 * numpy.logical_and(household.income >= %s, household.income < %s) +" % (self.breaks[0], self.breaks[1]) + \
                " 3 * numpy.logical_and(household.income >= %s, household.income < %s) +" % (self.breaks[1], self.breaks[2]) + \
                " 4 * (household.income >= %s)"  % self.breaks[2]
             ]
        
    def compute(self, dataset_pool):
        return self.get_dataset()["income_breaks"]
        