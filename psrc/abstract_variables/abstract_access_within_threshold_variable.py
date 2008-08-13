#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from numpy import array
from scipy import ndimage

class abstract_access_within_threshold_variable(Variable):
    """abstract variable for access to zone attribute within a given threshold, 
    e.g. employment_within_30_minutes_travel_time_hbw_am_transit_walk.
    This is a variable for zone dataset
    """

    _return_type = "int32"
    threshold = "to_be_defined"
    travel_data_attribute  = "to_be_defined_in_fully_qualified_name"
    zone_attribute_to_access = "to_be_defined_in_fully_qualified_name"
    function = "sum"  #available functions: mean, minimum, maximum, variance
    
    def dependencies(self):
        return [self.travel_data_attribute,
                self.zone_attribute_to_access]

    def compute(self, dataset_pool):
        travel_data = dataset_pool.get_dataset('travel_data')

        zones = dataset_pool.get_dataset('zone')
        zone_ids = zones.get_id_attribute()
        dest_zone_index = zones.get_id_index(travel_data.get_attribute("to_zone_id"))
        dest_zone_attribute = zones.get_attribute(self.zone_attribute_to_access)[dest_zone_index]
        
        is_within_threshold = (travel_data.get_attribute(self.travel_data_attribute) <= self.threshold).astype('int32')
        
        from_zone_id = travel_data.get_attribute("from_zone_id")
        f = getattr(ndimage, self.function)
        results = array(f(dest_zone_attribute*is_within_threshold,
                                    labels=from_zone_id, index=zone_ids))

        return results

## unittest in child classes