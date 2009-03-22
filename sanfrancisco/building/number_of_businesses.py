# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_businesses(Variable):
    """Number of businesses in a given parcel"""

    _return_type="int32"
        
    def dependencies(self):
        return ["_number_of_businesses=building.number_of_agents(business)"]
                
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_businesses")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
