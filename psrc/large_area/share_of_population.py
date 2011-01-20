# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class share_of_population(Variable):
    """share of population in each area"""
    _return_type="float32"
    
    
    def dependencies(self):
        return ["psrc.large_area.population"]
    
    def compute(self, dataset_pool):
        population = self.get_dataset().get_attribute("population")
        return population.astype(float32) / population.sum()
