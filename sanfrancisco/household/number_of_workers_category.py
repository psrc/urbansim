# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
    
class number_of_workers_category(Variable):
    """break number of workers to category"""
        
    def dependencies(self):
        return ["household.nfulltime"
                ]
        
    def compute(self,  dataset_pool):
        hhs = self.get_dataset().get_attribute("nfulltime")
        results = zeros(hhs.size)      #by default, categorize to 0
        results[hhs==1] = 1            #change to 1 if household size is 1
        results[hhs==2] = 2            #change to 2 if household size is 2
        results[hhs>=3] = 3            #change to 2 if household size is 2        
        return results
