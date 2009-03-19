# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class occupied_sqft(Variable):
    """Number of households in a given parcel"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_occupied_sqft=building.aggregate(business.sqft)"]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_occupied_sqft")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("business").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)