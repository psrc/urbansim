# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import array, concatenate, ones, newaxis
from opus_core.logger import logger

class abstract_travel_time_variable_1d(Variable):
    """abstract variable for 1-d travel time variables"""

    default_value = 180.0
    agent_zone_id = 'to_be_defined_in_fully_qualified_name'
    location_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'
    direction_from_home = True

    def dependencies(self):
        return [ self.agent_zone_id, self.location_zone_id, self.travel_data_attribute]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr = travel_data.get_attribute(self.travel_data_attribute)
        
        var1 = dataset.get_attribute(self.agent_zone_id)
        var2 = dataset.get_attribute(self.location_zone_id)
        if self.direction_from_home:
            home_zone = var1.astype("int32")
            work_zone = var2.astype("int32")
        else:
            home_zone = var2.astype("int32")
            work_zone = var1.astype("int32")
        
        results = array(home_zone.size*[self.default_value], dtype='float32')
        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(home_zone, work_zone)
        idx_for_valid_values = ones(home_zone.size, dtype='bool8')
        if missing_pairs_index[0].size > 0:
            logger.log_warning("zone pairs at index %s are not in travel data; value set to %s." % ( str(missing_pairs_index), self.default_value) )
            idx_for_valid_values[missing_pairs_index] = 0
        
        results[idx_for_valid_values] = travel_data.get_attribute_by_id(self.travel_data_attribute, 
                                            concatenate((home_zone[idx_for_valid_values][...,newaxis], 
                                                         work_zone[idx_for_valid_values][...,newaxis]),
                                                         axis=1)).astype('float32')
                
        return results
