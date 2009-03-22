# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_non_residential_sqft(Variable):
    """"""

    _return_type="int32"
    
    def dependencies(self):
        return [
               #"_vacant_building_sqft=sanfrancisco.building.nonresidential_building_sqft - sanfrancisco.building.occupied_sqft", 
                "_vacant_nonresidential_sqft=building.non_residential_sqft - sanfrancisco.building.occupied_sqft"]

    def compute(self,  dataset_pool):
        return clip_to_zero_if_needed( self.get_dataset().get_attribute("_vacant_nonresidential_sqft") )

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("building_sqft").max()
        self.do_check("x >= 0 and x <= " + str(size), values)
