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
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.travel_data_attribute_default_value)
        
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
        zone_ids = zones.get_id_attribute()
        for zone in zone_ids:
            tmp_zone = zone * ones(from_zone.shape, dtype="int32")
            t1 = travel_data_attr_mat[from_zone, tmp_zone]
            t2 = travel_data_attr_mat[tmp_zone, to_zone]
            results[where( t1 + t2 <= agent_resource)] += zones.get_attribute_by_id(self.zone_attribute_to_access, zone)
                
        return results
