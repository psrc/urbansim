# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class number_of_businesses_of_building_use_SSS(Variable):
    """Number of businesses of_building_use_SSS in a given parcel"""

    _return_type="int32"
    def __init__(self, building_use):
        self.building_use = building_use.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "is_of_building_use_%s = sanfrancisco.business.is_building_use_%s" % (self.building_use, self.building_use),
                "_number_of_businesses_of_building_use_%s = building.aggregate(business.is_of_building_use_%s)" % (self.building_use, self.building_use)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_businesses_of_building_use_%s" % self.building_use)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)
