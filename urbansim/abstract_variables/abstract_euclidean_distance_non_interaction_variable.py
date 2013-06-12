# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import sqrt, logical_or, newaxis, tile


class abstract_euclidean_distance_non_interaction_variable(Variable):
    """Euclidean distance from one attribute of the agent set to another. 
    The distance is measured from the origin attribute to the destination attribute. 
    Both should be disaggregated to the agent dataset and should correspond 
    to the id attributes of location_dataset_name.
    For example, distance from persons locations to their work.
    """
    
    origin_attribute = "to_be_defined_in_child_class"
    destination_attribute = "to_be_defined_in_child_class"
    location_dataset_name = "to_be_defined_in_child_class"
    coordinate_attributes = ("x_coord", "y_coord") # attributes of location dataset
    impute_missing = True
    missing_value_threshold = 0
    default_value = -1
    
    def dependencies(self):
        return [ self.origin_attribute, self.destination_attribute, 
                "%s.%s" % (self.location_dataset_name, self.coordinate_attributes[0]),
                "%s.%s" % (self.location_dataset_name, self.coordinate_attributes[1])
             ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        agent_locations = dataset.get_attribute(self.origin_attribute)
        destinations = dataset.get_attribute(self.destination_attribute)
        location_dataset = dataset_pool.get_dataset(self.location_dataset_name)
        x = location_dataset[self.coordinate_attributes[0]]
        y = location_dataset[self.coordinate_attributes[1]]
        
        distance = sqrt( (x[location_dataset.try_get_id_index(agent_locations)] - x[location_dataset.try_get_id_index(destinations)])**2 \
                         + (y[location_dataset.try_get_id_index(agent_locations)] - y[location_dataset.try_get_id_index(destinations)])**2 
                          )
                                  
        if self.impute_missing:
            index_missing_value = logical_or(agent_locations <= self.missing_value_threshold, 
                                             destinations <= self.missing_value_threshold)
            distance[index_missing_value] = self.default_value
        
        return distance
    
