#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from urbansim.functions import attribute_label
from opus_core.logger import logger

class abstract_time_space_prism_variable(Variable):
    """abstract variable for interaction time-space prism variables"""

    default_value = 0
    _return_type="int32"
    
    agent_resource = "to_be_defined_in_fully_qualified_name"
    agent_zone_id = 'to_be_defined_in_fully_qualified_name'
    choice_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute_default_value = 999  # default value if a zone pair index is not found in travel_data
    zone_attribute_to_access = "to_be_defined_in_fully_qualified_name"
    direction_from_agent_to_choice = True   #Is direction from agent_zone_id to choice_zone_id?
        
    def dependencies(self):
        return [ self.agent_resource, 
                 self.agent_zone_id,
                 self.choice_zone_id,
                 self.travel_data_attribute,
                 self.zone_attribute_to_access
                 ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        zones = dataset_pool.get_dataset('zone')
        travel_data = dataset_pool.get_dataset('travel_data')
        
        agent_resource = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_resource,
                                                                                    interaction_dataset.get_2d_index_of_dataset1())        
        var1 = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_zone_id,
                                                                         interaction_dataset.get_2d_index_of_dataset1())
        var2 = interaction_dataset.get_2d_dataset_attribute(self.choice_zone_id)
        
        if self.direction_from_agent_to_choice:
            from_zone = var1
            to_zone = var2
        else:
            from_zone = var2
            to_zone = var1
            
        results = resize(array([self.default_value], dtype=self._return_type), from_zone.shape)
        positions = ones(from_zone.shape, dtype="int32")
        #create indices for 2d array of (origin, destination)
        ij = map(lambda x, y: (x, y), where(positions)[0], where(positions)[1])
        zone_ids = zones.get_id_attribute()
        
        def __try_get_travel_data_attribute(travel_data, from_zone, to_zone, attribute, default_value=None):
            if default_value is None:
                default_value = self.travel_data_attribute_default_value
            try:
                result = travel_data.get_attribute_by_id(attribute, (from_zone, to_zone))
            except:
                logger.log_warning("zone pair (from_zone_id %s, to_zone_id %s) is not in travel_data; value set to default %s." % (from_zone, to_zone, default_value))
                result = default_value
            return result

        for a in ij:
            i, j = a
            accessible_zones = []
            for zone in zone_ids:                
                t1 = __try_get_travel_data_attribute(travel_data, from_zone[i,j], zone, self.travel_data_attribute)
                t2 = __try_get_travel_data_attribute(travel_data, zone, to_zone[i,j], self.travel_data_attribute)
                if t1 + t2 <= agent_resource[i,j]:
                    accessible_zones.append(zone)
            if len(accessible_zones) > 0:
                results[i,j] = zones.get_attribute_by_id(self.zone_attribute_to_access, accessible_zones).sum()
                
        return results
