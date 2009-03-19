# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class is_in_scalable_sector_group(Variable):
 
    def dependencies(self):
        return [my_attribute_label("is_in_employment_sector_group_scalable_sectors")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("is_in_employment_sector_group_scalable_sectors")