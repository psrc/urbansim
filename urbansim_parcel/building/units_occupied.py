# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import unique
from variable_functions import my_attribute_label
from numpy import zeros

class units_occupied(Variable):
    """units occupied by consumers, the unit is defined by unit_name in building_types 
       table (either building_sqft or residential_units)
    """

    _return_type="int32"
        
    def dependencies(self):
        return [
                "urbansim_parcel.building.generic_unit_name",
                "urbansim_parcel.building.parcel_sqft",
                "building_type.unit_name"
                ]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(), dtype=self._return_type)
        ##TODO: these dummy values are used when the businesses and households tables aren't ready
        for unit_name in unique(dataset_pool.get_dataset("building_type").get_attribute("unit_name")):
            #should not count parcel_sqft
            if unit_name == "parcel_sqft":continue
            matched = buildings.get_attribute("unit_name") == unit_name
            results[matched] = buildings.get_attribute(unit_name)[matched].astype(self._return_type)
        return results

    def post_check(self,  values, dataset_pool=None):
#        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0")


## TODO: create unittest for this variable