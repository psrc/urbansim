# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class share_of_de_population_DDD(Variable):
    """share of population in the faz.
"""
    _return_type="float32"

    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "de_population_" + str(int(number))
        Variable.__init__(self)
    
    
    def dependencies(self):
        return [attribute_label("faz", self.variable_name)]
    
    def compute(self, dataset_pool):
        population = self.get_dataset().get_attribute(self.variable_name)
        return population.astype(float32) / population.sum()
