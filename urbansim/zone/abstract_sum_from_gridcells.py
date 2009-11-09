# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class abstract_sum_from_gridcells(Variable):
    """Sum of any variable over zones.
"""
    gc_variable = "not_defined"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_variable), 
                 attribute_label("gridcell", "zone_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'), self.gc_variable)
