# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import float32

class share_of_employment(Variable):
    """share of jobs in each area"""
    _return_type="float32"
    
    
    def dependencies(self):
        return ["psrc.large_area.number_of_jobs_without_resource_construction_sectors"]
    
    def compute(self, dataset_pool):
        jobs = self.get_dataset().get_attribute("number_of_jobs_without_resource_construction_sectors")
        return jobs.astype(float32) / jobs.sum()
