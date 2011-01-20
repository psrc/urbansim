# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class ln_sector_DDD_jobs_in_faz(Variable):
    """Natural log of the sector_DDD_jobs_in_faz for this gridcell"""
      
    _return_type="float32"
    
    def __init__(self, number):
        self.tnumber = number
        self.number_of_jobs_of_sector = "sector_"+str(int(self.tnumber))+"_jobs_in_faz"
        Variable.__init__(self)
    
    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs_of_sector)]
        
    def compute(self, dataset_pool):
        return ln_bounded(self.get_dataset().get_attribute(self.number_of_jobs_of_sector))
        
#this is a special case of sector_DDD_jobs_in_faz, so the unnittest is there
#the ln_bounded function is tested in ln_commercial_sqft