# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class share_of_de_employment_DDD(Variable):
    """share of DRAM/EMPAL jobs in each area"""
    _return_type="float32"

    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "de_employment_" + str(int(number))
        Variable.__init__(self)
    
    
    def dependencies(self):
        return ["psrc.large_area." + self.variable_name]
    
    def compute(self, dataset_pool):
        jobs = self.get_dataset().get_attribute(self.variable_name)
        return jobs.astype(float32) / jobs.sum()
