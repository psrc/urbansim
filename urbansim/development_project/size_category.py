# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class size_category(Variable):
    """Create categories accoring to the sizes of projects"""
    
    def dependencies(self):
        return [my_attribute_label("project_id")]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.categorize(attribute_name=ds.attribute_name, bins=ds.categories)+1
