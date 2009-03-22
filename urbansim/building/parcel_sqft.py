# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class parcel_sqft(Variable):
    """
    """
    _return_type="float32"
    
    def dependencies(self):
        return ["_parcel_sqft=building.disaggregate(parcel.parcel_sqft)"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_parcel_sqft")
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
