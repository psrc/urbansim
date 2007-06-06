#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variables.variable import Variable
from opus_core.misc import unique_values
from variable_functions import my_attribute_label
from numpy import zeros

class units_occupied(Variable):
    """units occupied by consumers, the unit is defined by unit_name in generic_building_types 
       table (either building_sqft or residential_units)
    """

    _return_type="int32"
        
    def dependencies(self):
        return [
#                "occupied_building_sqft = building.aggregate(business.building_sqft)",
#                "occupied_residential_units = building.number_of_agents(household)",
#                "az_smart.building.building_sqft_per_residential_unit",
#                "_units_occupied = building.occupied_building_sqft + building.occupied_residential_units * building.building_sqft_per_residential_unit"
                "_generic_unit_name = building.disaggregate(generic_building_type.unit_name, intermediates=[building_type])",
                "parcel_sqft = building.disaggregate(parcel.parcel_sqft)",

##                "generic_building_type_name = building.disaggregate(generic_building_type.generic_building_type_name, intermediates=[building_type])"
                ]

    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        results = zeros(buildings.size(), dtype=self._return_type)
#        results += buildings.get_attribute("_units_occupied")
        ##TODO: these dummy values are used when the businesses and households tables aren't ready
        for unit_name in unique_values(dataset_pool.get_dataset("generic_building_type").get_attribute("unit_name")):
            #should not count parcel_sqft
            if unit_name == "parcel_sqft":continue
            matched = buildings.get_attribute("_generic_unit_name") == unit_name
            results[matched] = buildings.get_attribute(unit_name)[matched].astype(self._return_type)
        return results

    def post_check(self,  values, dataset_pool=None):
#        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0")
