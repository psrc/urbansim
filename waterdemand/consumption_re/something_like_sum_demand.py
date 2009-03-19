# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from random import choice

from opus_core.variables.variable import Variable
from numpy import array

class something_like_sum_demand(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def dependencies(self):
        return ['waterdemand.consumption_re.sum_demand']
        
    def compute(self, dataset_pool):
        sum_demand = self.get_dataset().get_attribute('sum_demand')
        values = []
        for num in sum_demand:
            values.append(num + choice([1,-1])*choice([.1, .1, .1, .1, .1, .2, .2, .2, .2, .3, .3, .3, .4, .4, .5])*num)
        return array(values)