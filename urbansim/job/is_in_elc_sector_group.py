# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_in_elc_sector_group(Variable):
    
    def dependencies(self):
        return [my_attribute_label("is_in_employment_sector_group_elc_sector")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("is_in_employment_sector_group_elc_sector")
      