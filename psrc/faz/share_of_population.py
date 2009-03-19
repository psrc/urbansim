# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class share_of_population(Variable):
    """share of population in the faz.
"""
    _return_type="float32"
    
    
    def dependencies(self):
        return ["urbansim.faz.population"]
    
    def compute(self, dataset_pool):
        population = self.get_dataset().get_attribute("population")
        return population.astype(float32) / population.sum()
