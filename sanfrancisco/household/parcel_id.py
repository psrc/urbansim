# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class parcel_id(Variable):
    """The parcel_id of household."""
    
    def dependencies(self):
        return ["_parcel_id = household.disaggregate(building.parcel_id)"]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_parcel_id")
