# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import sqrt, logical_or, newaxis, tile


class abstract_euclidean_distance_variable(Variable):
    """Euclidean distance from one dataset to another. 
    It is an interaction variable. The distance is measured from a given id attribute of dataset 1 
    (agent_attribute) to a given id attribute of dataset 2 (location_attribute) of the interaction dataset. 
    For example, distance from households locations to locations of sampled alternatives.
    """
    
    agent_attribute = "to_be_defined_in_child_class"
    destination_attribute = "to_be_defined_in_child_class"
    location_dataset_name = "to_be_defined_in_child_class"
    coordinate_attributes = ("x_coord", "y_coord") # attributes of location dataset
    impute_missing = True
    missing_value_threshold = 0
    default_value = 99999999
    
    def dependencies(self):
        return [ self.agent_attribute, self.destination_attribute, 
                "%s.%s" % (self.location_dataset_name, self.coordinate_attributes[0]),
                "%s.%s" % (self.location_dataset_name, self.coordinate_attributes[1])
             ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        #agent_locations = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_attribute,
        #                                                interaction_dataset.get_2d_index_of_dataset1())
        agent_locations = interaction_dataset.get_attribute(self.agent_attribute)
        destinations = interaction_dataset.get_2d_dataset_attribute(self.destination_attribute)
        # put agents locations into the same shape as destinations
        #agent_locations = tile(agent_locations[:,newaxis], destinations.shape[1])
        location_dataset = dataset_pool.get_dataset(self.location_dataset_name)
        x = location_dataset[self.coordinate_attributes[0]]
        y = location_dataset[self.coordinate_attributes[1]]
        
        distance = (sqrt( (x[location_dataset.try_get_id_index(agent_locations.ravel())] - x[location_dataset.try_get_id_index(destinations.ravel())])**2 \
                         + (y[location_dataset.try_get_id_index(agent_locations.ravel())] - y[location_dataset.try_get_id_index(destinations.ravel())])**2 
                          )).reshape(agent_locations.shape)
                                  
        if self.impute_missing:
            index_missing_value = logical_or(agent_locations <= self.missing_value_threshold, 
                                             destinations <= self.missing_value_threshold)
            distance[index_missing_value] = self.default_value
        
        return distance
    
